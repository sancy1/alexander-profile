# # codehub/serializers.py

# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
# from django.utils.text import slugify
# from django.urls import reverse
# from .models import (
#     Category,
#     CodeSnippet,
#     Reaction,
#     Comment,
#     ShareActivity,
#     UserHistory,
#     CodeRun
# )
# # Import UserMinimalSerializer from your user_account app
# from user_account.serializers import UserMinimalSerializer # <--- IMPORTANT CHANGE
# from django.utils import timezone
# from django.db.models import F


# # Add this near the top of your serializers.py
# class CodeSnippetFilterSerializer(serializers.Serializer):
#     """Serializes filter parameters for API documentation"""
#     q = serializers.CharField(required=False, help_text="Search term (title, description, code, tags)")
#     language = serializers.CharField(required=False, help_text="Filter by programming language")
#     difficulty = serializers.IntegerField(required=False, min_value=1, max_value=3, help_text="Filter by difficulty level (1-3)")
#     category = serializers.CharField(required=False, help_text="Filter by category slug")
#     output_type = serializers.CharField(required=False, help_text="Filter by output type")
#     is_featured = serializers.BooleanField(required=False, help_text="Filter featured snippets")
#     tags = serializers.CharField(required=False, help_text="Comma-separated tags to filter by")
#     ordering = serializers.CharField(required=False, help_text="Ordering (-created_at, title, etc.)")
    

# # ==================== UTILITY SERIALIZERS ====================

# class DynamicFieldsModelSerializer(serializers.ModelSerializer):
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed.
#     """
#     def __init__(self, *args, **kwargs):
#         fields = kwargs.pop('fields', None)
#         super().__init__(*args, **kwargs)

#         if fields is not None:
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)

# # Removed the old UserSerializer definition from here.
# # It is now replaced by UserMinimalSerializer imported from user_account.serializers.

# # ==================== MAIN SERIALIZERS ====================

# class CategorySerializer(DynamicFieldsModelSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name='category-detail',
#         lookup_field='slug'
#     )
#     snippet_count = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = Category
#         fields = [
#             'id',
#             'name',
#             'slug',
#             'description',
#             'snippet_count',
#             'created_at',
#             'updated_at',
#             'url'
#         ]
#         extra_kwargs = {
#             'slug': {'read_only': True}
#         }

#     def validate_name(self, value):
#         """Ensure category name is unique"""
#         if self.instance and Category.objects.filter(name=value).exclude(pk=self.instance.pk).exists():
#             raise ValidationError("A category with this name already exists.")
#         return value

#     def create(self, validated_data):
#         """Auto-generate slug on creation (though model pre_save also handles)"""
#         if 'name' in validated_data and not validated_data.get('slug'):
#             validated_data['slug'] = slugify(validated_data['name'])
#         return super().create(validated_data)


# class CodeSnippetSerializer(DynamicFieldsModelSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name='snippet-detail',
#         lookup_field='slug'
#     )
#     language_display = serializers.CharField(
#         source='get_language_display',
#         read_only=True
#     )
#     difficulty_display = serializers.CharField(
#         source='get_difficulty_display',
#         read_only=True
#     )
#     output_type_display = serializers.CharField(
#         source='get_output_type_display',
#         read_only=True
#     )
#     # Use the imported UserMinimalSerializer here
#     uploaded_by = UserMinimalSerializer(read_only=True) # <--- IMPORTANT CHANGE
#     category = CategorySerializer(read_only=True) # Nested read-only category detail
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(),
#         source='category',
#         write_only=True,
#         required=True # Category is required for snippet creation
#     )
#     reaction_stats = serializers.SerializerMethodField()
#     comment_count = serializers.IntegerField(read_only=True)
#     share_count = serializers.IntegerField(read_only=True)
#     user_has_reacted = serializers.SerializerMethodField()
#     user_history = serializers.SerializerMethodField()

#     class Meta:
#         model = CodeSnippet
#         fields = [
#             # Core fields
#             'id', 'title', 'slug', 'url',
#             'description', 'short_description',
            
#             # Categorization
#             'language', 'language_display',
#             'output_type', 'output_type_display',
#             'difficulty', 'difficulty_display',
#             'category', 'category_id', 'tags',
            
#             # Code content
#             'code_content', 'html_code', 'css_code', 'js_code', 'additional_files',
            
