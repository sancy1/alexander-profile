# codehub/views/snippets.py

from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from ..models import CodeSnippet, Category
from ..serializers import (
    CodeSnippetSerializer,
    CodeSnippetListSerializer,
    ReactionSerializer,
    CommentSerializer,
    CodeRunSerializer
)
from user_account.permissions import IsAdminOrSuperUser # Ensure this is correctly imported
from ..filters import CodeSnippetFilter
from ..services.snippet_services import (
    process_code_content,
    get_snippet_with_engagement
)


class SnippetListView(generics.ListAPIView):
    """
    GET: List all code snippets (Public)
    Includes filtering, searching, and ordering capabilities.
    """
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSnippetListSerializer
    permission_classes = [permissions.AllowAny] # As requested, public access
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CodeSnippetFilter # Use the existing CodeSnippetFilter
    search_fields = ['title', 'description', 'code_content', 'tags'] # Fields to search across
    ordering_fields = [ # Fields allowed for ordering
        '-created_at', 'created_at',
        '-updated_at', 'updated_at',
        'title', '-title',
        'difficulty', '-difficulty',
        'language', '-language',
    ]
    ordering = ['-created_at'] # Default ordering
    
    

class SnippetCreateView(generics.CreateAPIView):
    """
    POST: Create new snippet (Admin Only)
    Slug generation is now handled automatically by the CodeSnippet model's pre_save signal.
    """
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSnippetSerializer
    permission_classes = [IsAdminOrSuperUser]

    def perform_create(self, serializer):
        # The slug will be generated automatically by the model's pre_save signal.
        # No need for manual slug generation or conflict handling here.
        try:
            # You might still want to call process_code_content for other validations
            processed_data = process_code_content(serializer.validated_data)
            serializer.save(uploaded_by=self.request.user, **processed_data)
        except ValidationError as e:
            # Re-raise ValidationError with a 400 Bad Request if process_code_content fails
            raise e
        except IntegrityError:
            # This block might still catch rare race conditions or other IntegrityErrors
            # not related to slug if the pre_save hook fails (unlikely for slug now).
            # The slug conflict error specifically should be handled by the model's pre_save.
            return Response(
                {"detail": "An integrity error occurred, possibly a unique constraint violation."},
                status=status.HTTP_400_BAD_REQUEST
            )


class SnippetDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve snippet details (Authenticated)
    """
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSnippetSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_snippet_with_engagement(instance)
        return Response(data)

class SnippetUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update snippet (Admin Only)
    """
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSnippetSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrSuperUser]

    def perform_update(self, serializer):
        processed_data = process_code_content(serializer.validated_data)
        # The slug generation for updates is handled by the pre_save hook on the model
        serializer.save(**processed_data)

class SnippetDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete snippet (Admin Only)
    """
    queryset = CodeSnippet.objects.all()
    serializer_class = CodeSnippetSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrSuperUser]

    def perform_destroy(self, instance):
        instance.delete()

# class SnippetReactionsView(generics.ListAPIView):
#     """
#     GET: List reactions for a snippet
#     """
#     serializer_class = ReactionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         snippet_slug = self.kwargs['slug']
#         snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
#         return snippet.reactions.all()



# class SnippetCommentsView(generics.ListCreateAPIView):
#     """
#     GET: List comments for a snippet
#     POST: Create new comment (authenticated users)
#     """
#     serializer_class = CommentSerializer
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['-created_at']
#     ordering = ['-created_at']

#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         return [permissions.AllowAny()]

#     def get_queryset(self):
#         snippet_slug = self.kwargs['slug']
#         snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
#         return snippet.comments.filter(parent__isnull=True)

#     def perform_create(self, serializer):
#         snippet_slug = self.kwargs['slug']
#         snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
#         serializer.save(
#             user=self.request.user,
#             snippet=snippet
#         )



class SnippetRunView(generics.CreateAPIView):
    """
    POST: Log code execution/run
    """
    serializer_class = CodeRunSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        snippet_slug = self.kwargs['slug']
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(
            snippet=snippet,
            user=user,
            user_agent=self.request.META.get('HTTP_USER_AGENT'),
            ip_address=self.request.META.get('REMOTE_ADDR')
        )