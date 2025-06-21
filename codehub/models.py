
# codehub/models.py

import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from user_account.models import CustomUser
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .services.snippet_services import generate_snippet_slug


DIFFICULTY_LEVELS = (
    (1, 'Beginner'),
    (2, 'Intermediate'),
    (3, 'Advanced'),
)



# CATEGORY-----------------------------------------------------------------------------
class Category(models.Model):
    """
    Organizes code snippets into customizable categories (CRUD enabled for admins)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        # Ensure slug is unique, though unique=True in model helps
        original_slug = instance.slug
        num = 1
        while Category.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{original_slug}-{num}"
            num += 1
            
# class Category(models.Model):
#     """
#     Organizes code snippets into customizable categories (CRUD enabled for admins)
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100, unique=True)
#     slug = models.SlugField(max_length=100, unique=True, blank=True)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = "Categories"
#         ordering = ['name']

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('category-detail', kwargs={'slug': self.slug})


# @receiver(pre_save, sender=Category)
# def category_pre_save(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.name)


# CODE SNIPPET-----------------------------------------------------------------------------
class CodeSnippet(models.Model):
    """
    Represents a single code snippet with metadata and content.
    """
    LANGUAGE_CHOICES = [
        ("python", "Python"),
        ("javascript", "JavaScript"),
        ("typescript", "TypeScript"),
        ("html", "HTML"),
        ("css", "CSS"),
        ("nodejs", "Node.js"),
        ("java", "Java"),
        ("csharp", "C#"),
        ("cpp", "C++"),
        ("cee", "C"),
        ("go", "Go"),
        ("rust", "Rust"),
        ("django", "Django"),
        ("react", "React"),
        ("other", "Other"),
    ]

    OUTPUT_TYPE_CHOICES = [
        ("console", "Console Output"),
        ("browser", "Browser Preview"),
        ("api", "API Output"),
        ("other", "Other Output"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=160, blank=True)
    tags = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated tags (e.g. python,api,beginner)"
    )
    language = models.CharField(
        max_length=50, choices=LANGUAGE_CHOICES, default="python"
    )
    output_type = models.CharField(
        max_length=20, choices=OUTPUT_TYPE_CHOICES, default="console"
    )
    code_content = models.TextField(
        help_text="Main code content (can be combined or single-file)"
    )
    html_code = models.TextField(blank=True, null=True)
    css_code = models.TextField(blank=True, null=True)
    js_code = models.TextField(blank=True, null=True)
    additional_files = models.JSONField(
        blank=True, null=True, help_text="JSON structure for multi-file projects"
    )
    simulated_output = models.TextField(
        blank=True, null=True, help_text="Expected output for console-based snippets"
    )
    expected_result = models.TextField(
        blank=True, null=True, help_text="For tutorials - what the user should achieve"
    )
    thumbnail_image = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    difficulty = models.PositiveSmallIntegerField(
        choices=DIFFICULTY_LEVELS, default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="snippets",
        blank=True,
        null=True,
    )
    uploaded_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="uploaded_snippets", null=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['language']),
            models.Index(fields=['output_type']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['title']),
            models.Index(fields=['tags']),
        ]

    def __str__(self):
        return self.title

@receiver(pre_save, sender=CodeSnippet)
def codesnippet_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug or (instance.pk and sender.objects.filter(pk=instance.pk, title=instance.title).first() is None):
        # Generate slug only if it's new or title has changed
        instance.slug = generate_snippet_slug(instance.title, instance.pk)
    # Ensure all CodeSnippet slug are unique by excluding the current instance
    elif instance.slug:
        # If slug is provided or already exists, ensure it's still unique
        instance.slug = generate_snippet_slug(instance.title, instance.pk)
        
# class CodeSnippet(models.Model):
#     """
#     Core model for storing code tutorials and mini-apps with simulation support
#     """
#     class OutputType(models.TextChoices):
#         CONSOLE = 'console', 'Console Output'
#         BROWSER = 'browser', 'Browser Preview'
#         API = 'api', 'API Output'
#         OTHER = 'other', 'Other Output'

#     class Language(models.TextChoices):
#         PYTHON = 'python', 'Python'
#         JAVASCRIPT = 'javascript', 'JavaScript'
#         TYPESCRIPT = 'typescript', 'TypeScript'
#         HTML = 'html', 'HTML'
#         CSS = 'css', 'CSS'
#         NODEJS = 'nodejs', 'Node.js'
#         JAVA = 'java', 'Java'
#         CSHARP = 'csharp', 'C#'
#         CPP = 'cpp', 'C++'
#         CEE = 'cee', 'C'
#         GO = 'go', 'Go'
#         RUST = 'rust', 'Rust'
#         DJANGO = 'django', 'Django'
#         REACT = 'react', 'React'
#         OTHER = 'other', 'Other'