#             # Simulation
#             'simulated_output', 'expected_result',
            
#             # Presentation
#             'thumbnail_image', 'is_featured',
            
#             # Ownership
#             'uploaded_by', 'created_at', 'updated_at', 'last_accessed',
            
#             # Stats
#             'reaction_stats', 'comment_count', 'share_count',
#             'user_has_reacted', 'user_history'
#         ]
#         extra_kwargs = {
#             'slug': {'read_only': True},
#             'code_content': {'required': False}, 
#             'simulated_output': {'write_only': True}, # Make simulated_output write-only for creation/update
#             'category': {'read_only': True}, # Ensure category object is read-only
#             'category_id': {'write_only': True} # Ensure category_id is write-only for submission
#         }

#     def get_reaction_stats(self, obj):
#         """Calculate like/dislike counts"""
#         return {
#             'likes': obj.reactions.filter(is_like=True).count(),
#             'dislikes': obj.reactions.filter(is_like=False).count()
#         }

#     def get_user_has_reacted(self, obj):
#         """Check if current user has reacted"""
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             reaction = obj.reactions.filter(user=request.user).first()
#             if reaction:
#                 return 'like' if reaction.is_like else 'dislike'
#         return None

#     def get_user_history(self, obj):
#         """Get user-specific interaction data"""
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             history = obj.user_history.filter(user=request.user).first()
#             if history:
#                 return {
#                     'view_count': history.view_count,
#                     'is_saved': history.is_saved,
#                     'last_viewed': history.last_viewed
#                 }
#         return None
    
#     def validate(self, data):
#         """
#         Custom validation for code content based on language type and category presence.
#         """
#         # For updates, get existing instance language if not provided in data
#         language = data.get('language', self.instance.language if self.instance else None)
        
#         # Category validation for creation
#         if not self.instance and 'category' not in data and 'category_id' not in data:
#             raise serializers.ValidationError({
#                 'category_id': 'This field is required for new snippets.'
#             })
            
#         # Ensure required code fields are present based on language
#         if language in ['html', 'css', 'javascript']:
#             if not any(data.get(field) for field in ['html_code', 'css_code', 'js_code', 'code_content']):
#                 raise ValidationError({
#                     'code': 'Web snippets require at least one code field (html_code, css_code, js_code or code_content).'
#                 })
        
#         elif language in ['python', 'java', 'cpp', 'csharp', 'go', 'rust', 'django', 'nodejs']: # Added more console/backend languages
#             if not data.get('code_content'):
#                 raise serializers.ValidationError({
#                     'code_content': f'{language.capitalize()} snippets require code_content.'
#                 })
        
#         return data

#     def create(self, validated_data):
#         """Auto-set uploaded_by"""
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             validated_data['uploaded_by'] = request.user
        
#         # Slug generation is handled by the CodeSnippet model's pre_save signal.
#         # No need to set validated_data['slug'] here.

#         return super().create(validated_data)


# class ReactionSerializer(serializers.ModelSerializer):
#     user = UserMinimalSerializer(read_only=True) # <--- IMPORTANT CHANGE
#     snippet = serializers.PrimaryKeyRelatedField(
#         queryset=CodeSnippet.objects.all(),
#         write_only=True
#     )

#     class Meta:
#         model = Reaction
#         fields = ['id', 'user', 'snippet', 'is_like', 'created_at']
#         read_only_fields = ['id', 'user', 'created_at']

#     def validate(self, data):
#         """Ensure one reaction per user per snippet"""
#         request = self.context.get('request')
#         snippet = data.get('snippet')
        
#         if request and request.user.is_authenticated:
#             if Reaction.objects.filter(user=request.user, snippet=snippet).exists():
#                 # For updates, allow modifying existing reaction
#                 if self.instance and self.instance.user == request.user and self.instance.snippet == snippet:
#                     return data
#                 raise ValidationError("You've already reacted to this snippet.")
        
#         return data

#     def create(self, validated_data):
#         """Auto-set user from request"""
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             validated_data['user'] = request.user
#         return super().create(validated_data)

