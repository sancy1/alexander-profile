
# contact/services.copy()

from .models import Contact, NewsletterSubscriber, DeletedSubscriber
from .serializers import ContactSerializer, NewsletterSubscriberSerializer, DeletedSubscriberSerializer
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from smtplib import SMTPException
import sys
import logging
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import premailer # Import premailer
from django.core.mail import send_mail, EmailMultiAlternatives

logger = logging.getLogger(__name__)

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class ContactService:
    @staticmethod
    def get_base_url():
        """Safe way to get base URL with fallback"""
        try:
            from django.conf import settings
            protocol = getattr(settings, 'SITE_PROTOCOL', 'http')
            domain = getattr(settings, 'SITE_DOMAIN', 'localhost:8000')
            return f"{protocol}://{domain}"
        except Exception:
            return "http://localhost:8000"  # Default fallback

    @staticmethod
    def create_contact(data, request=None):
        print("\n=== Starting contact creation process ===")
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            contact = serializer.save()
            
            # Send detailed email notification
            if settings.EMAIL_HOST_USER:
                base_url = ContactService.get_base_url()
                admin_url = f"{base_url}/admin/contact/{contact.id}/"
                api_url = f"{base_url}/api/contacts/{contact.id}/"
                
                email_subject = f"NEW CONTACT: {contact.subject} (ID: {contact.id})"
                email_message = f"""
                =============================
                COMPLETE CONTACT SUBMISSION
                =============================
                
                Submission ID: {contact.id}
                Received at: {contact.created_at.strftime("%Y-%m-%d %H:%M:%S")}
                
                CONTACT DETAILS
                Name: {contact.name}
                Email: {contact.email}
                Phone: {contact.phone or 'Not provided'}
                Subject: {contact.subject}
                
                MESSAGE
                {contact.message}
                
                ADMIN ACTIONS
                View in Dashboard: {admin_url}
                API Endpoint: {api_url}
                
                =============================
                This is a complete copy for your records.
                =============================
                """
                
                try:
                    send_mail(
                        subject=email_subject,
                        message=email_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=False,
                    )
                    logger.info(f"Full contact details emailed for ID: {contact.id}")
                except Exception as e:
                    logger.error(f"Error sending contact email: {str(e)}")
            
            return contact
        raise ValidationError(serializer.errors)
    

    # READ operations
    @staticmethod
    def get_all_contacts():
        """Retrieve all contact submissions ordered by creation date (newest first)"""
        print("\n=== Retrieving all contacts ===")
        contacts = Contact.objects.all().order_by('-created_at')
        print(f"Found {contacts.count()} contacts")
        return contacts

    @staticmethod
    def get_contact_detail(pk):
        """Retrieve a single contact submission by ID"""
        print(f"\n=== Retrieving contact detail for ID: {pk} ===")
        try:
            contact = Contact.objects.get(pk=pk)
            print(f"Found contact: {contact.email}")
            return contact
        except ObjectDoesNotExist:
            print(f"Contact with ID {pk} not found")
            return None

    # UPDATE operation
    @staticmethod
    def update_contact(pk, data):
        """Update a contact submission"""
        print(f"\n=== Updating contact ID: {pk} ===")
        try:
            contact = Contact.objects.get(pk=pk)
            print(f"Found contact to update: {contact.email}")
            
            serializer = ContactSerializer(contact, data=data, partial=True)
            if serializer.is_valid():
                updated_contact = serializer.save()
                print("Contact updated successfully")
                return updated_contact
            else:
                print("Validation errors during update:")
                print(serializer.errors)
                raise ValidationError(serializer.errors)
        except ObjectDoesNotExist:
            print(f"Contact with ID {pk} not found")
            return None

    # DELETE operation
    @staticmethod
    def delete_contact(pk):
        """Delete a contact submission"""
        print(f"\n=== Deleting contact ID: {pk} ===")
        try:
            contact = Contact.objects.get(pk=pk)
            print(f"Found contact to delete: {contact.email}")
            contact.delete()
            print("Contact deleted successfully")
            return True
        except ObjectDoesNotExist:
            print(f"Contact with ID {pk} not found")
            return False






