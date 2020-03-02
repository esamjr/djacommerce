from django.conf.urls import url
from account.views import WithOutCache, PerViewCache, PerDataCache
from django.views.decorators.cache import cache_page

urlpatterns = [
    # without cache
    url(r'without-cache/$', WithOutCache),
    # with cache in url
    url(r'with-cache-url/$', cache_page(60 * 15)(WithOutCache)),
    # With Per View
    url(r'per-view-cache/$', PerViewCache),
    # With Per Data
    url(r'per-data-cache/$', PerDataCache),
]
