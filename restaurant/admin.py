from django.contrib import admin

from restaurant.models import Restaurant, Review, Menu, Deal

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Menu)
admin.site.register(Deal)