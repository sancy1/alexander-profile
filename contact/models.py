
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


# NEWSLETTER CAMPAIGN --------------------------------------------------------------------------
class NewsletterCampaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'user_account.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='newsletter_campaigns'
    )
    recipient_count = models.IntegerField(default=0)
    opened_count = models.IntegerField(default=0)
    clicked_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Newsletter Campaign'
        verbose_name_plural = 'Newsletter Campaigns'

    def __str__(self):
        return f"{self.title} - {self.status}"
