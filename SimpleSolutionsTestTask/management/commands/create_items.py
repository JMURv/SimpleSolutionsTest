import random
import string
from django.core.management import BaseCommand
from SimpleSolutionsTestTask.models import Item


def generate_random_string(length=10, min_letters=4):
    """Create a random string with a minimum of min_letters letters"""
    characters = string.ascii_letters + string.digits
    letters = string.ascii_letters

    if min_letters > length:
        raise ValueError("min_letters cannot be greater than length")

    num_letters = random.randint(min_letters, length)
    num_digits = length - num_letters

    random_username = (
        ''.join(random.choice(letters) for _ in range(num_letters)) +
        ''.join(random.choice(characters) for _ in range(num_digits))
    )
    return random_username


CURRENCY = [
    "usd",
    "eur",
]


class Command(BaseCommand):
    help = 'Creates items'

    def handle(self, *args, **options):
        if Item.objects.count() > 0:
            return self.stdout.write(
                self.style.SUCCESS('Items already exists')
            )
        for _ in range(1, 10):
            Item.objects.create(
                name=generate_random_string(
                    length=8,
                    min_letters=6
                ),
                description=generate_random_string(
                    length=100,
                    min_letters=50
                ),
                price=100,
                currency=random.choice(CURRENCY)
            )

        return self.stdout.write(
            self.style.SUCCESS('Successfully created items')
        )
