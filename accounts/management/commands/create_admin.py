from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create default admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(email='admin@walletpro.com').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@walletpro.com',
                password='admin123',
                first_name='Super',
                last_name='Admin',
            )
            self.stdout.write(self.style.SUCCESS('Admin created: admin@walletpro.com / admin123'))
        else:
            self.stdout.write('Admin already exists.')
