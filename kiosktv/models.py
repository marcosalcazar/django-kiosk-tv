from django.db import models


class Row(models.Model):
    height = models.PositiveSmallIntegerField(choices=((str(i), i) for i in range(5, 101, 5)),
                                              help_text='Percentage used vertically of the screen')


class Frame(models.Model):
    parent = models.ForeignKey(Row)
    columns = models.PositiveSmallIntegerField(help_text='Columns in a row shouldn\'t exceed 12')

    class Meta:
        abstract = True

    def get_render_template(self):
        raise NotImplementedError()


class VideoFrame(Frame):
    url = models.URLField()


class CarouselFrame(Frame):
    wait_time = models.PositiveSmallIntegerField()


class ImageForImagesField(models.Model):
    carousel = models.ForeignKey(CarouselFrame)
    image = models.ImageField()
