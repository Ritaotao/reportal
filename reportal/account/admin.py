from django.contrib import admin
from .models import Group, Role, Profile

# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display=('id','name', 'create_date',)
    #list_filter=()
    #search_fields=()

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display=('id','name', 'create_date', 'can_create', \
                'can_update', 'can_delete', 'can_submit',)
    #list_filter=()
    #search_fields=()

admin.site.register(Profile)

