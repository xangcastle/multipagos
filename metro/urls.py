from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
import autocomplete_light
from metropolitana.views import home

autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^adminactions/', include('adminactions.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^entregas/', include('metropolitana.urls')),
    url(r'^cartera/', include('cartera.urls')),
    url(r'^movil/', include('movil.urls')),
    url(r'^digitalizacion/', include('digitalizacion.urls')),
    url(r'^report_builder/', include('report_builder.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
