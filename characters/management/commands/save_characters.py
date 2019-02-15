from django.core.management.base import BaseCommand, CommandError
from characters.models import Character
from api.utils import Marvel
from requests.exceptions import RequestException
from marvel.settings import PRIVATE_KEY, PUBLIC_KEY
from itertools import repeat
from concurrent import futures

MAX_WORKERS = 30


class Command(BaseCommand):
    help = 'Import character list to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'start', help='Choose the first character to iterate.',
        )
        parser.add_argument(
            'stop', help='Choose the last character to iterate.',
        )
        parser.add_argument(
            '--api-version', help='API Version',
        )
        parser.add_argument(
            '--offset', help='Skip the specified number of resources in the result set.',
        )

    def handle(self, *args, **options):
        start = int(options['start'])
        stop = int(options['stop'])

        try:
            marvel = Marvel(PRIVATE_KEY, PUBLIC_KEY)
        except TypeError:
            raise CommandError(
                'Please check your environment variables for public and private keys.'
            )

        results = get_all_results(marvel, start, stop)
        create_all_characters(results)


def get_results(marvel, offset):
    try:
        response = marvel.send_request('characters', offset=offset)
        response.raise_for_status()
        results = response.json()['data']['results']
    except RequestException:
        raise CommandError('Characters data could not be downloaded.')
    return results


def get_all_results(marvel, start, stop):
    offsets = [number for number in range(start, stop, 20)]
    with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
        results = [result for result in list(
            executor.map(get_results, repeat(marvel), offsets)
        ) for result in result]
    return results


def create_character(result):
    if result:
        character, created = Character.objects.get_or_create(
            id=result['id'],
            name=result['name'],
            description=result['description'],
            resource_uri=result['resourceURI'],
        )
        character.data = result
        character.save()
        if created:
            message = f'Creating Character {result["id"]} {result["name"]}.'
        else:
            message = f'Character {result["id"]} {result["name"]} already exists.'
        print(message)


def create_all_characters(results):
    with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
        for result in results:
            executor.map(create_character(result))