
# codehub/urls.copy()

from django.urls import path
from .views.categories import (
    CategoryListView,
    CategoryCreateView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategorySnippetsView
)
from .views.snippets import (
    SnippetListView,
    SnippetCreateView,
    SnippetDetailView,
    SnippetUpdateView,
    SnippetDeleteView,
    # SnippetReactionsView,
    # SnippetCommentsView,
    # SnippetRunView
)
from .views.reactions import SnippetReactionsView 
from .views.comments import SnippetCommentsView, CommentDetailView 
from .views.shares import SnippetShareActivityView
from .views.user_history import UserHistoryListCreateView, UserHistoryDetailView
from .views.code_runs import SnippetRunView


urlpatterns = [
    # Category endpoints
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<slug:slug>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/<slug:slug>/snippets/', CategorySnippetsView.as_view(), name='category-snippets'),
    
    # Snippet endpoints
    path('snippets/create/', SnippetCreateView.as_view(), name='snippet-create'),
    path('snippets/', SnippetListView.as_view(), name='snippet-list'),
    path('snippets/<slug:slug>/', SnippetDetailView.as_view(), name='snippet-detail'),
    path('snippets/<slug:slug>/update/', SnippetUpdateView.as_view(), name='snippet-update'),
    path('snippets/<slug:slug>/delete/', SnippetDeleteView.as_view(), name='snippet-delete'),
    
    # Reaction endpoints
    path('snippets/<slug:slug>/reactions/', SnippetReactionsView.as_view(), name='snippet-reactions'),
   
    # For Creating/Updating a Reaction:
    # http://localhost:8000/api/codehub/snippets/<slug:slug>/reactions/
    
    # HTTP Method: DELETE
    # Endpoint: http://localhost:8000/api/codehub/snippets/<slug:slug>/reactions/
    
    # Purpose: To check if the authenticated user has already reacted to a snippet and what that reaction is.
    # Method: GET
    # URL: http://localhost:8000/api/codehub/snippets/<your_snippet_slug>/reactions/
    
    # Scenario 3: Change Reaction from Like to Dislike (Update)
    # {
    #     "is_like": false
    # }
    # Purpose: To update an existing reaction (e.g., changing a 'like' to a 'dislike').
    # Pre-requisite: You must have already performed Scenario 1 (liked the snippet).
    # Method: POST
    # URL: http://localhost:8000/api/codehub/snippets/<your_snippet_slug>/reactions/
    
  
    # Comments endpoints
    # Path for listing comments on a snippet and creating new top-level comments/replies
    path('snippets/<slug:slug>/comments/', SnippetCommentsView.as_view(), name='snippet-comments'),
    
    # Path for retrieving, updating, or deleting a specific comment by its primary key
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    
    path('snippets/<slug:slug>/shares/', SnippetShareActivityView.as_view(), name='snippet-shares'),
    
    # User History endpoints <--- NEW SECTION
    path('history/', UserHistoryListCreateView.as_view(), name='user-history-list-create'),
    path('history/<int:pk>/', UserHistoryDetailView.as_view(), name='user-history-detail'),
    
    # Code Run endpoint
    path('snippets/<slug:slug>/run/', SnippetRunView.as_view(), name='snippet-run'),
]



