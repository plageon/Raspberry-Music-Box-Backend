from django.conf.urls import url, include
from .views import resume,pause,play_next,play_prev,volume_increase,volume_decrease,switch_album

urlpatterns = [
    url(r'resume$', resume, ),
    url(r'pause$', pause, ),
    url(r'play_next$', play_next, ),
    url(r'play_prev$', play_prev, ),
    url(r'volume_increase$', volume_increase, ),
    url(r'volume_decrease$', volume_decrease, ),
    url(r'switch_album$', switch_album, ),
]
