from concurrent import futures
from itertools import repeat

from django.core.management.base import BaseCommand, CommandError

from characters.models import (
    Character, CharacterComic, CharacterEvent, CharacterSeries, CharacterStory, Comic, Event, Series, Story,
)

MAX_WORKERS = 30
CHARACTERS_FOUND = 0
CHARACTERS_NOT_FOUND = 0
ASSOCIATIONS = 0

RESOURCES = dict(
    comics=(Comic, CharacterComic),
    series=(Series, CharacterSeries),
    events=(Event, CharacterEvent),
    stories=(Story, CharacterStory),
)


class Command(BaseCommand):
    help = 'Get resource and append to respective Characters'

    def add_arguments(self, parser):
        parser.add_argument(
            'resource', help='Choose the resource.', type=str,
        )

    def handle(self, *args, **options):
        resource_name = options['resource']
        try:
            Resource, ResourceRelation = RESOURCES.get(resource_name)
        except TypeError:
            raise CommandError(
                'Please choose a correct resource.'
            )
        resources = Resource.objects.all()

        with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
            executor.map(
                associate_resource_to_characters,
                repeat(resource_name),
                repeat(ResourceRelation),
                resources
            )

        print(f'{CHARACTERS_FOUND} Characters found')
        print(f'{CHARACTERS_NOT_FOUND} Characters not found')
        print(f'{ASSOCIATIONS} Associations')


def associate_resource_to_characters(resource_name, resource_relation, resource):
    items = resource.data['characters']['items']
    ResourceRelation = resource_relation
    print(f'Processing {len(items)} {resource_name} item(s) for {resource}')
    for item in items:
        try:
            character = Character.objects.get(
                name=item['name'],
                resource_uri=item['resourceURI'],
            )
        except Character.DoesNotExist:
            print(f"\tCharacter {item['name']} not found.")
            global CHARACTERS_NOT_FOUND
            CHARACTERS_NOT_FOUND += 1
            continue
        global CHARACTERS_FOUND
        CHARACTERS_FOUND += 1
        data = {character: character, resource_name: resource}
        character_resource, created = ResourceRelation.objects.get_or_create(
            **data
        )
        if created:
            global ASSOCIATIONS
            ASSOCIATIONS += 1
            print(f'\t\tAssociating {resource} to {character}')
        else:
            print(f'\t\tAssociation for {resource} to {character} already exists.')

    print(f'\tEnd of process for {resource}\n')
