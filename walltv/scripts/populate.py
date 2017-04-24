import datetime
import traceback

from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.management import call_command

from walltv.models import TextPanel, FooterRow, RSSOneLinePanel, ContentRow


def run():
    print("Resetting db")
    call_command('reset_db', interactive=True)

    print("Migrating db")
    call_command('migrate')

    print("Creating user admin (pass: administrator)")
    # User admin
    admin_data = {
        "id": 1,
        "password": "pbkdf2_sha256$36000$XEJlI6dWgXRS$v4QMWqte7Mv3RWlDre/LeCDbCztvwnK5XV+2At6qtmE=",
        "last_login": None,
        "is_superuser": True,
        "username": "admin",
        "first_name": "",
        "last_name": "",
        "email": "admin@admin.com",
        "is_staff": True,
        "is_active": True,
        "date_joined": datetime.datetime.now(),
        "groups": [],
        "user_permissions": []
    }
    try:
        admin = User.objects.create(**admin_data)
    except:
        print(traceback.format_exc())

    print("Create initial db data for walltv")
    call_command('walltv_initialize')

    print("Creating sample data")
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

    f = FooterRow.objects.get()
    TextPanel.objects.create(
        parent=f,
        name='footer_text',
        columns=3
    )
    RSSOneLinePanel.objects.create(
        parent=f,
        name='footer_rss',
        columns=9,
        url='http://losandes.com.ar/rss'
    )

    if settings.DEBUG:
        pass
