# codehub/views/reactions.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView # <--- Make sure this is correctly imported
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from ..models import CodeSnippet, Reaction
from ..serializers import ReactionSerializer
from ..services.reaction_services import ReactionService

class SnippetReactionsView(APIView): # <--- Ensure it inherits from APIView
    """
    API endpoint for a user to manage their reaction (like/dislike) to a specific code snippet.
    
    - GET: Retrieve the current authenticated user's reaction to the snippet.
    - POST: Create a new reaction or update an existing one.
    - DELETE: Remove the current authenticated user's reaction to the snippet.
    """
    permission_classes = [IsAuthenticated] # Only authenticated users can react

    def get(self, request, slug):
        """
        Retrieve the current user's reaction to the snippet.
        """
        try:
            reaction = ReactionService.get_user_reaction(user=request.user, snippet_slug=slug)
        except CodeSnippet.DoesNotExist:
            return Response({"detail": "Code snippet not found."}, status=status.HTTP_404_NOT_FOUND)

        if reaction:
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No reaction found for this user on this snippet."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, slug): # <--- VERY IMPORTANT: Ensure this method name is exactly 'post' (lowercase)
        """
        Create a new reaction or update an existing one.
        """
        is_like = request.data.get('is_like')

        if not isinstance(is_like, bool): # Ensure is_like is explicitly a boolean
            return Response(
                {"detail": "The 'is_like' field is required and must be a boolean (true or false)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reaction, created = ReactionService.create_or_update_reaction(
                user=request.user,
                snippet_slug=slug,
                is_like_status=is_like
            )
        except CodeSnippet.DoesNotExist:
            return Response({"detail": "Code snippet not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e: # Catch any other unexpected errors from the service
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReactionSerializer(reaction, context={'request': request})
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=response_status)

    def delete(self, request, slug):
        """
        Remove the user's reaction to the snippet.
        """
        try:
            deleted = ReactionService.delete_reaction(user=request.user, snippet_slug=slug)
        except CodeSnippet.DoesNotExist:
            return Response({"detail": "Code snippet not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e: # Catch any other unexpected errors from the service
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "No reaction found for this user and snippet."}, status=status.HTTP_404_NOT_FOUND)