# class CommentSerializer(DynamicFieldsModelSerializer):
#     user = UserMinimalSerializer(read_only=True) # <--- IMPORTANT CHANGE
#     snippet = serializers.PrimaryKeyRelatedField(
#         queryset=CodeSnippet.objects.all(),
#         write_only=True,
#         required=False
#     )
#     parent = serializers.PrimaryKeyRelatedField(
#         queryset=Comment.objects.all(),
#         required=False,
#         allow_null=True # Allow null for top-level comments
#     )
#     replies = serializers.SerializerMethodField()
#     user_vote = serializers.SerializerMethodField()

#     class Meta:
#         model = Comment
#         fields = [
#             'id',
#             'user',
#             'snippet',
#             'parent',
#             'text', # Assuming your Comment model has a 'text' field for content
#             'is_resolved',
#             'created_at',
#             'updated_at',
#             'replies',
#             'user_vote'
#         ]
#         read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'replies']

#     def get_replies(self, obj):
#         """Nested replies if they exist"""
#         if obj.replies.exists():
#             # Use self.__class__ for recursive serializer reference
#             return self.__class__(
#                 obj.replies.all(),
#                 many=True,
#                 context=self.context,
#                 fields=['id', 'user', 'text', 'created_at', 'parent'] # Added parent field for clarity in replies
#             ).data
#         return []

#     def get_user_vote(self, obj):
#         """Check if current user has voted on this comment (Placeholder)"""
#         # Implement if you add comment voting later
#         return None

#     def validate(self, data):
#         """Ensure either snippet or parent is set"""
#         if not data.get('snippet') and not data.get('parent'):
#             raise ValidationError("A comment must be associated with either a snippet or a parent comment.")
        
#         # If parent is provided, ensure snippet is not simultaneously provided
#         if data.get('parent') and data.get('snippet'):
#             raise ValidationError("A comment cannot be both a top-level comment and a reply simultaneously. Provide either 'snippet' or 'parent'.")
        
#         return data

# class ShareActivitySerializer(serializers.ModelSerializer):
#     user = UserMinimalSerializer(read_only=True) # <--- IMPORTANT CHANGE
#     snippet = serializers.PrimaryKeyRelatedField(
#         queryset=CodeSnippet.objects.all(),
#         write_only=True
#     )
#     share_method_display = serializers.CharField(
#         source='get_share_method_display',
#         read_only=True
#     )

#     class Meta:
#         model = ShareActivity
#         fields = [
#             'id',
#             'user',
#             'snippet',
#             'share_method',
#             'share_method_display',
#             'shared_to',
#             'shared_at',
#             'ip_address'
#         ]
#         read_only_fields = ['id', 'user', 'shared_at', 'ip_address']

#     def create(self, validated_data):
#         """Auto-set user and IP address"""
#         request = self.context.get('request')
#         if request:
#             validated_data['user'] = request.user if request.user.is_authenticated else None
#             validated_data['ip_address'] = request.META.get('REMOTE_ADDR')
#         return super().create(validated_data)

# class UserHistorySerializer(serializers.ModelSerializer):
#     user = UserMinimalSerializer(read_only=True) # <--- IMPORTANT CHANGE
#     snippet = CodeSnippetSerializer(read_only=True, fields=['id', 'title', 'slug']) # Only show relevant snippet fields
#     snippet_id = serializers.PrimaryKeyRelatedField(
#         queryset=CodeSnippet.objects.all(),
#         source='snippet',
#         write_only=True
#     )

#     class Meta:
#         model = UserHistory
#         fields = [
#             'id',
#             'user',
#             'snippet',
#             'snippet_id',
#             'last_viewed',
#             'view_count',
#             'is_saved',
#             'saved_at'
#         ]
#         read_only_fields = ['id', 'user', 'last_viewed', 'view_count']

#     def update(self, instance, validated_data):
#         """Handle incrementing view count and saving"""
#         if 'is_saved' in validated_data:
#             instance.is_saved = validated_data['is_saved']
#             if validated_data['is_saved'] and not instance.saved_at:
#                 instance.saved_at = timezone.now()
#             elif not validated_data['is_saved'] and instance.saved_at: # If unsaved, clear saved_at
#                 instance.saved_at = None 
#             instance.save(update_fields=['is_saved', 'view_count', 'last_viewed', 'saved_at'])
        
#         # Always increment view count on update and update last_viewed
#         instance.view_count = F('view_count') + 1
#         instance.last_viewed = timezone.now() 
#         instance.save(update_fields=['view_count', 'last_viewed'])

