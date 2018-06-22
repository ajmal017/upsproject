from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Trade)
admin.site.register(UserRole)
admin.site.register(Strategy)
admin.site.register(Scripts)
