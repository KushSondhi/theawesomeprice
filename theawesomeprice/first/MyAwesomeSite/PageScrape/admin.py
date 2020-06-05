from django.contrib import admin

# Register your models here.
from .models import Shopclues,Snapdeal,Shopclue,Amazon

admin.site.register(Snapdeal)
admin.site.register(Shopclues)
admin.site.register(Shopclue)
admin.site.register(Amazon)