from django.conf.urls import url

from restaurant import views

urlpatterns = [
    url(r'^$', views.restaurants, name='restaurants'),
    url(r'^search/', views.search, name='search'),
    url(r'^order/', views.order, name='order'),
    url(r'^(?P<res_name>[\w &]+)/', views.detail, name='detail'),
]