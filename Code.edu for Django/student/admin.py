from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += (
    ("Custom fields", {"fields": ("nickname", "profile_pic", "intro", "teacher", "group_in",)}),
)
admin.site.register(Question)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Problem)