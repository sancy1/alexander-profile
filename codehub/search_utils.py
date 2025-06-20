
# codehub/search_utils.py

from django.db.models import Q

def build_snippet_search_query(params):
    """
    Constructs complex Q objects for snippet searches
    Returns: Q object for filtering
    """
    query = Q()
    
    # Text search
    if 'q' in params:
        search_term = params['q']
        query &= (
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(code_content__icontains=search_term) |
            Q(tags__icontains=search_term)
        )
    
    # Exact matches
    if 'language' in params:
        query &= Q(language__iexact=params['language'])
    
    if 'difficulty' in params:
        query &= Q(difficulty=params['difficulty'])
    
    if 'category' in params:
        query &= Q(category__slug__iexact=params['category'])
    
    if 'output_type' in params:
        query &= Q(output_type__iexact=params['output_type'])
    
    if 'is_featured' in params:
        query &= Q(is_featured=params['is_featured'])
    
    # Tag filtering
    if 'tags' in params:
        tags = [tag.strip().lower() for tag in params['tags'].split(',') if tag.strip()]
        if tags:
            tag_query = Q()
            for tag in tags:
                tag_query |= Q(tags__icontains=tag)
            query &= tag_query
    
    return query
