import os

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from embed_video.fields import EmbedVideoField
from ordered_model.models import OrderedModel
from polymorphic.models import PolymorphicModel


class ModelRenderMixin:
    """
    https://github.com/a1fred/django-model-render/
    """
    template_path = None

    def get_template_path(self):
        return getattr(
            self, "template_path", None) or os.path.join(
            self._meta.app_label,
            'models',
            self._meta.object_name.lower() + "." + getattr(
                settings, "MODEL_RENDER_DEFAULT_EXTENSION", "html"))

    def render(self, template=None, additional=None):
        """
        Render single model to its html representation.
        You may set template path in render function argument,
            or model's variable named 'template_path',
            or get default name: $app_label$/models/$model_name$.html
        Settings:
        * MODEL_RENDER_DEFAULT_EXTENSION
            set default template extension. Usable if you use jinja or others.
        :param template: custom template_path
        :return: rendered model html string
        """
        template_path = template or self.get_template_path()

        template_vars = {'model': self}
        if additional:
            template_vars.update(additional)

        rendered = render_to_string(template_path, template_vars)
        return mark_safe(rendered)


class Row(ModelRenderMixin, OrderedModel):
    template_path = 'models/row.html'
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    height = models.PositiveSmallIntegerField(help_text=_('Percentage used vertically of the screen'))
    # background_color = ColorPicker()

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.name


class Panel(PolymorphicModel, ModelRenderMixin, OrderedModel):
    parent = models.ForeignKey(Row, related_name='panels', verbose_name=_('Parent'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    columns = models.PositiveSmallIntegerField(help_text=_('Columns in a row shouldn\'t exceed 12'),
                                               verbose_name=_('Columns'))

    def get_template_path(self):
        raise NotImplementedError()

    def __str__(self):
        return self.name


class URLVideoPanel(Panel):
    """
    Used for Youtube/Vimeo/soundcloud
    """
    video_url = EmbedVideoField(verbose_name=_('Video URL'))

    def get_template_path(self):
        return 'models/urlvideopanel.html'


class VideoPanel(Panel):
    file = models.FileField(verbose_name=_('File'))


class ImagePanel(Panel):
    image = models.ImageField(verbose_name=_('Image'))

    def get_template_path(self):
        return 'models/imagepanel.html'


class CarouselPanel(Panel):
    wait_time = models.PositiveSmallIntegerField(verbose_name=_('Wait time'))


class ImageForImagesField(models.Model):
    carousel = models.ForeignKey(CarouselPanel)
    image = models.ImageField(verbose_name=_('Image'))


class TextPanel(models.Model):
    text = models.TextField(verbose_name=_('Text'))


class WeatherPanel(models.Model):
    location = models.CharField(max_length=255, verbose_name=_('Location'))


class RSSPanel(models.Model):
    url = models.URLField(verbose_name=_('URL'))
