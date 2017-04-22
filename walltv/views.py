from django.views.generic.base import TemplateView

from walltv.models import HeaderRow, ContentRow, FooterRow


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['header_row'] = HeaderRow.objects.get()
        context['content_row'] = ContentRow.objects.get()
        context['footer_row'] = FooterRow.objects.get()
        return context
