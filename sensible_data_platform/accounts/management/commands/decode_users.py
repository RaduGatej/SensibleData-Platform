from django.core.management.base import BaseCommand, CommandError
from accounts.decode_users import *

class Command(BaseCommand):
        def handle(self, *args, **options):
                decode_users(args[0])
