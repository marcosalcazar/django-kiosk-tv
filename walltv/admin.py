from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from ordered_model.admin import OrderedModelAdmin, OrderedTabularInline
from polymorphic.admin.childadmin import PolymorphicChildModelAdmin
from polymorphic.admin.filters import PolymorphicChildModelFilter
from polymorphic.admin.parentadmin import PolymorphicParentModelAdmin

try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode
from django.utils.translation import ugettext as _

from walltv.models import Row, URLVideoPanel, Panel, ImagePanel, CarouselPanel, ImageForCarouselPanel, HeaderRow, \
    FooterRow, ContentRow, TextPanel, RSSOneLinePanel, RSSPanel


class MainRowAdmin(admin.ModelAdmin):
    object_history_template = "custom_admin/singleton/object_history.html"
    change_form_template = "custom_admin/singleton/change_form.html"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super(MainRowAdmin, self).get_urls()

        # _meta.model_name only exists on Django>=1.6 -
        # on earlier versions, use module_name.lower()
        try:
            model_name = self.model._meta.model_name
        except AttributeError:
            model_name = self.model._meta.module_name.lower()

        self.model._meta.verbose_name_plural = self.model._meta.verbose_name
        url_name_prefix = '%(app_name)s_%(model_name)s' % {
            'app_name': self.model._meta.app_label,
            'model_name': model_name,
        }
        custom_urls = [
            url(r'^history/$',
                self.admin_site.admin_view(self.history_view),
                {'object_id': str(self.singleton_instance_id)},
                name='%s_history' % url_name_prefix),
            url(r'^$',
                self.admin_site.admin_view(self.change_view),
                {'object_id': str(self.singleton_instance_id)},
                name='%s_change' % url_name_prefix),
        ]
        # By inserting the custom URLs first, we overwrite the standard URLs.

        return custom_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if object_id == str(self.singleton_instance_id):
            self.model.objects.get_or_create(pk=self.singleton_instance_id)
        return super(MainRowAdmin, self).change_view(
            request,
            object_id,
            form_url=form_url,
            extra_context=extra_context,
        )

    def response_change(self, request, obj):
        msg = _('%(obj)s was changed successfully.') % {'obj': force_unicode(obj)}
        if '_continue' in request.POST:
            self.message_user(request, msg + ' ' + _('You may edit it again below.'))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

        return HttpResponseRedirect("../../")

    @property
    def singleton_instance_id(self):
        if not hasattr(self.model, 'singleton_instance_id'):
            raise Exception('Missing config for model %s: singleton_instance_id' % self.model)
        return self.model.singleton_instance_id


@admin.register(HeaderRow)
class HeaderRowAdmin(MainRowAdmin):
    pass


@admin.register(ContentRow)
class ContentRowAdmin(MainRowAdmin):
    pass


@admin.register(FooterRow)
class FooterRowAdmin(MainRowAdmin):
    pass


@admin.register(Row)
class RowAdmin(OrderedModelAdmin):
    list_display = ('name', 'parent', 'height', 'columns', 'move_up_down_links')


@admin.register(Panel)
class PanelParentAdmin(PolymorphicParentModelAdmin, OrderedModelAdmin):
    """ The parent model admin """
    base_model = Panel
    child_models = (URLVideoPanel, ImagePanel, RSSOneLinePanel, RSSPanel, CarouselPanel)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
    list_display = ('name', 'move_up_down_links')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
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


@admin.register(TextPanel)
class ImagePanelAdmin(PanelChildAdmin):
    base_model = TextPanel
    show_in_index = True


@admin.register(RSSPanel)
class RSSPanelPanelAdmin(PanelChildAdmin):
    base_model = RSSPanel
    show_in_index = True


@admin.register(RSSOneLinePanel)
class RSSOneLinePanelAdmin(PanelChildAdmin):
    base_model = RSSOneLinePanel
    show_in_index = True


class ImageForCarouselPanelAdmin(OrderedTabularInline):
    model = ImageForCarouselPanel
    readonly_fields = ('order', 'move_up_down_links',)
    ordering = ('order',)


@admin.register(CarouselPanel)
class CarouselPanelAdmin(PanelChildAdmin):
    base_model = CarouselPanel
    show_in_index = True
    inlines = [
        ImageForCarouselPanelAdmin
    ]

    def get_urls(self):
        urls = super(CarouselPanelAdmin, self).get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls
