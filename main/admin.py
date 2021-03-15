from django.contrib import admin
from .models import *
# Register your models here.


class Usersubscribe(admin.ModelAdmin):
    list_display=('email', 'date_added')


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Subscribe,Usersubscribe)