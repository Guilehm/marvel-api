from concurrent import futures

from django.core.management.base import BaseCommand

from characters.models import Character, ComicItem

MAX_WORKERS = 30
CHARACTERS_FOUND = 0
CHARACTERS_NOT_FOUND = 0
ASSOCIATIONS = 0


class Command(BaseCommand):
    help = 'Get comics and append to respective Characters'

    def handle(self, *args, **options):
        comics = ComicItem.objects.all()
        with futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
            executor.map(associate_comic_to_characters, comics)

        print(f'{CHARACTERS_FOUND} Characters found')
        print(f'{CHARACTERS_NOT_FOUND} Characters not found')
        print(f'{CHARACTERS_NOT_FOUND} Associations')


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
        global ASSOCIATIONS
        CHARACTERS_FOUND += 1
        character.comics.add(comic)
        print(f'\t\tAssociating {comic} to {character}')

    print(f'\tEnd of process for {comic}\n')
