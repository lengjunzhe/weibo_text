from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from weibo_text.views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weibo_text.views.home', name='home'),
    # url(r'^weibo_text/', include('weibo_text.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
      url(r'^$',weibo_login),
      url(r'^login/$',weibo_login2),
      url(r'^index/$',weibo_index),
      url(r'^login/user1.html/$',user1),
      url(r'^user/(\d+)$',friendships),
      url(r'^login/user1.html/allfollow$',allfollow),
      url(r'^login/user1.html/follow_byid$',follow_byid),
      url(r'^group/$',group_found),
      url(r'^group/group_show/$',group_show),
      url(r'^group/group_show/(\d+)/$',group_list),
      url(r'^group/group_show/(\d+)/append/$',group_append),
      url(r'^group/group_show/(\d+)/join/$',group_join),
   #   url(r'^static/(?p<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,'show_indexes':True}),
)
