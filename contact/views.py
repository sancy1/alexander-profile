
# # contact/views.py

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
# from django.db.models import Q

# from .services import ContactService, NewsletterService, DeletedSubscriber
# from .serializers import ContactSerializer, NewsletterSubscriberSerializer, DeletedSubscriberSerializer
# from .models import Contact, NewsletterSubscriber
# from user_account.permissions import IsAdminOrSuperUser
# from rest_framework.exceptions import ValidationError



# # CONTACT ----------------------------------------------------------------------------
# # Contact Views
# class ContactCreateView(APIView):
#     permission_classes = [AllowAny]
    
#     def post(self, request):
#         try:
#             contact = ContactService.create_contact(request.data)
#             if contact:
#                 serializer = ContactSerializer(contact)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response({'error': 'Failed to create contact'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class ContactListView(ListAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     serializer_class = ContactSerializer
    
#     def get_queryset(self):
#         return ContactService.get_all_contacts()


# class ContactDetailView(RetrieveAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     serializer_class = ContactSerializer
#     queryset = Contact.objects.all()
#     lookup_field = 'pk'


# class ContactUpdateView(UpdateAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     serializer_class = ContactSerializer
#     queryset = Contact.objects.all()
#     lookup_field = 'pk'


# class ContactDeleteView(DestroyAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     queryset = Contact.objects.all()
#     lookup_field = 'pk'


# class ContactSearchView(APIView):
#     permission_classes = [IsAdminOrSuperUser]

#     def get(self, request):
#         try:
#             query = request.query_params.get('q', '')
#             is_read = request.query_params.get('is_read', '')
#             date_from = request.query_params.get('date_from', '')
#             date_to = request.query_params.get('date_to', '')

#             contacts = Contact.objects.all()

#             if query:
#                 contacts = contacts.filter(
#                     Q(name__icontains=query) |
#                     Q(email__icontains=query) |
#                     Q(subject__icontains=query)
#                 )

#             if is_read:
#                 contacts = contacts.filter(is_read=is_read.lower() == 'true')

#             if date_from:
#                 contacts = contacts.filter(created_at__gte=date_from)

#             if date_to:
#                 contacts = contacts.filter(created_at__lte=date_to)

#             serializer = ContactSerializer(contacts, many=True)
#             return Response({
#                 "status": "success",
#                 "count": contacts.count(),
#                 "data": serializer.data
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"error": f"Failed to search contacts: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class ContactStatisticsView(APIView):
#     permission_classes = [IsAdminOrSuperUser]

#     def get(self, request):
#         try:
#             from datetime import timedelta
#             from django.utils import timezone

#             total_contacts = Contact.objects.count()
#             unread_contacts = Contact.objects.filter(is_read=False).count()
#             read_contacts = total_contacts - unread_contacts

#             # Contacts by date (last 30 days)
#             thirty_days_ago = timezone.now() - timedelta(days=30)
#             recent_contacts = Contact.objects.filter(created_at__gte=thirty_days_ago).count()

#             # Contacts by date (last 7 days)
#             seven_days_ago = timezone.now() - timedelta(days=7)
#             very_recent_contacts = Contact.objects.filter(created_at__gte=seven_days_ago).count()

#             return Response({
#                 "status": "success",
#                 "data": {
#                     "total_contacts": total_contacts,
#                     "unread_contacts": unread_contacts,
#                     "read_contacts": read_contacts,
#                     "recent_contacts_30_days": recent_contacts,
#                     "recent_contacts_7_days": very_recent_contacts
#                 }
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"error": f"Failed to retrieve contact statistics: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )



# # NEWSLETTER ----------------------------------------------------------------------------
# # Newsletter Views

# class NewsletterSubscribeView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             subscriber = NewsletterService.subscribe_email(request.data)
#             # NewsletterSubscriberSerializer now only has email, subscribed_at, id
#             return Response(NewsletterSubscriberSerializer(subscriber).data, status=status.HTTP_201_CREATED)
#         except ValidationError as e:
#             # ValidationError from service will have a dict for the error.
#             return Response(e.detail, status=status.HTTP_400_BAD_REQUEST) # Use e.detail for serializer errors
#         except Exception as e:
#             # Catch any other unexpected errors from the service
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class NewsletterUnsubscribeView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):  # For clickable links
#         email = request.query_params.get('email')
#         success, message = NewsletterService.unsubscribe_email(email)
#         if success:
#             return Response({"message": message}, status=status.HTTP_200_OK)
#         return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request):  # For API requests (e.g., from a form)
#         email = request.data.get('email')
#         success, message = NewsletterService.unsubscribe_email(email)
#         if success:
#             return Response({"message": message}, status=status.HTTP_200_OK)
#         return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


