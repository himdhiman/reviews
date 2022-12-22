from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_list = settings.ADMINS
        for user in users_list:
            qs = User.objects.filter(email=user[1])
            if len(qs) == 0:
                username = user[0].replace(" ", "")
                email = user[1]
                password = user[2]
                print("Creating account for %s (%s)" % (username, email))
                admin = User.objects.create_superuser(
                    email=email, username=username, password=password
                )
                admin.is_active = True
                admin.is_admin = True
                admin.save()
            else:
                print(f"User {qs.first().email} already exists")
        return

