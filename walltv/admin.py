from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from polymorphic.admin.childadmin import PolymorphicChildModelAdmin
from polymorphic.admin.filters import PolymorphicChildModelFilter
from polymorphic.admin.parentadmin import PolymorphicParentModelAdmin

from walltv.models import Row, URLVideoPanel, Panel, ImagePanel


@admin.register(Row)
class RowAdmin(OrderedModelAdmin):
    list_display = ('name', 'height', 'move_up_down_links')


@admin.register(Panel)
class PanelParentAdmin(PolymorphicParentModelAdmin, OrderedModelAdmin):
    """ The parent model admin """
    base_model = Panel
    child_models = (URLVideoPanel, ImagePanel, )
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
    list_display = ('name', 'move_up_down_links')

    def has_add_permission(self, request):
        return False


class PanelChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Panel

    # # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
    #     ...
    # )


@admin.register(URLVideoPanel)
class URLVideoPanelAdmin(PanelChildAdmin):
    base_model = URLVideoPanel
    show_in_index = True


@admin.register(ImagePanel)
class ImagePanelAdmin(PanelChildAdmin):
    base_model = ImagePanel
    show_in_index = True
