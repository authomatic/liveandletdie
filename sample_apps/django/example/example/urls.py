from django.urls import include, re_path
from example.views import home

urlpatterns = [
    re_path(r'^$', home, name='home'),
]
