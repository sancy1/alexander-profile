

# codehub/views/code_runs.py

from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404

from ..models import CodeSnippet, CodeRun # Import models
from ..serializers import CodeRunSerializer # Import serializer

class SnippetRunView(generics.ListCreateAPIView):
    """
    GET: List all code run activities for a specific snippet.
         (Useful for analytics on how often a snippet is run)
    POST: Log a new code run activity for a specific snippet.
          This is typically hit when a user executes the code in the frontend.
    """
    serializer_class = CodeRunSerializer
    # AllowAny for POST, as runs can be anonymous.
    # AllowAny for GET to see overall run activity for analytics, or IsAuthenticatedOrReadOnly.
    permission_classes = [permissions.AllowAny] 

    def get_queryset(self):
        """
        Returns code run activities for the specific snippet from the URL.
        """
        snippet_slug = self.kwargs['slug']
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
        return CodeRun.objects.filter(snippet=snippet).order_by('-run_at')

    def perform_create(self, serializer):
        """
        Automatically sets the 'snippet' field for the CodeRun instance
        based on the URL slug. The 'user', 'ip_address', and 'user_agent'
        are set by the serializer's create method.
        """
        snippet_slug = self.kwargs['slug']
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
        
        # Save the instance, injecting the snippet object directly
        serializer.save(snippet=snippet)