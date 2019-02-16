from concurrent import futures
from itertools import repeat

from django.core.management.base import BaseCommand, CommandError
from requests.exceptions import RequestException

from api.utils import Marvel
from characters.models import SeriesItem, EventItem, ComicItem, StoryItem
from marvel.settings import PRIVATE_KEY, PUBLIC_KEY

MAX_WORKERS = 5
RESOURCES = dict(
    comics=ComicItem,
    series=SeriesItem,
    events=EventItem,
    stories=StoryItem,
)


class Command(BaseCommand):
    help = 'Import character list to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'event', help='Choose the event.', type=str,
        )
        parser.add_argument(
            'start', help='Choose the first character to iterate.', type=int,
        )
        parser.add_argument(
            'stop', help='Choose the last character to iterate.', type=int,
        )
        parser.add_argument(
            '--limit', help='Choose the limit per request.', type=int,
        )
        parser.add_argument(
            '--api-version', help='API Version',
        )

    def handle(self, *args, **options):
        event_name = options['event']
        start = options['start']
        stop = options['stop']

        try:
            marvel = Marvel(PRIVATE_KEY, PUBLIC_KEY)
        except TypeError:
            raise CommandError(
                'Please check your environment variables for public and private keys.'
            )

        get_all_results(marvel, event_name, start, stop)


def get_results(marvel, resource_name, offset=0):
    try:
        response = marvel.send_request(resource_name, offset=offset)
        response.raise_for_status()
        results = response.json()['data']['results']
    except RequestException:

        raise CommandError(f'{resource_name.title()} data could not be downloaded. {response.status_code}')
    print(f'Got response for "/{resource_name}/" with offset: {offset}.')
    create_all_resources(resource_name, results)
    return results


def get_all_results(marvel, resource_name, start, stop):
    offsets = [number for number in range(start, stop, 20)]
    with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
        results = [result for result in list(
            executor.map(get_results, repeat(marvel), repeat(resource_name), offsets)
        ) for result in result]
    return results


def create_resource(resource_name, result):
    Resource = RESOURCES.get(resource_name)
    if result:
        resource, created = Resource.objects.get_or_create(
            id=result['id'],
            name=result['title'],
        )
        resource.data = result
        resource.save()
        if created:
            message = f'Creating {resource_name} {result["id"]} {result["title"]}.'
        else:
            message = f'{resource_name.title()} {result["id"]} {result["title"]} already exists.'
        print(message)


def create_all_resources(resource_name, results):
    with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
        for result in results:
            executor.map(create_resource(resource_name, result))
