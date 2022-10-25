from django.core.management.base import BaseCommand, CommandError
from app.tasks import *


class Command(BaseCommand):
    help = 'Update status of insurance'

    def add_arguments(self, parser):
        parser.add_argument('user_id')

    def handle(self, *args, **options):
        try:
            user = User.objects.get(pk=options['user_id'])
        except:
            raise CommandError('User "%s" does not exist' % options['user_id'])
        user.first_name = 'Nguyen Thuq'
        user.save()
