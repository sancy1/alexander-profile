
# codehub/services/snippet_services.py:

from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db import models
# from ..models import CodeSnippet, Category # Removed to break circular import

def generate_snippet_slug(title, existing_id=None):
    """
    Generate a unique slug from snippet title with collision handling.
    Args:
        title (str): The title of the code snippet.
        existing_id (UUID, optional): The ID of the existing snippet if updating. Defaults to None.
    Returns:
        str: A unique slug.
    """
    from ..models import CodeSnippet # Imported locally to break circular dependency

    base_slug = slugify(title)
    unique_slug = base_slug
    num = 1

    while True:
        qs = CodeSnippet.objects.filter(slug=unique_slug)
        if existing_id:
            qs = qs.exclude(id=existing_id)
        if not qs.exists():
            break
        unique_slug = f"{base_slug}-{num}"
        num += 1

    return unique_slug

def process_code_content(data):
    """
    Validate and process all snippet data including:
    - Category existence
    - Language-specific requirements
    - Default values

    Returns: dict (validated data)
    Raises: ValidationError if requirements not met
    """
    # Assuming Category is not needed at the top level of this file for now
    # If Category is needed for validation here, consider passing it as an argument
    # or importing it locally if it doesn't cause a circular dependency with models.py
    # from ..models import Category # If Category validation needs it

    # Enhanced category validation (from first version)
    if 'category' not in data:
        raise ValidationError({
            'category': 'This field is required'
        })

    # Language validation (from both versions)
    language = data.get('language')
    if not language:
        raise ValidationError({
            'language': 'This field is required'
        })

    # Web snippets validation (enhanced from both)
    if language in ['html', 'css', 'javascript']:
        if not any(data.get(field) for field in ['html_code', 'css_code', 'js_code']):
            raise ValidationError({
                'code_content': 'Web snippets require at least one of html_code, css_code, or js_code'
            })

    # Console snippets validation (from second version)
    elif language in ['python', 'java', 'cpp']:
        if not data.get('code_content'):
            raise ValidationError({
                'code_content': 'Console snippets require code_content'
            })

    # Set default simulated_output (from second version)
    if language in ['python', 'java', 'cpp', 'javascript'] and not data.get('simulated_output'):
        data['simulated_output'] = "Output will be displayed here"

    return data

def get_snippet_with_engagement(snippet):
    """
    Returns enriched snippet data with engagement stats
    Returns: dict
    """
    from ..serializers import CodeSnippetSerializer # Imported here to avoid circular dependency

    data = CodeSnippetSerializer(snippet).data

    # Engagement stats
    reactions = snippet.reactions.all()
    data.update({
        'like_count': reactions.filter(is_like=True).count(),
        'dislike_count': reactions.filter(is_like=False).count(),
        'comment_count': snippet.comments.count(),
        'view_count': snippet.user_history.aggregate(
            total_views=models.Sum('view_count')
        )['total_views'] or 0,
        'run_count': snippet.runs.count()
    })

    return data