#         instance.refresh_from_db()
#         return instance

#     def create(self, validated_data):
#         """Create or update user history"""
#         request = self.context.get('request')
#         user = request.user if request and request.user.is_authenticated else None
#         snippet = validated_data['snippet']

#         # Check if history already exists for this user and snippet
#         history, created = UserHistory.objects.get_or_create(
#             user=user,
#             snippet=snippet,
#             defaults={'view_count': 1, 'last_viewed': timezone.now()}
#         )
#         if not created:
#             # If exists, update view count and last viewed
#             history.view_count = F('view_count') + 1
#             history.last_viewed = timezone.now()
#             history.save(update_fields=['view_count', 'last_viewed'])
#             history.refresh_from_db()

#         if 'is_saved' in validated_data:
#             history.is_saved = validated_data['is_saved']
#             if validated_data['is_saved'] and not history.saved_at:
#                 history.saved_at = timezone.now()
#             elif not validated_data['is_saved'] and history.saved_at: # If unsaved, clear saved_at
#                 history.saved_at = None 
#             history.save(update_fields=['is_saved', 'saved_at'])

#         return history


# class CodeRunSerializer(serializers.ModelSerializer):
#     user = UserMinimalSerializer(read_only=True) # <--- IMPORTANT CHANGE
#     snippet = serializers.PrimaryKeyRelatedField(
#         queryset=CodeSnippet.objects.all(),
#         write_only=True
#     )

#     class Meta:
#         model = CodeRun
#         fields = [
#             'id',
#             'user',
#             'snippet',
#             'run_at',
#             'was_modified',
#             'execution_time',
#             'user_agent',
#             'ip_address'
#         ]
#         read_only_fields = ['id', 'user', 'run_at', 'ip_address']

#     def create(self, validated_data):
#         """Auto-set user, IP, and user agent"""
#         request = self.context.get('request')
#         if request:
#             validated_data['user'] = request.user if request.user.is_authenticated else None
#             validated_data['ip_address'] = request.META.get('REMOTE_ADDR')
#             validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT')
#         return super().create(validated_data)

# # ==================== OPTIMIZED LIST SERIALIZERS ====================

# class CodeSnippetListSerializer(DynamicFieldsModelSerializer):
#     """Lightweight serializer for list views"""
#     url = serializers.HyperlinkedIdentityField(
#         view_name='snippet-detail',
#         lookup_field='slug'
#     )
#     language_display = serializers.CharField(
#         source='get_language_display',
#         read_only=True
#     )
#     category_name = serializers.CharField(source='category.name', read_only=True) # Ensure category name is available
#     uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True) # Ensure uploaded_by username is available
#     reaction_stats = serializers.SerializerMethodField()
#     comment_count = serializers.IntegerField(read_only=True) # Assuming 'comment_count' is a property on the model or annotated in queryset


#     class Meta:
#         model = CodeSnippet
#         fields = [
#             'id',
#             'title',
#             'slug',
#             'url',
#             'short_description',
#             'language',
#             'language_display',
#             'thumbnail_image',
#             'is_featured',
#             'created_at',
#             'reaction_stats',
#             'comment_count',
#             'category_name', # Use category_name instead of category_detail
#             'uploaded_by_username',
#             'difficulty' # Include difficulty for list view filtering/display
#         ]
#         read_only_fields = [
#             'id', 'slug', 'url', 'language_display', 'created_at',
#             'reaction_stats', 'comment_count', 'category_name', 'uploaded_by_username'
#         ]

#     def get_reaction_stats(self, obj):
#         return {
#             'likes': obj.reactions.filter(is_like=True).count(),
#             'dislikes': obj.reactions.filter(is_like=False).count()
#         }

# class CategoryWithSnippetsSerializer(CategorySerializer):
#     """Includes nested snippets for category detail views"""
#     snippets = CodeSnippetListSerializer(many=True, read_only=True)

#     class Meta(CategorySerializer.Meta):
#         fields = CategorySerializer.Meta.fields + ['snippets']






















# codehub/serializers.py

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse
from .models import (
    Category,
    CodeSnippet,
    Reaction,
    Comment,
    ShareActivity,
    UserHistory,
    CodeRun
)
# Import UserMinimalSerializer from your user_account app
from user_account.serializers import UserMinimalSerializer 
from django.utils import timezone
from django.db.models import F
from user_account.models import CustomUser


