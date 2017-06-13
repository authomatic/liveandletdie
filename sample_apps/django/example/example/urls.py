from django.conf.urls import url

from example.views import home


urlpatterns = [
    url(r'^$', home, name='home'),
]
