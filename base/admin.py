# base/admin.py
from django.contrib import admin
from .models import Quote, LaserCuttingSpec, PressBrakeSpec, TubeLaserSpec # Import new models

admin.site.register(Quote)
admin.site.register(LaserCuttingSpec) # Register new spec models
admin.site.register(PressBrakeSpec)
admin.site.register(TubeLaserSpec)