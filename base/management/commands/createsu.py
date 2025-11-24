from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser with a default username and password'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = 'ChangeMe123!'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser: {username}')
            )
            self.stdout.write(
                self.style.WARNING('IMPORTANT: Please change the password after first login!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists')
            )
