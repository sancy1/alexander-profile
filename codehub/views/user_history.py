

# codehub/views/user_history.py
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from django.db.models import F # Import F expression

from ..models import UserHistory, CodeSnippet, CustomUser # Ensure CustomUser is imported
from ..serializers import UserHistorySerializer
from ..permissions import IsOwnerOfUserHistory # Import your custom permission

class UserHistoryListCreateView(generics.ListCreateAPIView):
    """
    GET: List all user history entries for the authenticated user (their viewing/saving history).
    POST: Create a new user history entry or update an existing one (for logging a view).
          If a history entry for the user and snippet already exists, its view_count will be incremented
          and last_viewed updated.
          This is typically hit when a user *views* a snippet.
    """
    serializer_class = UserHistorySerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users have a history

    def get_queryset(self):
        """
        Returns history entries only for the authenticated user.
        """
        return UserHistory.objects.filter(user=self.request.user).order_by('-last_viewed')

    def perform_create(self, serializer):
        """
        Set the user for the history entry.
        The serializer's create method handles the get_or_create logic and view_count increment.
        """
        # The serializer's create method expects 'snippet' in validated_data.
        # It gets the user from request.user, so no need to explicitly pass it here
        # unless you want to override what the serializer's create method does.
        # In this setup, the serializer's create method is robust enough.
        serializer.save()


class UserHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific user history entry.
    PATCH/PUT: Update a specific user history entry (e.g., toggle is_saved).
              This will also increment view_count and update last_viewed due to serializer's update method.
    DELETE: Delete a specific user history entry.
    """
    queryset = UserHistory.objects.all()
    serializer_class = UserHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfUserHistory]
    lookup_field = 'pk' # or 'id', if you prefer to use primary key from URL


    # Optional: If you want to use snippet_slug for detail view instead of pk:
    # lookup_field = 'slug' # assuming snippet has a slug, and UserHistory has a custom manager/method to find by snippet slug
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     user = self.request.user
    #     snippet_slug = self.kwargs[self.lookup_url_kwarg] # assuming url uses snippet_slug
    #     obj = get_object_or_404(queryset, user=user, snippet__slug=snippet_slug)
    #     self.check_object_permissions(self.request, obj)
    #     return obj
    # For now, let's stick to PK for simplicity with RetrieveUpdateDestroyAPIView.
    