# codehub/services/reaction_services.py

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError as DjangoValidationError
from ..models import CodeSnippet, Reaction

class ReactionService:
    @staticmethod
    def create_or_update_reaction(user, snippet_slug, is_like_status):
        """
        Creates a new reaction or updates an existing one for a user on a snippet.
        If a reaction already exists:
        - If is_like_status is different, the existing reaction's 'is_like' is updated.
        - If is_like_status is the same, no change is made (user reacted again with same status).
        Returns the Reaction instance and a boolean indicating if it was created.
        """
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)

        with transaction.atomic():
            reaction, created = Reaction.objects.get_or_create(
                user=user,
                snippet=snippet,
                defaults={'is_like': is_like_status}
            )
            if not created:
                # If reaction already existed, check if 'is_like' status needs updating
                if reaction.is_like != is_like_status:
                    reaction.is_like = is_like_status
                    reaction.save(update_fields=['is_like'])
        return reaction, created

    @staticmethod
    def get_user_reaction(user, snippet_slug):
        """
        Retrieves a user's specific reaction for a code snippet.
        Returns the Reaction instance or None if not found.
        """
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
        return Reaction.objects.filter(user=user, snippet=snippet).first()

    @staticmethod
    def delete_reaction(user, snippet_slug):
        """
        Deletes a user's reaction for a specific snippet.
        Returns True if deleted, False if no reaction was found.
        """
        snippet = get_object_or_404(CodeSnippet, slug=snippet_slug)
        deleted_count, _ = Reaction.objects.filter(user=user, snippet=snippet).delete()
        return deleted_count > 0