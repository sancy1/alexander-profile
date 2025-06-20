
# # codehub/services/category_services.py

# from django.core.exceptions import ValidationError
# from ..models import Category

# def validate_category_name(name):
#     """
#     Ensure category name is unique
#     Raises ValidationError if name already exists
#     """
#     if Category.objects.filter(name__iexact=name).exists():
#         raise ValidationError("A category with this name already exists.")

# def get_category_with_stats(category):
#     """
#     Returns category data with additional statistics
#     """
#     from ..serializers import CategorySerializer  # Avoid circular imports
    
#     data = CategorySerializer(category).data
#     data['snippet_count'] = category.snippets.count()
#     return data













# # codehub/services/category_services.py

from django.utils.text import slugify
from django.core.exceptions import ValidationError
from ..models import Category
from django.db import models


def validate_category_name(name, instance=None):
    """
    Enhanced to handle both create and update scenarios
    """
    qs = Category.objects.filter(name__iexact=name)
    if instance:
        qs = qs.exclude(pk=instance.pk)
    if qs.exists():
        raise ValidationError("A category with this name already exists.")

def generate_category_slug(name):
    """
    Generate a unique slug from category name with collision handling
    """
    slug = slugify(name)
    unique_slug = slug
    num = 1
    while Category.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug

def get_category_with_stats(category):
    """
    Enhanced to include more statistics and filter capabilities
    """
    from ..serializers import CategorySerializer
    
    data = CategorySerializer(category).data
    data['snippet_count'] = category.snippets.count()
    data['featured_snippet_count'] = category.snippets.filter(is_featured=True).count()
    
    # Add language distribution
    languages = category.snippets.values('language').annotate(count=models.Count('language'))
    data['languages'] = {item['language']: item['count'] for item in languages}
    
    return data