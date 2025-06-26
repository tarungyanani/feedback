from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Feedback

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'manager')  # shows in user list
    list_filter = ('role',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'manager')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Feedback)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('employee', 'manager', 'sentiment', 'acknowledged', 'created_at')
    list_filter = ('sentiment', 'acknowledged')
    search_fields = ('employee__username', 'manager__username')

admin.site.unregister(Feedback)  # if already registered above
admin.site.register(Feedback, FeedbackAdmin)
