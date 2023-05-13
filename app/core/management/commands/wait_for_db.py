"""
Django command to wait for the database to be available.
"""
import time

from termcolor2 import colored

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write(
            colored('[...WAITING FOR DATABASE...]', 'red')
        )
        time.sleep(1)
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(colored(
                    '[...DATABASE UNAVAILABLE, WAITING 1 SECOND...]',
                    'red')
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('[...DATABASE AVAILABLE!...]'))
