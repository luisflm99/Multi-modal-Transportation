from django.contrib import admin
from .models import Location, Route, Order


for model in [Location, Route, Order]:
    admin.site.register(model)
