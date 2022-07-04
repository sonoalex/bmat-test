
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError # Error django throws when db isn't ready
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        '''
        Entrypoint command to wait for database
        '''
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(Psycopg2OpError, OperationalError):
                self.stdout.write('Database still unavailable, sleep 1s...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))