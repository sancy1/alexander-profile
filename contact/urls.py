
# contact/urls.py

from django.urls import path
from .views import (
    ContactCreateView, ContactListView, ContactDetailView, ContactUpdateView, ContactDeleteView,
    NewsletterSubscribeView, NewsletterUnsubscribeView, NewsletterListView, 
    NewsletterDetailView, NewsletterUpdateView, NewsletterDeleteView, DeletedSubscriberListView,
    DeletedSubscriberDetailView, DeletedSubscriberDeleteView, DeletedSubscriberClearAllView,
    ReactivateDeletedSubscriberView,
)

urlpatterns = [
    # Contact URLs
    path('contacts/create/', ContactCreateView.as_view(), name='contact-create'),
    path('contacts/', ContactListView.as_view(), name='contact-list'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('contacts/<int:pk>/update/', ContactUpdateView.as_view(), name='contact-update'),
    path('contacts/<int:pk>/delete/', ContactDeleteView.as_view(), name='contact-delete'),
    
    # Newsletter URLs
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('newsletter/unsubscribe/', NewsletterUnsubscribeView.as_view(), name='newsletter-unsubscribe'),
    path('newsletter/subscribers/', NewsletterListView.as_view(), name='newsletter-list'), 
    path('newsletter/subscribers/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter-detail'),
    path('newsletter/subscribers/<int:pk>/update/', NewsletterUpdateView.as_view(), name='newsletter-update'),
    path('newsletter/subscribers/<int:pk>/delete/', NewsletterDeleteView.as_view(), name='newsletter-delete'),
    
    # Deleted Newsletter Subscribers (Admin Only)
    path('newsletter/deleted/', DeletedSubscriberListView.as_view(), name='deleted-subscriber-list'),
    path('newsletter/deleted/<int:pk>/', DeletedSubscriberDetailView.as_view(), name='deleted-subscriber-detail'),
    path('newsletter/deleted/<int:pk>/delete/', DeletedSubscriberDeleteView.as_view(), name='deleted-subscriber-delete-single'),
    path('newsletter/deleted/clear-all/', DeletedSubscriberClearAllView.as_view(), name='deleted-subscriber-clear-all'),
    path('newsletter/deleted/reactivate/', ReactivateDeletedSubscriberView.as_view(), name='deleted-subscriber-reactivate'),
]