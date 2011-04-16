from django.conf.urls.defaults import *


urlpatterns = patterns('testapp.views',
    url(r'^(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$','view', name='product_detail'),
    url(r'^$', 'list', name="product_list"),
    url(r'^search/$', 'search', name="product_search"),
)
