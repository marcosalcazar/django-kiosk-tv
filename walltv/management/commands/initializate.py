from django.core.management.base import BaseCommand

from walltv.models import HeaderRow, ContentRow, FooterRow


class Command(BaseCommand):
    help = 'Creates basic data'

    def handle(self, *args, **options):
        HeaderRow.objects.create(id=1, height=20, logo_alt_text='Logo')
        ContentRow.objects.create(id=2, height=70)
        FooterRow.objects.create(id=3, height=10)
