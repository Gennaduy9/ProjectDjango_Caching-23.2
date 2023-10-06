from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@gmail.com',
            first_name='Root',
            last_name='SkyCom',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password('123qwe456rty')
        user.save()