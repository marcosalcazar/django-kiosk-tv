from django.core.management.base import BaseCommand

from walltv.models import HeaderRow, ContentRow, FooterRow, Row, TextPanel
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates sample data'

    def handle(self, *args, **options):
        c = ContentRow.objects.get()

        TextPanel.objects.create(
            text='SAMPLE SAMPLE',
            name='texto1',
            parent=c,
            columns=6
        )
        TextPanel.objects.create(
            text='SAMPLE2 SAMPLE2',
            name='texto2',
            parent=c,
            columns=6
        )
