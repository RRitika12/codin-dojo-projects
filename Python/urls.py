from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout?$', views.logout),
    url(r'^posts/new$', views.new),
    url(r'^addpost?$', views.addpost),
    url(r'^posts/(?P<my_val>\d+)/edit$', views.posts_edit),
    url(r'^posts/(?P<my_val>\d+)/edit/process$', views.process_edit),
    url(r'^(?P<id>[0-9]+)/delete$',	views.destroy, name="delete_post")
]