# Add this near the top of your serializers.py
class CodeSnippetFilterSerializer(serializers.Serializer):
    """Serializes filter parameters for API documentation"""
    q = serializers.CharField(required=False, help_text="Search term (title, description, code, tags)")
    language = serializers.CharField(required=False, help_text="Filter by programming language")
    difficulty = serializers.IntegerField(required=False, min_value=1, max_value=3, help_text="Filter by difficulty level (1-3)")
    category = serializers.CharField(required=False, help_text="Filter by category slug")
    output_type = serializers.CharField(required=False, help_text="Filter by output type")
    is_featured = serializers.BooleanField(required=False, help_text="Filter featured snippets")
    tags = serializers.CharField(required=False, help_text="Comma-separated tags to filter by")
    ordering = serializers.CharField(required=False, help_text="Ordering (-created_at, title, etc.)")
    

# ==================== UTILITY SERIALIZERS ====================

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

# Removed the old UserSerializer definition from here.
# It is now replaced by UserMinimalSerializer imported from user_account.serializers.

# ==================== MAIN SERIALIZERS ====================

class CategorySerializer(DynamicFieldsModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='category-detail',
        lookup_field='slug'
    )
    snippet_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'snippet_count',
            'created_at',
            'updated_at',
            'url'
        ]
        extra_kwargs = {
            'slug': {'read_only': True}
        }

    def validate_name(self, value):
        """Ensure category name is unique"""
        if self.instance and Category.objects.filter(name=value).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A category with this name already exists.")
        return value

    def create(self, validated_data):
        """Auto-generate slug on creation (though model pre_save also handles)"""
        if 'name' in validated_data and not validated_data.get('slug'):
            validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class CodeSnippetSerializer(DynamicFieldsModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='snippet-detail',
        lookup_field='slug'
    )
    language_display = serializers.CharField(
        source='get_language_display',
        read_only=True
    )
    difficulty_display = serializers.CharField(
        source='get_difficulty_display',
        read_only=True
    )
    output_type_display = serializers.CharField(
        source='get_output_type_display',
        read_only=True
    )
    # Use the imported UserMinimalSerializer here
    uploaded_by = UserMinimalSerializer(read_only=True) 
    category = CategorySerializer(read_only=True) # Nested read-only category detail
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=True # Category is required for snippet creation
    )
    reaction_stats = serializers.SerializerMethodField()
    comment_count = serializers.IntegerField(read_only=True)
    share_count = serializers.IntegerField(read_only=True)
    user_has_reacted = serializers.SerializerMethodField()
    user_history = serializers.SerializerMethodField()

    class Meta:
        model = CodeSnippet
        fields = [
            # Core fields
            'id', 'title', 'slug', 'url',
            'description', 'short_description',
            
            # Categorization
            'language', 'language_display',
            'output_type', 'output_type_display',
            'difficulty', 'difficulty_display',
            'category', 'category_id', 'tags',
            
            # Code content
            'code_content', 'html_code', 'css_code', 'js_code', 'additional_files',
            
            # Simulation
            'simulated_output', 'expected_result',
            
            # Presentation
            'thumbnail_image', 'is_featured',
            
            # Ownership
            'uploaded_by', 'created_at', 'updated_at', 'last_accessed',
            
            # Stats
            'reaction_stats', 'comment_count', 'share_count',
            'user_has_reacted', 'user_history'
        ]
        extra_kwargs = {
            'slug': {'read_only': True},
            'code_content': {'required': False}, 
            'simulated_output': {'write_only': True}, # Make simulated_output write-only for creation/update
            'category': {'read_only': True}, # Ensure category object is read-only
            'category_id': {'write_only': True} # Ensure category_id is write-only for submission
        }

    def get_reaction_stats(self, obj):
        """Calculate like/dislike counts"""
        return {
            'likes': obj.reactions.filter(is_like=True).count(),
            'dislikes': obj.reactions.filter(is_like=False).count()
        }

    def get_user_has_reacted(self, obj):
        """Check if current user has reacted"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            reaction = obj.reactions.filter(user=request.user).first()
            if reaction:
                return 'like' if reaction.is_like else 'dislike'
        return None

    def get_user_history(self, obj):
        """Get user-specific interaction data"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            history = obj.user_history.filter(user=request.user).first()
            if history:
                return {
                    'view_count': history.view_count,
                    'is_saved': history.is_saved,
                    'last_viewed': history.last_viewed
                }
        return None
    
    def validate(self, data):
        """
        Custom validation for code content based on language type and category presence.
        """
        # For updates, get existing instance language if not provided in data
        language = data.get('language', self.instance.language if self.instance else None)
        
        # Category validation for creation
        if not self.instance and 'category' not in data and 'category_id' not in data:
            raise serializers.ValidationError({
                'category_id': 'This field is required for new snippets.'
            })
            
        # Ensure required code fields are present based on language
        if language in ['html', 'css', 'javascript']:
            if not any(data.get(field) for field in ['html_code', 'css_code', 'js_code', 'code_content']):
                raise ValidationError({
                    'code': 'Web snippets require at least one code field (html_code, css_code, js_code or code_content).'
                })
        
        elif language in ['python', 'java', 'cpp', 'csharp', 'go', 'rust', 'django', 'nodejs']: # Added more console/backend languages
            if not data.get('code_content'):
                raise serializers.ValidationError({
                    'code_content': f'{language.capitalize()} snippets require code_content.'
                })
        
        return data

    def create(self, validated_data):
        """Auto-set uploaded_by"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['uploaded_by'] = request.user
        
        # Slug generation is handled by the CodeSnippet model's pre_save signal.
        # No need to set validated_data['slug'] here.

        return super().create(validated_data)


class ReactionSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True) 
    snippet = serializers.PrimaryKeyRelatedField(
        queryset=CodeSnippet.objects.all(),
        write_only=True
    )

    class Meta:
        model = Reaction
        fields = ['id', 'user', 'snippet', 'is_like', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        """Ensure one reaction per user per snippet"""
        request = self.context.get('request')
        snippet = data.get('snippet')
        
        if request and request.user.is_authenticated:
            if Reaction.objects.filter(user=request.user, snippet=snippet).exists():
                # For updates, allow modifying existing reaction
                if self.instance and self.instance.user == request.user and self.instance.snippet == snippet:
                    return data
                raise ValidationError("You've already reacted to this snippet.")
        
        return data

    def create(self, validated_data):
        """Auto-set user from request"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
    
    

