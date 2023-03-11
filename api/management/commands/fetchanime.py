from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from api.views import Studio

class Command(BaseCommand):
    help = 'Fetch the seasonal animes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully ran job poll ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))