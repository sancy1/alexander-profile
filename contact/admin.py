
# contact/admin.py

from django.contrib import admin, messages
from .models import Contact, NewsletterSubscriber, DeletedSubscriber
from .services import NewsletterService

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'is_archived')
    list_filter = ('is_read', 'is_archived', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read', 'is_archived')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_archived')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active', 'unsubscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    list_editable = ('is_active',)
    date_hierarchy = 'subscribed_at'
    ordering = ('-subscribed_at',)

    fieldsets = (
        (None, {
            'fields': ('email', 'is_active')
        }),
        ('Dates', {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Contact, ContactAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)


@admin.register(DeletedSubscriber)
class DeletedSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'unsubscribed_at', 'deleted_at')
    list_filter = ('deleted_at', 'unsubscribed_at')
    search_fields = ('email',)
    readonly_fields = ('unsubscribed_at', 'deleted_at')
    date_hierarchy = 'unsubscribed_at'
    ordering = ('-unsubscribed_at',)

    fieldsets = (
        (None, {
            'fields': ('email',)
        }),
        ('Timestamps', {
            'fields': ('unsubscribed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['reactivate_selected_subscribers', 'delete_selected'] # Add your custom action here

    def reactivate_selected_subscribers(self, request, queryset):
        """
        Custom admin action to reactivate selected deleted subscribers.
        Moves them from DeletedSubscriber back to NewsletterSubscriber.
        """
        reactivated_count = 0
        failed_count = 0
        for deleted_subscriber in queryset:
            email = deleted_subscriber.email
            try:
                # Call the service method to reactivate.
                # It returns a tuple: (response_data, status_code)
                response_data, status_code = NewsletterService.reactivate_deleted_subscriber(email)

                if response_data.get('success'):
                    reactivated_count += 1
                else:
                    failed_count += 1
                    self.message_user(
                        request,
                        f"Failed to reactivate '{email}': {response_data.get('message', 'Unknown error.')}",
                        level=messages.ERROR
                    )
            except Exception as e:
                failed_count += 1
                self.message_user(
                    request,
                    f"An error occurred trying to reactivate '{email}': {str(e)}",
                    level=messages.ERROR
                )

        if reactivated_count > 0:
            self.message_user(
                request,
                f"Successfully reactivated {reactivated_count} subscriber(s).",
                level=messages.SUCCESS
            )
        if failed_count > 0:
            self.message_user(
                request,
                f"Failed to reactivate {failed_count} subscriber(s). Check error messages for details.",
                level=messages.WARNING
            )

    reactivate_selected_subscribers.short_description = "Reactivate selected deleted subscribers" # Display name for the action