# class CommentSerializer(DynamicFieldsModelSerializer):
#     user = UserMinimalSerializer(read_only=True) 
#     snippet = serializers.PrimaryKeyRelatedField(
#         queryset=CodeSnippet.objects.all(),
#         write_only=True,
#         required=False
#     )
#     parent = serializers.PrimaryKeyRelatedField(
#         queryset=Comment.objects.all(),
#         required=False,
#         allow_null=True # Allow null for top-level comments
#     )
#     replies = serializers.SerializerMethodField()
#     user_vote = serializers.SerializerMethodField()

#     class Meta:
#         model = Comment
#         fields = [
#             'id',
#             'user',
#             'snippet',
#             'parent',
#             'text', # Assuming your Comment model has a 'text' field for content
#             'is_resolved',
#             'created_at',
#             'updated_at',
#             'replies',
#             'user_vote'
#         ]
#         read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'replies']

#     def get_replies(self, obj):
#         """Nested replies if they exist"""
#         if obj.replies.exists():
#             # Use self.__class__ for recursive serializer reference
#             return self.__class__(
#                 obj.replies.all(),
#                 many=True,
#                 context=self.context,
#                 fields=['id', 'user', 'text', 'created_at', 'parent'] # Added parent field for clarity in replies
#             ).data
#         return []

#     def get_user_vote(self, obj):
#         """Check if current user has voted on this comment (Placeholder)"""
#         # Implement if you add comment voting later
#         return None

#     def validate(self, data):
#         """Ensure either snippet or parent is set"""
#         if not data.get('snippet') and not data.get('parent'):
#             raise ValidationError("A comment must be associated with either a snippet or a parent comment.")
        
#         # If parent is provided, ensure snippet is not simultaneously provided
#         if data.get('parent') and data.get('snippet'):
#             raise ValidationError("A comment cannot be both a top-level comment and a reply simultaneously. Provide either 'snippet' or 'parent'.")
        
#         return data




class UserMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for user information in nested contexts.
    """
    class Meta:
        model = CustomUser # Assuming CustomUser is your user model
        fields = ['id', 'email', 'username'] 
        read_only_fields = ['id', 'email', 'username']

class CommentSerializer(DynamicFieldsModelSerializer): # Or serializers.ModelSerializer if DynamicFieldsModelSerializer is not used
    """
    Serializer for the Comment model.
    Handles both main comments and nested replies.
    """
    user = UserMinimalSerializer(read_only=True)
    
    # 'snippet' is now removed as a directly writable field for client input.
    # It will be set by the view's perform_create method based on the URL context or parent comment.
    
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        required=False, # Allow null for top-level comments
        allow_null=True # Explicitly allow null
    )
    
    replies = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField() # Placeholder for future voting feature

    class Meta:
        model = Comment
        # 'snippet' is removed from fields because it's no longer provided directly by the client's request body
        fields = [
            'id', 'user', 'parent', 'text', 'is_resolved', 
            'created_at', 'updated_at', 'replies', 'user_vote'
        ]
        # 'is_resolved' is typically not read-only so it can be updated
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'replies', 'user_vote'] 

    def get_replies(self, obj):
        """
        Nested replies if they exist.
        Uses self.__class__ for recursive serializer reference.
        """
        if obj.replies.exists():
            return self.__class__(
                obj.replies.all(),
                many=True,
                context=self.context, # Pass context for nested serializers
                # Ensure 'snippet' is included here for completeness when reading replies
                fields=['id', 'user', 'text', 'created_at', 'parent', 'snippet'] 
            ).data
        return []

    def get_user_vote(self, obj):
        """
        Placeholder method to check if the current user has voted on this comment.
        Implement if you add comment voting later.
        """
        return None
    
    
    
    

class ShareActivitySerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True) 
    snippet = serializers.PrimaryKeyRelatedField(
        queryset=CodeSnippet.objects.all(),
        write_only=True
    )
    share_method_display = serializers.CharField(
        source='get_share_method_display',
        read_only=True
    )

    class Meta:
        model = ShareActivity
        fields = [
            'id',
            'user',
            'snippet',
            'share_method',
            'share_method_display',
            'shared_to',
            'shared_at',
            'ip_address'
        ]
        read_only_fields = ['id', 'user', 'shared_at', 'ip_address']

    def create(self, validated_data):
        """Auto-set user and IP address"""
        request = self.context.get('request')
        if request:
            validated_data['user'] = request.user if request.user.is_authenticated else None
            validated_data['ip_address'] = request.META.get('REMOTE_ADDR')
        return super().create(validated_data)

class UserHistorySerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True) 
    snippet = CodeSnippetSerializer(read_only=True, fields=['id', 'title', 'slug']) # Only show relevant snippet fields
    snippet_id = serializers.PrimaryKeyRelatedField(
        queryset=CodeSnippet.objects.all(),
        source='snippet',
        write_only=True
    )

    class Meta:
        model = UserHistory
        fields = [
            'id',
            'user',
            'snippet',
            'snippet_id',
            'last_viewed',
            'view_count',
            'is_saved',
            'saved_at'
        ]
        read_only_fields = ['id', 'user', 'last_viewed', 'view_count']

    def update(self, instance, validated_data):
        """Handle incrementing view count and saving"""
        if 'is_saved' in validated_data:
            instance.is_saved = validated_data['is_saved']
            if validated_data['is_saved'] and not instance.saved_at:
                instance.saved_at = timezone.now()
            elif not validated_data['is_saved'] and instance.saved_at: # If unsaved, clear saved_at
                instance.saved_at = None 
            instance.save(update_fields=['is_saved', 'view_count', 'last_viewed', 'saved_at'])
        
        # Always increment view count on update and update last_viewed
        instance.view_count = F('view_count') + 1
        instance.last_viewed = timezone.now() 
        instance.save(update_fields=['view_count', 'last_viewed'])

        instance.refresh_from_db()
        return instance

    def create(self, validated_data):
        """Create or update user history"""
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        snippet = validated_data['snippet']

        # Check if history already exists for this user and snippet
        history, created = UserHistory.objects.get_or_create(
            user=user,
            snippet=snippet,
            defaults={'view_count': 1, 'last_viewed': timezone.now()}
        )
        if not created:
            # If exists, update view count and last viewed
            history.view_count = F('view_count') + 1
            history.last_viewed = timezone.now()
            history.save(update_fields=['view_count', 'last_viewed'])
            history.refresh_from_db()

        if 'is_saved' in validated_data:
            history.is_saved = validated_data['is_saved']
            if validated_data['is_saved'] and not history.saved_at:
                history.saved_at = timezone.now()
            elif not validated_data['is_saved'] and history.saved_at: # If unsaved, clear saved_at
                history.saved_at = None 
            history.save(update_fields=['is_saved', 'saved_at'])

        return history


class CodeRunSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True) 
    snippet = serializers.PrimaryKeyRelatedField(
        queryset=CodeSnippet.objects.all(),
        write_only=True
    )

    class Meta:
        model = CodeRun
        fields = [
            'id',
            'user',
            'snippet',
            'run_at',
            'was_modified',
            'execution_time',
            'user_agent',
            'ip_address'
        ]
        read_only_fields = ['id', 'user', 'run_at', 'ip_address']

    def create(self, validated_data):
        """Auto-set user, IP, and user agent"""
        request = self.context.get('request')
        if request:
            validated_data['user'] = request.user if request.user.is_authenticated else None
            validated_data['ip_address'] = request.META.get('REMOTE_ADDR')
            validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT')
        return super().create(validated_data)

# ==================== OPTIMIZED LIST SERIALIZERS ====================

class CodeSnippetListSerializer(DynamicFieldsModelSerializer):
    """Lightweight serializer for list views"""
    url = serializers.HyperlinkedIdentityField(
        view_name='snippet-detail',
        lookup_field='slug'
    )
    language_display = serializers.CharField(
        source='get_language_display',
        read_only=True
    )
    output_type_display = serializers.CharField( # <--- Added
        source='get_output_type_display',
        read_only=True
    )
    category_name = serializers.CharField(source='category.name', read_only=True) 
    uploaded_by = UserMinimalSerializer(read_only=True) # <--- Changed to full UserMinimalSerializer
    reaction_stats = serializers.SerializerMethodField()
    comment_count = serializers.IntegerField(read_only=True) 
    user_has_reacted = serializers.SerializerMethodField() # <--- Added
    user_history = serializers.SerializerMethodField() # <--- Added


    class Meta:
        model = CodeSnippet
        fields = [
            'id',
            'title',
            'slug',
            'url',
            'description', # <--- Added
            'short_description',
            'language',
            'language_display',
            'output_type', # <--- Added
            'output_type_display', # <--- Added
            'difficulty', 
            'thumbnail_image',
            'is_featured',
            'tags', # <--- Added
            'created_at',
            'updated_at', # <--- Added
            'last_accessed', # <--- Added
            'reaction_stats',
            'comment_count', 
            'category_name', 
            'uploaded_by', # <--- Changed
            'user_has_reacted', # <--- Added
            'user_history' # <--- Added
        ]
        read_only_fields = [
            'id', 'slug', 'url', 'language_display', 'output_type_display',
            'created_at', 'updated_at', 'last_accessed',
            'reaction_stats', 'comment_count', 'category_name', 
            'uploaded_by', 'user_has_reacted', 'user_history'
        ]
    
    def get_reaction_stats(self, obj):
        """Calculate like/dislike counts (copied from CodeSnippetSerializer)"""
        return {
            'likes': obj.reactions.filter(is_like=True).count(),
            'dislikes': obj.reactions.filter(is_like=False).count()
        }

    def get_user_has_reacted(self, obj):
        """Check if current user has reacted (copied from CodeSnippetSerializer)"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            reaction = obj.reactions.filter(user=request.user).first()
            if reaction:
                return 'like' if reaction.is_like else 'dislike'
        return None

    def get_user_history(self, obj):
        """Get user-specific interaction data (copied from CodeSnippetSerializer)"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            history = obj.user_history.filter(user=request.user).first()
            if history:
                return {
                    'view_count': history.view_count,
                    'is_saved': history.is_saved,
                    'last_viewed': history.last_viewed
                }
        return None


class CategoryWithSnippetsSerializer(CategorySerializer):
    """Includes nested snippets for category detail views"""
    snippets = CodeSnippetListSerializer(many=True, read_only=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['snippets']