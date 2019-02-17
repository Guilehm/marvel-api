from concurrent import futures

from django.core.management.base import BaseCommand

from characters.models import Character, Comic, CharacterComic

MAX_WORKERS = 30
CHARACTERS_FOUND = 0
CHARACTERS_NOT_FOUND = 0
ASSOCIATIONS = 0


class Command(BaseCommand):
    help = 'Get comics and append to respective Characters'

    def handle(self, *args, **options):
        comics = Comic.objects.all()
        with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
            executor.map(associate_comic_to_characters, comics)

        print(f'{CHARACTERS_FOUND} Characters found')
        print(f'{CHARACTERS_NOT_FOUND} Characters not found')
        print(f'{ASSOCIATIONS} Associations')


def associate_comic_to_characters(comic):
    items = comic.data['characters']['items']
    print(f'Processing {len(items)} item(s) for {comic}')
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
        character_comic, created = CharacterComic.objects.get_or_create(
            character=character, comic=comic
        )
        if created:
            global ASSOCIATIONS
            ASSOCIATIONS += 1
            print(f'\t\tAssociating {comic} to {character}')
        else:
            print(f'\t\tAssociation for {comic} to {character} already exists.')

    print(f'\tEnd of process for {comic}\n')