# # NEWSLETTER --------------------------------------------------------------------------------------
# class NewsletterService:
#     @staticmethod
#     def get_unsubscribe_url(email):
#         """Generate unsubscribe link with email parameter"""
#         try:
#             frontend_url = getattr(settings, 'FRONTEND_URL', None)
#             if frontend_url:
#                 return f"{frontend_url}/unsubscribe/?email={email}"
#             # Fallback to backend URL if frontend URL is not set
#             return f"{ContactService.get_base_url()}/api/newsletter/unsubscribe/?email={email}"
#         except Exception as e:
#             logger.error(f"Error generating unsubscribe URL: {str(e)}")
#             return f"http://yourdomain.com/unsubscribe/?email={email}"  # Hardcoded fallback

#     @staticmethod
#     def subscribe_email(data):
#         email = data.get('email')
#         if not email:
#             raise ValidationError({'email': 'This field is required.'})

#         try:
#             # Check if email is already an active subscriber
#             if NewsletterSubscriber.objects.filter(email=email).exists():
#                 raise ValidationError({'email': 'This email is already an active subscriber.'})

#             # If email exists in deleted, remove it from there first for re-subscription
#             deleted_sub = DeletedSubscriber.objects.filter(email=email).first()
#             if deleted_sub:
#                 deleted_sub.delete()
#                 logger.info(f"Removed {email} from deleted subscribers for re-subscription.")

#             # Create new active subscriber
#             # The 'is_active=True' is fine here, assuming your model has it.
#             # However, if NewsletterSubscriber represents *only* active subscribers (as implied by the move-to-deleted logic),
#             # the is_active field could potentially be removed from this model in favor of relying on presence/absence.
#             # For now, keeping it as it was in your working code.
#             subscriber = NewsletterSubscriber.objects.create(email=email, is_active=True)
#             logger.info(f"New active newsletter subscriber created: {email}")

#             # Send emails
#             if settings.EMAIL_HOST_USER: # Only attempt to send if EMAIL_HOST_USER is configured
#                 unsubscribe_url = NewsletterService.get_unsubscribe_url(email)

#                 # 1. Send welcome email to subscriber
#                 subscriber_message = f"""Thank you for subscribing to our newsletter!

# You will now receive updates from us.

# To unsubscribe at any time, click here:
# {unsubscribe_url}
# """
#                 send_mail(
#                     subject="Welcome to Our Newsletter!",
#                     message=subscriber_message,
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[email],
#                     fail_silently=False,
#                 )
#                 logger.info(f"Welcome email sent to {email}")

#                 # 2. Send notification to admin
#                 admin_message = f"""New newsletter subscription:

# Email: {email}
# Date: {subscriber.subscribed_at.strftime("%Y-%m-%d %H:%M:%S")}

# Current active subscribers: {NewsletterSubscriber.objects.filter(is_active=True).count()}
# """
#                 send_mail(
#                     subject=f"New Newsletter Subscriber: {email}",
#                     message=admin_message,
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[settings.ADMIN_EMAIL],
#                     fail_silently=False,
#                 )
#                 logger.info(f"Admin notification sent for new subscriber {email}")

#             return subscriber

#         except ValidationError: # Re-raise DRF ValidationErrors directly
#             raise
#         except Exception as e:
#             logger.error(f"Error in newsletter subscription for {email}: {str(e)}", exc_info=True)
#             raise ValidationError({'error': 'An internal error occurred during subscription.'})
        
#     @staticmethod
#     def unsubscribe_email(email):
#         """
#         Handles unsubscription: Moves subscriber to DeletedSubscriber table.
#         Returns tuple: (success: bool, message: str)
#         """
#         if not email:
#             return False, "Email is required"

#         try:
#             subscriber = NewsletterSubscriber.objects.get(email=email)

#             # Create entry in DeletedSubscriber
#             DeletedSubscriber.objects.create(
#                 email=subscriber.email,
#                 unsubscribed_at=timezone.now() # Use current time for unsubscribed_at
#             )
#             logger.info(f"Moved {email} to DeletedSubscriber table.")

