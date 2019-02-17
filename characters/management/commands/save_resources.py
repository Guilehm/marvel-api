from concurrent import futures
from itertools import repeat

from django.core.management.base import BaseCommand, CommandError
from requests.exceptions import RequestException

from api.utils import Marvel
from characters.models import Comic, Event, Series, StoryItem
from marvel.settings import PRIVATE_KEY, PUBLIC_KEY

REQUEST_COUNT = 0
REQUEST_ERROR_COUNT = 0
RESOURCES_CREATED = 0
RESOURCES_UPDATED = 0

MAX_WORKERS = 35
RESOURCES = dict(
    comics=Comic,
    series=Series,
    events=Event,
    stories=StoryItem,
)


class Command(BaseCommand):
    help = 'Import character list to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'resource', help='Choose the resource.', type=str,
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
        resource_name = options['resource']
        start = options['start']
        stop = options['stop']

        try:
            marvel = Marvel(PRIVATE_KEY, PUBLIC_KEY)
        except TypeError:
            raise CommandError(
                'Please check your environment variables for public and private keys.'
            )

        get_all_results(marvel, resource_name, start, stop)
        print(f'{REQUEST_COUNT} requests')
        print(f'{REQUEST_ERROR_COUNT} requests failed')
        print(f'{RESOURCES_CREATED} resources created')
        print(f'{RESOURCES_UPDATED} resources updated')


def get_results(marvel, resource_name, offset=0, limit=100):
    print(f'Requesting for "/{resource_name}/" with offset: {offset}.')
    try:
        response = marvel.send_request(resource_name, offset=offset, limit=limit)
        global REQUEST_COUNT
        REQUEST_COUNT += 1
        response.raise_for_status()
        results = response.json()['data']['results']
    except RequestException:
        global REQUEST_ERROR_COUNT
        REQUEST_ERROR_COUNT += 1
        results = list()
        print(f'{resource_name.title()} with offset: {offset} data could not be downloaded.')
    print(f'Got response for "/{resource_name}/" with offset: {offset}.')
    create_all_resources(resource_name, results)
    return results


def get_all_results(marvel, resource_name, start, stop):
    offsets = [number for number in range(start, stop, 100)]
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
        resource_type = result.get('type')
        if resource_type:
            resource.type = resource_type
        resource.save()
        if created:
            message = f'Creating {resource_name} {result["id"]} {result["title"]}.'
            global RESOURCES_CREATED
            RESOURCES_CREATED += 1
        else:
            message = f'{resource_name.title()} {result["id"]} {result["title"]} already exists.'
            global RESOURCES_UPDATED
            RESOURCES_UPDATED += 1
        print(message)


def create_all_resources(resource_name, results):
    with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
        for result in results:
            executor.map(create_resource(resource_name, result))