#     # Core Metadata
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255)
#     slug = models.SlugField(max_length=255, unique=True, blank=True)
#     description = models.TextField()
#     short_description = models.CharField(max_length=160, blank=True)
#     category = models.ForeignKey(
#         Category, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True,
#         related_name='snippets'
#     )
#     tags = models.CharField(
#     max_length=255,
#     blank=True,
#     help_text="Comma-separated tags (e.g. python,api,beginner)"
# )

#     # Code Content
#     language = models.CharField(
#         max_length=50,
#         choices=Language.choices,
#         default=Language.PYTHON
#     )
#     output_type = models.CharField(
#         max_length=20,
#         choices=OutputType.choices,
#         default=OutputType.CONSOLE
#     )
#     code_content = models.TextField(
#         help_text="Main code content (can be combined or single-file)"
#     )
#     html_code = models.TextField(blank=True, null=True)
#     css_code = models.TextField(blank=True, null=True)
#     js_code = models.TextField(blank=True, null=True)
#     additional_files = models.JSONField(
#         blank=True, 
#         null=True,
#         help_text="JSON structure for multi-file projects"
#     )

#     # Simulation & Output
#     simulated_output = models.TextField(
#         blank=True, 
#         null=True,
#         help_text="Expected output for console-based snippets"
#     )
#     expected_result = models.TextField(
#         blank=True, 
#         null=True,
#         help_text="For tutorials - what the user should achieve"
#     )

#     # Media & Presentation
#     thumbnail_image = models.URLField(blank=True, null=True)
#     is_featured = models.BooleanField(default=False)
#     difficulty = models.PositiveSmallIntegerField(
#         default=1,
#         choices=DIFFICULTY_LEVELS
#     )

#     # Ownership & Timestamps
#     uploaded_by = models.ForeignKey(
#         CustomUser,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='uploaded_snippets'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     last_accessed = models.DateTimeField(null=True, blank=True)

#     class Meta:
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['-created_at']),
#             models.Index(fields=['language']),
#             models.Index(fields=['output_type']),
#             models.Index(fields=['difficulty']),
#             models.Index(fields=['is_featured']),
#             models.Index(fields=['title']),  # For faster title searches
#             models.Index(fields=['tags']),   # For tag filtering
#         ]

#     def __str__(self):
#         return f"{self.title} ({self.get_language_display()})"

#     def get_absolute_url(self):
#         return reverse('snippet-detail', kwargs={'slug': self.slug})

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(f"{self.title}-{str(self.id)[:8]}")
#         if not self.short_description and self.description:
#             self.short_description = self.description[:160]
#         super().save(*args, **kwargs)


# REACTION-----------------------------------------------------------------------------
class Reaction(models.Model):
    """
    Tracks user likes/dislikes on code snippets (one per user per snippet)
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    snippet = models.ForeignKey(
        CodeSnippet,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'snippet')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} {'liked' if self.is_like else 'disliked'} {self.snippet.title}"


# COMMENTS-----------------------------------------------------------------------------
class Comment(models.Model):
    """
    User comments on code snippets with threaded replies support
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    snippet = models.ForeignKey(
        CodeSnippet,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    text = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.email} on {self.snippet.title}"


# SHARE-----------------------------------------------------------------------------
class ShareActivity(models.Model):
    """
    Tracks when users share code snippets
    """
    class ShareMethod(models.TextChoices):
        LINK = 'link', 'Link'
        EMAIL = 'email', 'Email'
        SOCIAL = 'social', 'Social Media'

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shares'
    )
    snippet = models.ForeignKey(
        CodeSnippet,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    share_method = models.CharField(
        max_length=20,
        choices=ShareMethod.choices,
        default=ShareMethod.LINK
    )
    shared_to = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Email or platform shared to"
    )
    shared_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Share Activities"
        ordering = ['-shared_at']

    def __str__(self):
        return f"{self.snippet.title} shared via {self.get_share_method_display()}"
    


# USERHISTORY-----------------------------------------------------------------------------
class UserHistory(models.Model):
    """
    Tracks user interaction with code snippets (viewing, saving)
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='code_history'
    )
    snippet = models.ForeignKey(
        CodeSnippet,
        on_delete=models.CASCADE,
        related_name='user_history'
    )
    last_viewed = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=1)
    is_saved = models.BooleanField(default=False)
    saved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "User Histories"
        unique_together = ('user', 'snippet')
        ordering = ['-last_viewed']

    def __str__(self):
        return f"{self.user.email}'s history with {self.snippet.title}"



# RUN CODE-----------------------------------------------------------------------------
class CodeRun(models.Model):
    """
    Optional: Tracks when users run code simulations (for analytics)
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='code_runs'
    )
    snippet = models.ForeignKey(
        CodeSnippet,
        on_delete=models.CASCADE,
        related_name='runs'
    )
    run_at = models.DateTimeField(auto_now_add=True)
    was_modified = models.BooleanField(default=False)
    execution_time = models.FloatField(
        null=True,
        blank=True,
        help_text="Client-reported execution time in ms"
    )
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ['-run_at']

    def __str__(self):
        return f"Run of {self.snippet.title} by {self.user.email if self.user else 'anonymous'}"