#             # Delete from active NewsletterSubscriber table
#             # This is the key line to remove it from the active list
#             subscriber.delete() 
#             logger.info(f"Deleted {email} from active NewsletterSubscriber table.")

#             # Send confirmation email
#             if settings.EMAIL_HOST_USER:
#                 try:
#                     send_mail(
#                         subject="You've been unsubscribed",
#                         message="You have been successfully unsubscribed from our newsletter. We're sad to see you go!",
#                         from_email=settings.DEFAULT_FROM_EMAIL,
#                         recipient_list=[email],
#                         fail_silently=False,
#                     )
#                     logger.info(f"Unsubscribe confirmation email sent to {email}")
#                 except Exception as e:
#                     logger.error(f"Failed to send unsubscribe confirmation to {email}: {str(e)}", exc_info=True)

#             return True, "Successfully unsubscribed"

#         except NewsletterSubscriber.DoesNotExist:
#             # Check if it's already in DeletedSubscriber
#             if DeletedSubscriber.objects.filter(email=email).exists():
#                 return False, "This email was already unsubscribed."
#             logger.warning(f"Unsubscribe attempt for non-existent or already deleted email: {email}")
#             return False, "Email not found in our active subscription list."
#         except Exception as e:
#             logger.error(f"Error unsubscribing {email}: {str(e)}", exc_info=True)
#             return False, "An error occurred while processing your request."
    
#     @staticmethod
#     def get_all_subscribers():
#         # This will now only return truly active subscribers (those not deleted)
#         return NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    
#     @staticmethod
#     def get_subscriber_detail(pk):
#         try:
#             return NewsletterSubscriber.objects.get(pk=pk)
#         except ObjectDoesNotExist:
#             return None
    
#     @staticmethod
#     def update_subscriber(pk, data):
#         try:
#             subscriber = NewsletterSubscriber.objects.get(pk=pk)
#             serializer = NewsletterSubscriberSerializer(subscriber, data=data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return serializer.data
#             raise ValidationError(serializer.errors)
#         except ObjectDoesNotExist:
#             return None
    
#     @staticmethod
#     def delete_subscriber(pk):
#         # This method directly deletes from NewsletterSubscriber, 
#         # it doesn't move to DeletedSubscriber. Use unsubscribe_email for standard unsubscription.
#         try:
#             subscriber = NewsletterSubscriber.objects.get(pk=pk)
#             subscriber.delete()
#             return True
#         except ObjectDoesNotExist:
#             return False
        
#     # --- New methods for Deleted Subscribers (Admin Only) ---
    
#     @staticmethod
#     def get_all_deleted_subscribers():
#         """Retrieves all deleted newsletter subscriptions."""
#         deleted_subscribers = DeletedSubscriber.objects.all()
#         serializer = DeletedSubscriberSerializer(deleted_subscribers, many=True)
#         return {'success': True, 'data': serializer.data}, 200

#     @staticmethod
#     def get_deleted_subscriber_by_id(pk):
#         """Retrieves a single deleted subscriber by ID."""
#         try:
#             deleted_subscriber = DeletedSubscriber.objects.get(pk=pk)
#             serializer = DeletedSubscriberSerializer(deleted_subscriber)
#             return {'success': True, 'data': serializer.data}, 200
#         except ObjectDoesNotExist:
#             return {'success': False, 'message': 'Deleted subscriber not found.'}, 404

#     @staticmethod
#     def delete_single_deleted_subscriber(pk):
#         """Permanently deletes a single unsubscribed email from the deleted list."""
#         try:
#             deleted_subscriber = DeletedSubscriber.objects.get(pk=pk)
#             deleted_subscriber.delete()
#             logger.info(f"Permanently deleted subscriber with ID {pk} from deleted list.")
#             return {'success': True, 'message': 'Deleted subscriber permanently removed.'}, 204
#         except ObjectDoesNotExist:
#             return {'success': False, 'message': 'Deleted subscriber not found.'}, 404
#         except Exception as e:
#             logger.error(f"Error deleting single deleted subscriber {pk}: {str(e)}", exc_info=True)
#             return {'success': False, 'message': 'An error occurred during deletion.'}, 500

