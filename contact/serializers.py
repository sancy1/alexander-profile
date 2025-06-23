
# contact/serializers.py

from rest_framework import serializers
from .models import Contact, NewsletterSubscriber, DeletedSubscriber


# CONTACT ----------------------------------------------------------------------------
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'subject', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'created_at', 'is_read']


# NEWSLETTER ----------------------------------------------------------------------------
class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'subscribed_at', 'is_active']
        read_only_fields = ['id', 'subscribed_at']
        
        
class DeletedSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeletedSubscriber
        fields = ['id', 'email', 'unsubscribed_at', 'deleted_at']
        read_only_fields = ['id', 'unsubscribed_at', 'deleted_at']