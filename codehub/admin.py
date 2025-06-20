# codehub/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Category, 
    CodeSnippet, 
    Reaction, 
    Comment, 
    ShareActivity, 
    UserHistory, 
    CodeRun
)

# Common Admin Mixins
class ReadOnlyMixin:
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

# CATEGORY ADMIN---------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'snippet_count', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    
    def snippet_count(self, obj):
        return obj.snippets.count()
    snippet_count.short_description = 'Snippets'

# CODE SNIPPET ADMIN-----------------------------------------------------------------
class ReactionInline(admin.TabularInline):
    model = Reaction
    extra = 0
    readonly_fields = ('user', 'snippet', 'is_like', 'created_at')
    can_delete = False

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'snippet', 'parent', 'created_at')
    fields = ('user', 'text', 'is_resolved', 'created_at')
    show_change_link = True

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'language_display', 
        'difficulty_display', 
        'category', 
        'uploaded_by', 
        'created_at',
        'reaction_count',
        'comment_count'
    )
    list_filter = (
        'language', 
        'difficulty', 
        'category', 
        'is_featured',
        'created_at'
    )
    search_fields = ('title', 'description', 'code_content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = (
        'created_at', 
        'updated_at', 
        'last_accessed',
        'reaction_count',
        'comment_count',
        'share_count',
        'preview_code'
    )
    fieldsets = (
        ('Metadata', {
            'fields': (
                'title', 
                'slug', 
                'description', 
                'short_description',
                'category',
                'tags'
            )
        }),
        ('Code Content', {
            'fields': (
                'language',
                'output_type',
                'code_content',
                'html_code',
                'css_code',
                'js_code',
                'additional_files',
                'preview_code'
            )
        }),
        ('Simulation & Output', {
            'fields': (
                'simulated_output',
                'expected_result',
            )
        }),
        ('Presentation', {
            'fields': (
                'thumbnail_image',
                'is_featured',
                'difficulty',
            )
        }),
        ('Statistics', {
            'fields': (
                'uploaded_by',
                'created_at',
                'updated_at',
                'last_accessed',
                'reaction_count',
                'comment_count',
                'share_count'
            )
        }),
    )
    inlines = [ReactionInline, CommentInline]
    filter_horizontal = ()
    raw_id_fields = ('uploaded_by',)
    ordering = ('-created_at',)
    
    def language_display(self, obj):
        return obj.get_language_display()
    language_display.short_description = 'Language'
    
    def difficulty_display(self, obj):
        return obj.get_difficulty_display()
    difficulty_display.short_description = 'Difficulty'
    
    def reaction_count(self, obj):
        return obj.reactions.count()
    reaction_count.short_description = 'Reactions'
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'
    
    def share_count(self, obj):
        return obj.shares.count()
    share_count.short_description = 'Shares'
    
    def preview_code(self, obj):
        if len(obj.code_content) > 100:
            preview = obj.code_content[:100] + '...'
        else:
            preview = obj.code_content
        return format_html('<pre style="max-height: 200px; overflow: auto;">{}</pre>', preview)
    preview_code.short_description = 'Code Preview'

# REACTION ADMIN---------------------------------------------------------------------
@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'snippet', 'is_like', 'created_at')
    list_filter = ('is_like', 'created_at')
    search_fields = ('user__email', 'snippet__title')
    readonly_fields = ('user', 'snippet', 'is_like', 'created_at')
    ordering = ('-created_at',)

# COMMENT ADMIN----------------------------------------------------------------------
class CommentReplyInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'snippet', 'created_at')
    fields = ('user', 'text', 'is_resolved', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'snippet', 'parent', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('user__email', 'snippet__title', 'text')
    readonly_fields = ('user', 'snippet', 'parent', 'created_at', 'updated_at')
    inlines = [CommentReplyInline]
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'snippet', 'parent')

# SHARE ACTIVITY ADMIN--------------------------------------------------------------
@admin.register(ShareActivity)
class ShareActivityAdmin(admin.ModelAdmin):
    list_display = ('snippet', 'share_method_display', 'user', 'shared_at')
    list_filter = ('share_method', 'shared_at')
    search_fields = ('snippet__title', 'user__email', 'shared_to')
    readonly_fields = ('user', 'snippet', 'share_method', 'shared_to', 'shared_at', 'ip_address')
    ordering = ('-shared_at',)
    
    def share_method_display(self, obj):
        return obj.get_share_method_display()
    share_method_display.short_description = 'Method'

# USER HISTORY ADMIN-----------------------------------------------------------------
@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'snippet', 'last_viewed', 'view_count', 'is_saved')
    list_filter = ('is_saved', 'last_viewed')
    search_fields = ('user__email', 'snippet__title')
    readonly_fields = ('user', 'snippet', 'last_viewed', 'view_count', 'saved_at')
    ordering = ('-last_viewed',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'snippet')

# CODE RUN ADMIN--------------------------------------------------------------------
@admin.register(CodeRun)
class CodeRunAdmin(admin.ModelAdmin):
    list_display = ('snippet', 'user', 'run_at', 'was_modified', 'execution_time')
    list_filter = ('was_modified', 'run_at')
    search_fields = ('snippet__title', 'user__email')
    readonly_fields = ('user', 'snippet', 'run_at', 'was_modified', 'execution_time', 'user_agent', 'ip_address')
    ordering = ('-run_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'snippet')