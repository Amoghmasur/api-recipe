from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

class Command(BaseCommand):
    """django command to wait for database"""

    def handle(self,*args,**options):
        """entery point for command"""
        self.stdout.write('waiting for databse..')
        db_up=False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up=True
            except (Psycopg2OpError,OperationalError):
                self.stdout.write('database unavailabe,waiting for 1second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('databse available'))