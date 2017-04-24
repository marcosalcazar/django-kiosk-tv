from django.core.management.base import BaseCommand

from walltv.models import HeaderRow, ContentRow, FooterRow
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates basic data'

    def handle(self, *args, **options):
        HeaderRow.objects.create(id=settings.HEADER_ROW_PK, height=20, logo_alt_text='Logo')
        ContentRow.objects.create(id=settings.CONTENT_ROW_PK, height=70)
        FooterRow.objects.create(id=settings.FOOTER_ROW_PK, height=10, text='Footer 2017')
