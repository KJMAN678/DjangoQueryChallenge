from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext
from queryapp.models import User


class Command(BaseCommand):
    help = 'Demonstrate Django SQL query inspection methods'

    def handle(self, *args, **options):
        User.objects.all().delete()
        
        User.objects.create(username="gustave")
        User.objects.create(username="alice")
        User.objects.create(username="bob")
        
        self.stdout.write(self.style.SUCCESS('=== Method 1: Using qs.query ==='))
        qs = User.objects.filter(username="gustave")
        print(qs.query)
        
        self.stdout.write(self.style.SUCCESS('\n=== Method 2: Using connection.queries ==='))
        reset_queries()
        list(User.objects.filter(username="gustave"))
        print(connection.queries)
        
        self.stdout.write(self.style.SUCCESS('\n=== Method 3: Using CaptureQueriesContext ==='))
        with CaptureQueriesContext(connection) as ctx:
            list(User.objects.filter(username="gustave"))
            print(ctx.captured_queries)
        
        self.stdout.write(self.style.SUCCESS('\nAll SQL query methods demonstrated successfully!'))
