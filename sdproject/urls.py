from django.conf.urls import url, include
from django.contrib import admin

import restaurant

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('home.urls', namespace="home")),
    url(r'^restaurant/', include('restaurant.urls', namespace="restaurant")),
    url(r'^register/', include('register.urls', namespace="register")),
]
