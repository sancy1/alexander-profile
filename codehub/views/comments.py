
# codehub/views/comments.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q # For filtering top-level comments if needed

from ..models import CodeSnippet, Comment
from ..serializers import CommentSerializer # <--- Import your CommentSerializer

# Custom permission to allow owners to edit/delete, others to only read
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Read permissions are allowed to any authenticated user.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the comment.
        return obj.user == request.user
    
    

class SnippetCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        snippet_slug = self.kwargs['slug']
        get_object_or_404(CodeSnippet, slug=snippet_slug) 
        return Comment.objects.filter(snippet__slug=snippet_slug, parent__isnull=True).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Set the user and snippet for the comment before saving.
        Handles both top-level comments and replies based on 'parent' field.
        """
        snippet_slug = self.kwargs['slug']
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)

        parent_comment = serializer.validated_data.get('parent')
        
        if parent_comment:
            # If it's a reply, ensure its snippet is correctly linked to the parent's snippet
            # (and optionally, verify it matches the URL's snippet if desired)
            if parent_comment.snippet != snippet: # This check is a good safety measure
                raise generics.ValidationError("Reply's snippet must match the parent comment's snippet.")
            serializer.save(user=self.request.user, snippet=parent_comment.snippet)
        else:
            # It's a top-level comment, associate it with the snippet from the URL
            serializer.save(user=self.request.user, snippet=snippet) 
            
            

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific comment.
    PUT/PATCH: Update a specific comment.
    DELETE: Delete a specific comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'pk' # Use primary key for lookup (e.g., /comments/1/)

    # Optional: If you want to ensure the comment belongs to the snippet in the URL
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     snippet_slug = self.kwargs.get('snippet_slug')
    #     if snippet_slug:
    #         queryset = queryset.filter(snippet__slug=snippet_slug)
    #     return queryset