from django.contrib import admin
from todo.models import User,Item,Dolist
# Register your models here.

admin.site.register(Dolist)
admin.site.register(Item)
admin.site.register(User)