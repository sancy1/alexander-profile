
# # codehub/views/categories.py

# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from ..models import Category
# from ..serializers import CategorySerializer, CodeSnippetListSerializer
# from user_account.permissions import IsAdminOrSuperUser

# from ..services.category_services import (
#     validate_category_name,
#     get_category_with_stats
# )

# class CategoryListView(generics.ListAPIView):
#     """
#     GET: List all categories (public access)
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         return Category.objects.all().order_by('name')

# class CategoryCreateView(generics.CreateAPIView):
#     """
#     POST: Create new category (admin only)
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminOrSuperUser]

#     def perform_create(self, serializer):
#         name = serializer.validated_data.get('name')
#         validate_category_name(name)
#         serializer.save()

# class CategoryDetailView(generics.RetrieveAPIView):
#     """
#     GET: Retrieve a single category (authenticated users)
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     lookup_field = 'slug'
#     permission_classes = [permissions.IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         data = get_category_with_stats(instance)
#         return Response(data)

# class CategoryUpdateView(generics.UpdateAPIView):
#     """
#     PUT/PATCH: Update a category (admin only)
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAdminOrSuperUser]

#     def perform_update(self, serializer):
#         name = serializer.validated_data.get('name')
#         if name and name != serializer.instance.name:
#             validate_category_name(name)
#         serializer.save()

# class CategoryDeleteView(generics.DestroyAPIView):
#     """
#     DELETE: Delete a category (admin only)
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAdminOrSuperUser]

# class CategorySnippetsView(generics.ListAPIView):
#     """
#     GET: List all snippets in a specific category (public access)
#     """
#     serializer_class = CodeSnippetListSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         category_slug = self.kwargs['slug']
#         category = get_object_or_404(Category, slug=category_slug)
#         return category.snippets.all().order_by('-created_at')
















# codehub/views/categories.py

from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from ..models import Category
from ..serializers import CategorySerializer, CodeSnippetListSerializer
from ..filters import CodeSnippetFilter  # Your existing filter
from user_account.permissions import IsAdminOrSuperUser
from ..services.category_services import (
    validate_category_name,
    generate_category_slug,
    get_category_with_stats
)

class CategoryListView(generics.ListAPIView):
    """
    GET: List all categories with advanced filtering
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'slug': ['exact'],
        'created_at': ['gte', 'lte', 'exact'],
    }
    search_fields = ['name', 'slug', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']

class CategoryCreateView(generics.CreateAPIView):
    """
    POST: Create new category with auto-slug generation
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrSuperUser]

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        validate_category_name(name)
        slug = generate_category_slug(name)
        serializer.save(slug=slug)

class CategoryDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve category by slug with enhanced statistics
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = get_category_with_stats(instance)
        return Response(data)

class CategoryUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update category with slug regeneration if name changes
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrSuperUser]

    def perform_update(self, serializer):
        name = serializer.validated_data.get('name')
        instance = self.get_object()
        
        if name and name != instance.name:
            validate_category_name(name, instance=instance)
            serializer.save(slug=generate_category_slug(name))
        else:
            serializer.save()

class CategoryDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete category by slug
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrSuperUser]

class CategorySnippetsView(generics.ListAPIView):
    """
    GET: List snippets in category with full filtering capabilities
    """
    serializer_class = CodeSnippetListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CodeSnippetFilter  # Your existing snippet filter
    ordering_fields = ['-created_at', 'title', 'difficulty']
    ordering = ['-created_at']

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=category_slug)
        return category.snippets.all()