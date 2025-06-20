
# codehub/filters.py

import django_filters
from django.db.models import Q
from .models import CodeSnippet

class CodeSnippetFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', label="Search")
    language = django_filters.CharFilter(field_name='language', lookup_expr='iexact')
    difficulty = django_filters.NumberFilter(field_name='difficulty')
    category = django_filters.CharFilter(field_name='category__slug')
    output_type = django_filters.CharFilter(field_name='output_type', lookup_expr='iexact')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')
    tags = django_filters.CharFilter(method='filter_tags')
    ordering = django_filters.CharFilter(method='filter_ordering')

    class Meta:
        model = CodeSnippet
        fields = ['language', 'difficulty', 'category', 'output_type', 'is_featured']

    def search(self, queryset, name, value):
        """Full-text search across multiple fields"""
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(code_content__icontains=value) |
            Q(tags__icontains=value)
        )

    def filter_tags(self, queryset, name, value):
        """Filter by comma-separated tags"""
        tags = [tag.strip().lower() for tag in value.split(',') if tag.strip()]
        if not tags:
            return queryset
            
        query = Q()
        for tag in tags:
            query |= Q(tags__icontains=tag)
        return queryset.filter(query)

    def filter_ordering(self, queryset, name, value):
        """Custom ordering handling"""
        valid_ordering = [
            '-created_at', 'created_at',
            '-updated_at', 'updated_at',
            'title', '-title',
            'difficulty', '-difficulty'
        ]
        
        if value in valid_ordering:
            return queryset.order_by(value)
        return queryset.order_by('-created_at')