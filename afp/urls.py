from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'afp.web.views.home', name='afp.home'),
    url(r'^fondos-(?P<slug>[a-e]+)$', 'afp.web.views.funds_by_name', name='funds_by_name'),
    url(r'^(?P<slug>[A-Za-z0-9\-]+)$', 'afp.web.views.funds_by_administrator', name='funds_by_administrator'),
    url(r'^fondo/chart-data$', 'afp.web.views.fund_chart_data'),
)

urlpatterns += staticfiles_urlpatterns()