#     @staticmethod
#     def delete_all_deleted_subscribers():
#         """Permanently deletes all unsubscribed emails from the deleted list."""
#         count, _ = DeletedSubscriber.objects.all().delete()
#         logger.info(f"Permanently deleted {count} subscribers from deleted list.")
#         return {'success': True, 'message': f'All {count} deleted subscribers permanently removed.'}, 204


















class NewsletterService:
    @staticmethod
    def get_unsubscribe_url(email):
        """Generate unsubscribe link with email parameter for the frontend."""
        try:
            frontend_url = getattr(settings, 'FRONTEND_URL', None)
            if frontend_url:
                # This should point to your Next.js unsubscribe page
                return f"{frontend_url}/unsubscribe/?email={email}"
            
            # Fallback to backend URL if frontend URL is not set (less ideal for user)
            # You might want to remove this fallback if frontend is always expected.
            return f"{ContactService.get_base_url()}/api/newsletter/unsubscribe/?email={email}"
        except Exception as e:
            logger.error(f"Error generating unsubscribe URL: {str(e)}")
            # Provide a generic fallback URL if all else fails
            return f"http://www.alexandercyril.xyz/unsubscribe/?email={email}"  

    @staticmethod
    def subscribe_email(data):
        email = data.get('email')
        if not email:
            raise ValidationError({'email': 'This field is required.'})

        try:
            if NewsletterSubscriber.objects.filter(email=email).exists():
                raise ValidationError({'email': 'This email is already an active subscriber.'})

            deleted_sub = DeletedSubscriber.objects.filter(email=email).first()
            if deleted_sub:
                deleted_sub.delete()
                logger.info(f"Removed {email} from deleted subscribers for re-subscription.")

            subscriber = NewsletterSubscriber.objects.create(email=email, is_active=True)
            logger.info(f"New active newsletter subscriber created: {email}")

            if settings.EMAIL_HOST_USER:
                unsubscribe_url = NewsletterService.get_unsubscribe_url(email)
                
                # --- Context for the welcome email template ---
                context = {
                    'subscriber_email': email,
                    'unsubscribe_url': unsubscribe_url,
                    'current_year': timezone.now().year,
                    'current_month_year': timezone.now().strftime("%B %Y"), # e.g., "June 2025"
                    'website_url': getattr(settings, 'FRONTEND_URL', 'https://www.alexandercyril.xyz'), # Your website base URL
                    'preferences_url': f"{getattr(settings, 'FRONTEND_URL', 'https://www.alexandercyril.xyz')}/preferences", # Example preference URL
                    'view_in_browser_url': f"{ContactService.get_base_url()}/newsletter/view-in-browser/{subscriber.id}/", # Or link to a publicly hosted version
                    # Add your social media links here
                    'linkedin_url': 'https://www.linkedin.com/in/alexander-cyril-603a2528a/', # Replace with actual
                    'github_url': 'https://github.com/alexcy1', # Replace with actual
                    'twitter_url': 'https://twitter.com/yourtwitterprofile', # Replace with actual
                }

                # 1. Send welcome email to subscriber
                # Render HTML content from template
                html_content_raw = render_to_string('newsletter/welcome_newsletter_email.html', context)
                
                # Use premailer to inline CSS
                # Provide a base_url if your template uses relative URLs for images that need to be absolutized.
                # For inline CSS, base_url is less critical but good practice.
                inliner = premailer.Premailer(html_content_raw,
                                             base_url=ContactService.get_base_url(),
                                             cssutils_logging_level=logging.WARNING) 
                html_message = inliner.transform()

                plain_message = strip_tags(html_message) # Generate plain text from the *inlined* HTML

                msg = EmailMultiAlternatives(
                    subject="Welcome to Alexander S. Cyril's Newsletter!",
                    body=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                msg.attach_alternative(html_message, "text/html")
                msg.send(fail_silently=False)
                
                logger.info(f"Welcome HTML email sent to {email}")

                # 2. Send notification to admin (can remain plain text or be HTML too)
                admin_message = f"""New newsletter subscription:

Email: {email}
Date: {subscriber.subscribed_at.strftime("%Y-%m-%d %H:%M:%S")}

Current active subscribers: {NewsletterSubscriber.objects.filter(is_active=True).count()}
"""
                send_mail(
                    subject=f"New Newsletter Subscriber: {email}",
                    message=admin_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                logger.info(f"Admin notification sent for new subscriber {email}")

            return subscriber

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error in newsletter subscription for {email}: {str(e)}", exc_info=True)
            raise ValidationError({'error': 'An internal error occurred during subscription.'})
        
    @staticmethod
    def unsubscribe_email(email):
        """
        Handles unsubscription: Moves subscriber to DeletedSubscriber table.
        Returns tuple: (success: bool, message: str)
        """
        if not email:
            return False, "Email is required"

        try:
            subscriber = NewsletterSubscriber.objects.get(email=email)

            DeletedSubscriber.objects.create(
                email=subscriber.email,
                unsubscribed_at=timezone.now()
            )
            logger.info(f"Moved {email} to DeletedSubscriber table.")

            subscriber.delete() 
            logger.info(f"Deleted {email} from active NewsletterSubscriber table.")

            # Send unsubscribe confirmation email
            if settings.EMAIL_HOST_USER:
                try:
                    # --- Context for the unsubscribe email template ---
                    context = {
                        'subscriber_email': email,
                        'current_year': timezone.now().year,
                        'current_month_year': timezone.now().strftime("%B %Y"),
                        'website_url': getattr(settings, 'FRONTEND_URL', 'https://www.alexandercyril.xyz'),
                        'feedback_url': f"{getattr(settings, 'FRONTEND_URL', 'https://www.alexandercyril.xyz')}/feedback/unsubscribe/", # Example feedback URL
                        'preferences_url': f"{getattr(settings, 'FRONTEND_URL', 'https://www.alexandercyril.xyz')}/preferences",
                        'view_in_browser_url': f"{ContactService.get_base_url()}/newsletter/view-in-browser/confirmation/", # A generic link, or dynamic if needed
                        
                        # Add your social media links here
                        'linkedin_url': 'https://www.linkedin.com/in/yourlinkedinprofile', # Replace with actual
                        'github_url': 'https://github.com/yourgithubprofile', # Replace with actual
                        'twitter_url': 'https://twitter.com/yourtwitterprofile', # Replace with actual
                    }
                    
                    # Render HTML content from template
                    html_content_raw = render_to_string('newsletter/unsubscribe_confirmation_email.html', context)
                    
                    # Use premailer to inline CSS
                    inliner = premailer.Premailer(html_content_raw,
                                                 base_url=ContactService.get_base_url(),
                                                 cssutils_logging_level=logging.WARNING) 
                    html_message = inliner.transform()

                    plain_message = strip_tags(html_message)

                    msg = EmailMultiAlternatives(
                        subject="You've been unsubscribed from Alexander S. Cyril's Newsletter",
                        body=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email],
                    )
                    msg.attach_alternative(html_message, "text/html")
                    msg.send(fail_silently=False)

                    logger.info(f"Unsubscribe confirmation HTML email sent to {email}")
                except Exception as e:
                    logger.error(f"Failed to send unsubscribe confirmation to {email}: {str(e)}", exc_info=True)

            return True, "Successfully unsubscribed"

        except NewsletterSubscriber.DoesNotExist:
            if DeletedSubscriber.objects.filter(email=email).exists():
                return False, "This email was already unsubscribed."
            logger.warning(f"Unsubscribe attempt for non-existent or already deleted email: {email}")
            return False, "Email not found in our active subscription list."
        except Exception as e:
            logger.error(f"Error unsubscribing {email}: {str(e)}", exc_info=True)
            return False, "An error occurred while processing your request."
    
    
    @staticmethod
    def reactivate_deleted_subscriber(email):
        """
        Reactivates a deleted subscriber by moving them back to the active subscriber list.
        This leverages the existing subscribe_email logic which handles
        removing from DeletedSubscriber if present.
        """
        if not email:
            raise ValidationError({'email': 'Email is required for reactivation.'})

        try:
            # The subscribe_email method already handles the logic of:
            # 1. Checking if the email is an active subscriber (raises error if so).
            # 2. If found in DeletedSubscriber, it deletes it from there.
            # 3. Creates a new active NewsletterSubscriber.
            # 4. Sends welcome email and admin notification.
            subscriber = NewsletterService.subscribe_email({'email': email})
            logger.info(f"Reactivated subscriber: {email}")
            return {'success': True, 'message': f'Subscriber {email} reactivated successfully.', 'subscriber_id': subscriber.id}, 200
        except ValidationError as e:
            logger.warning(f"Failed to reactivate {email}: {e.detail}")
            return {'success': False, 'message': e.detail}, 400
        except Exception as e:
            logger.error(f"Error reactivating subscriber {email}: {str(e)}", exc_info=True)
            return {'success': False, 'message': 'An internal error occurred during reactivation.'}, 500
    
    
    @staticmethod
    def get_all_subscribers():
        # This will now only return truly active subscribers (those not deleted)
        return NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    
    @staticmethod
    def get_subscriber_detail(pk):
        try:
            return NewsletterSubscriber.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def update_subscriber(pk, data):
        try:
            subscriber = NewsletterSubscriber.objects.get(pk=pk)
            serializer = NewsletterSubscriberSerializer(subscriber, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            raise ValidationError(serializer.errors)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def delete_subscriber(pk):
        # This method directly deletes from NewsletterSubscriber, 
        # it doesn't move to DeletedSubscriber. Use unsubscribe_email for standard unsubscription.
        try:
            subscriber = NewsletterSubscriber.objects.get(pk=pk)
            subscriber.delete()
            return True
        except ObjectDoesNotExist:
            return False
        
    # --- New methods for Deleted Subscribers (Admin Only) ---
    
    @staticmethod
    def get_all_deleted_subscribers():
        """Retrieves all deleted newsletter subscriptions."""
        deleted_subscribers = DeletedSubscriber.objects.all()
        serializer = DeletedSubscriberSerializer(deleted_subscribers, many=True)
        return {'success': True, 'data': serializer.data}, 200

    @staticmethod
    def get_deleted_subscriber_by_id(pk):
        """Retrieves a single deleted subscriber by ID."""
        try:
            deleted_subscriber = DeletedSubscriber.objects.get(pk=pk)
            serializer = DeletedSubscriberSerializer(deleted_subscriber)
            return {'success': True, 'data': serializer.data}, 200
        except ObjectDoesNotExist:
            return {'success': False, 'message': 'Deleted subscriber not found.'}, 404

    @staticmethod
    def delete_single_deleted_subscriber(pk):
        """Permanently deletes a single unsubscribed email from the deleted list."""
        try:
            deleted_subscriber = DeletedSubscriber.objects.get(pk=pk)
            deleted_subscriber.delete()
            logger.info(f"Permanently deleted subscriber with ID {pk} from deleted list.")
            return {'success': True, 'message': 'Deleted subscriber permanently removed.'}, 204
        except ObjectDoesNotExist:
            return {'success': False, 'message': 'Deleted subscriber not found.'}, 404
        except Exception as e:
            logger.error(f"Error deleting single deleted subscriber {pk}: {str(e)}", exc_info=True)
            return {'success': False, 'message': 'An error occurred during deletion.'}, 500

    @staticmethod
    def delete_all_deleted_subscribers():
        """Permanently deletes all unsubscribed emails from the deleted list."""
        count, _ = DeletedSubscriber.objects.all().delete()
        logger.info(f"Permanently deleted {count} subscribers from deleted list.")
        return {'success': True, 'message': f'All {count} deleted subscribers permanently removed.'}, 204




