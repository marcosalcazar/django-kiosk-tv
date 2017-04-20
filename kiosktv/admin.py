from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from kiosktv.models import Row


class RowAdmin(OrderedModelAdmin):
    list_display = ('name', 'height', 'move_up_down_links')


admin.site.register(Row, RowAdmin)