# class NewsletterListView(ListAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     serializer_class = NewsletterSubscriberSerializer
#     # ONLY show active subscribers here
#     queryset = NewsletterSubscriber.objects.filter(is_active=True).order_by('-subscribed_at')


# class NewsletterDetailView(RetrieveAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     serializer_class = NewsletterSubscriberSerializer
#     queryset = NewsletterSubscriber.objects.filter(is_active=True) # Only active can be detailed
#     lookup_field = 'pk'


# # Admin can update status (though with new logic, they are deleted upon unsubscribe)
# # This update view could be used for other properties if added to active subscriber model.
# # If an admin updates an active subscriber to be *inactive*, you'd need custom logic here
# # to move it to deleted. For now, we assume active subscribers are only removed by unsubscribe_email.
# class NewsletterUpdateView(UpdateAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     serializer_class = NewsletterSubscriberSerializer
#     queryset = NewsletterSubscriber.objects.filter(is_active=True)
#     lookup_field = 'pk'

#     def update(self, request, *args, **kwargs):
#         # Prevent manual setting of is_active to False if it should trigger deletion
#         if 'is_active' in request.data and not request.data['is_active']:
#             return Response({"error": "Use the unsubscribe endpoint for deactivating subscribers."},
#                             status=status.HTTP_400_BAD_REQUEST)
#         return super().update(request, *args, **kwargs)


# class NewsletterDeleteView(DestroyAPIView):
#     # This view would now be for direct deletion of *active* subscribers by admin.
#     # If the intention is to move to deleted, use the unsubscribe view with admin credentials.
#     # Given the new logic, deleting from this view would be a permanent delete of an *active* subscriber.
#     # It might be safer to remove this view or clarify its purpose.
#     # For this implementation, we'll keep it but note its function.
#     permission_classes = [IsAdminOrSuperUser]
#     queryset = NewsletterSubscriber.objects.filter(is_active=True)
#     lookup_field = 'pk'

#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # DELETED SUBSCRIBERS (Admin Only) -------------------------------------------------
# class DeletedSubscriberListView(ListAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     serializer_class = DeletedSubscriberSerializer
#     queryset = DeletedSubscriber.objects.all().order_by('-deleted_at')


# class DeletedSubscriberDetailView(RetrieveAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     serializer_class = DeletedSubscriberSerializer
#     queryset = DeletedSubscriber.objects.all()
#     lookup_field = 'pk'


# class DeletedSubscriberDeleteView(DestroyAPIView):
#     permission_classes = [IsAdminOrSuperUser]
#     queryset = DeletedSubscriber.objects.all()
#     lookup_field = 'pk'
#     # This deletes a single entry from the DeletedSubscriber list

# class DeletedSubscriberClearAllView(APIView):
#     permission_classes = [IsAdminOrSuperUser]

#     def delete(self, request, *args, **kwargs):
#         response_data, status_code = NewsletterService.delete_all_deleted_subscribers()
#         return Response(response_data, status=status_code)
    
    
# class ReactivateDeletedSubscriberView(APIView):
#     permission_classes = [IsAdminOrSuperUser]

#     def post(self, request):
#         """
#         Allows an admin to reactivate a subscriber by moving them from the
#         deleted list back to the active subscriber list.
#         Expects {'email': 'subscriber@example.com'} in the request body.
#         """
#         email = request.data.get('email')
#         response_data, status_code = NewsletterService.reactivate_deleted_subscriber(email)
#         return Response(response_data, status=status_code)










































# contact/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from django.db.models import Q
from rest_framework.exceptions import ValidationError

# FIXED: Moved DeletedSubscriber from .services import directly to the .models block
from .services import ContactService, NewsletterService
from .serializers import ContactSerializer, NewsletterSubscriberSerializer, DeletedSubscriberSerializer
from .models import Contact, NewsletterSubscriber, DeletedSubscriber  
from user_account.permissions import IsAdminOrSuperUser


