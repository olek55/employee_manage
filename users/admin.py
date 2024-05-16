from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount


class UserAccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'role', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)

    # Since we are using email as the USERNAME_FIELD, we need to adjust the add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.register(UserAccount, UserAccountAdmin)
