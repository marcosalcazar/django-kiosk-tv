from django.views.generic.base import TemplateView

from .models import Row


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['rows'] = Row.objects.all()
        return context