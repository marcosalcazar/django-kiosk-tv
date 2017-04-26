from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django_feedparser.views import FeedFetchMixin, FeedView

from walltv.models import HeaderRow, ContentRow, FooterRow, RSSPanel, RSSOneLinePanel


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['header_row'] = HeaderRow.objects.get()
        context['content_row'] = ContentRow.objects.get()
        context['footer_row'] = FooterRow.objects.get()
        return context


class RSSView(FeedFetchMixin, DetailView):
    model = RSSPanel
    template_name = 'models/panels/rsspanel_renderer.html'

    def get_context_data(self, **kwargs):
        context = super(RSSView, self).get_context_data(**kwargs)

        feed_url = self.get_feed_url()
        feed_renderer = self.get_feed_renderer()

        context['feed_url'] = feed_url
        context['feed_rendered'] = self.render_feed(feed_renderer, feed_url)

        return context

    def get_feed_url(self):
        return self.object.feed_url


class RSSOneLineView(RSSView):
    model = RSSOneLinePanel
    template_name = 'models/panels/rssonelinepanel_renderer.html'