# CONTACT ----------------------------------------------------------------------------
class ContactCreateView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            contact = ContactService.create_contact(request.data)
            if contact:
                serializer = ContactSerializer(contact)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'Failed to create contact'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ContactListView(ListAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = ContactSerializer
    
    def get_queryset(self):
        return ContactService.get_all_contacts()


class ContactDetailView(RetrieveAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    lookup_field = 'pk'


class ContactUpdateView(UpdateAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    lookup_field = 'pk'


class ContactDeleteView(DestroyAPIView):
    permission_classes = [IsAdminOrSuperUser]
    queryset = Contact.objects.all()
    lookup_field = 'pk'


class ContactSearchView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):
        try:
            query = request.query_params.get('q', '')
            is_read = request.query_params.get('is_read', '')
            date_from = request.query_params.get('date_from', '')
            date_to = request.query_params.get('date_to', '')

            contacts = Contact.objects.all()

            if query:
                contacts = contacts.filter(
                    Q(name__icontains=query) |
                    Q(email__icontains=query) |
                    Q(subject__icontains=query)
                )

            if is_read:
                contacts = contacts.filter(is_read=is_read.lower() == 'true')

            if date_from:
                contacts = contacts.filter(created_at__gte=date_from)

            if date_to:
                contacts = contacts.filter(created_at__lte=date_to)

            serializer = ContactSerializer(contacts, many=True)
            return Response({
                "status": "success",
                "count": contacts.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to search contacts: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContactStatisticsView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):
        try:
            from datetime import timedelta
            from django.utils import timezone

            total_contacts = Contact.objects.count()
            unread_contacts = Contact.objects.filter(is_read=False).count()
            read_contacts = total_contacts - unread_contacts

            thirty_days_ago = timezone.now() - timedelta(days=30)
            recent_contacts = Contact.objects.filter(created_at__gte=thirty_days_ago).count()

            seven_days_ago = timezone.now() - timedelta(days=7)
            very_recent_contacts = Contact.objects.filter(created_at__gte=seven_days_ago).count()

            return Response({
                "status": "success",
                "data": {
                    "total_contacts": total_contacts,
                    "unread_contacts": unread_contacts,
                    "read_contacts": read_contacts,
                    "recent_contacts_30_days": recent_contacts,
                    "recent_contacts_7_days": very_recent_contacts
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve contact statistics: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# NEWSLETTER ----------------------------------------------------------------------------
class NewsletterSubscribeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            subscriber = NewsletterService.subscribe_email(request.data)
            return Response(NewsletterSubscriberSerializer(subscriber).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewsletterUnsubscribeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):  # Clickable unsubscribe routing
        email = request.query_params.get('email')
        success, message = NewsletterService.unsubscribe_email(email)
        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):  # Frontend form submission routing
        email = request.data.get('email')
        success, message = NewsletterService.unsubscribe_email(email)
        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


class NewsletterListView(ListAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = NewsletterSubscriberSerializer
    queryset = NewsletterSubscriber.objects.filter(is_active=True).order_by('-subscribed_at')


class NewsletterDetailView(RetrieveAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = NewsletterSubscriberSerializer
    queryset = NewsletterSubscriber.objects.filter(is_active=True)
    lookup_field = 'pk'


class NewsletterUpdateView(UpdateAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = NewsletterSubscriberSerializer
    queryset = NewsletterSubscriber.objects.filter(is_active=True)
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        if 'is_active' in request.data and not request.data['is_active']:
            return Response({"error": "Use the unsubscribe endpoint for deactivating subscribers."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class NewsletterDeleteView(DestroyAPIView):
    permission_classes = [IsAdminOrSuperUser]
    queryset = NewsletterSubscriber.objects.filter(is_active=True)
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        """FIXED: Router triggers service lifecycle instead of hard SQL row purge"""
        instance = self.get_object()
        success, message = NewsletterService.unsubscribe_email(instance.email)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


# DELETED SUBSCRIBERS (Admin Only) -------------------------------------------------
class DeletedSubscriberListView(ListAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = DeletedSubscriberSerializer
    queryset = DeletedSubscriber.objects.all().order_by('-deleted_at')


class DeletedSubscriberDetailView(RetrieveAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = DeletedSubscriberSerializer
    queryset = DeletedSubscriber.objects.all()
    lookup_field = 'pk'


class DeletedSubscriberDeleteView(DestroyAPIView):
    permission_classes = [IsAdminOrSuperUser]
    queryset = DeletedSubscriber.objects.all()
    lookup_field = 'pk'


class DeletedSubscriberClearAllView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def delete(self, request, *args, **kwargs):
        response_data, status_code = NewsletterService.delete_all_deleted_subscribers()
        return Response(response_data, status=status_code)
    
    
class ReactivateDeletedSubscriberView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def post(self, request):
        email = request.data.get('email')
        response_data, status_code = NewsletterService.reactivate_deleted_subscriber(email)
        return Response(response_data, status=status_code)