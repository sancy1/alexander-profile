
# contact/models.py

from django.db import models
from django.utils import timezone


# CONTACT ----------------------------------------------------------------------------
class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} - {self.subject}"


# NEWSLETTER ----------------------------------------------------------------------------
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return self.email
    


class DeletedSubscriber(models.Model):
    email = models.EmailField(unique=True)
    unsubscribed_at = models.DateTimeField(default=timezone.now) # When they unsubscribed
    deleted_at = models.DateTimeField(auto_now_add=True) # When they were moved to this table

    class Meta:
        ordering = ['-deleted_at']
        verbose_name = 'Deleted Subscriber'
        verbose_name_plural = 'Deleted Subscribers'

    def __str__(self):
        return self.email + " (deleted)"
