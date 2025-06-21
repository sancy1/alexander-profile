
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import ShareActivity, CodeSnippet # Import CodeSnippet
from ..serializers import ShareActivitySerializer

class SnippetShareActivityView(generics.ListCreateAPIView):
    """
    GET: List share activities for a specific code snippet.
         (Optional: you might only need POST for simple share logging)
    POST: Create a new share activity for a code snippet.
    """
    serializer_class = ShareActivitySerializer
    # Allow shares from unauthenticated users if you want to track all shares.
    # If shares should only be logged for authenticated users, change to [IsAuthenticated].
    permission_classes = [AllowAny] 

    def get_queryset(self):
        """
        Filters share activities by the snippet slug from the URL.
        This method is used for GET requests to /snippets/<slug>/shares/
        """
        snippet_slug = self.kwargs['slug']
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
        # Assuming you want to order by most recent shares
        return ShareActivity.objects.filter(snippet=snippet).order_by('-shared_at')

    def perform_create(self, serializer):
        """
        Automatically sets the 'snippet' field for the ShareActivity
        based on the URL slug. The 'user' and 'ip_address' are set
        by the serializer's create method.
        """
        snippet_slug = self.kwargs['slug']
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
        serializer.save(snippet=snippet)