import os

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
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
    name = models.CharField(max_length=255)
    height = models.PositiveSmallIntegerField(help_text='Percentage used vertically of the screen')

    class Meta(OrderedModel.Meta):
        pass


class Frame(ModelRenderMixin, PolymorphicModel, OrderedModel):
    parent = models.ForeignKey(Row)
    name = models.CharField(max_length=255)
    columns = models.PositiveSmallIntegerField(help_text='Columns in a row shouldn\'t exceed 12')

    def get_render_template(self):
        raise NotImplementedError()


class URLVideoFrame(Frame):
    """
    Used for Youtube/Vimeo/soundcloud
    """
    video_url = EmbedVideoField()


class VideoFrame(Frame):
    file = models.FileField()


class CarouselFrame(Frame):
    wait_time = models.PositiveSmallIntegerField()


class ImageForImagesField(models.Model):
    carousel = models.ForeignKey(CarouselFrame)
    image = models.ImageField()
