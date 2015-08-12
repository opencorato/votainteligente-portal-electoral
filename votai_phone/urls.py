from django.conf.urls import patterns, url
from votai_phone.views import MediaNaranjaView, MediaNaranjaResponseView, MediaNaranjaProblemView


urlpatterns = patterns('',
    url(r'^phone_medianaranja/?$', MediaNaranjaView.as_view(), name='phone_medianaranja'),
    url(r'^phone_medianaranja_save/?$', MediaNaranjaResponseView.as_view(), name='phone_medianaranja_save'),
    url(r'^phone_medianaranja_problem/?$', MediaNaranjaProblemView.as_view(), name='phone_medianaranja_problem'),
    )
