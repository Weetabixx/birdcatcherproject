"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import twitter_stream.views


urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^Admin', admin.site.urls),
    url(r'^Admin/', admin.site.urls),
    url(r'^Search', twitter_stream.views.search, name='search'),
    url(r'^(?P<tgroup_name>\w{1,50})', twitter_stream.views.index, name='index'),
    url(r'^(?P<tgroup_name>\w{1,50})/', twitter_stream.views.index, name='index'),
    url(r'', twitter_stream.views.home, name='home'),
   # url(r'^(?P<q>[\w-]+/?)', twitter_stream.views.home, name='home'),
    #url(r'^$', twitter_stream.views.index, name='index'),
]

