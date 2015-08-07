from django.conf.urls import patterns, url
from votai_phone.views import MediaNaranjaView


urlpatterns = patterns('',
    url(r'^phone_medianaranja/?$', MediaNaranjaView.as_view(), name='phone_medianaranja'),
    )
