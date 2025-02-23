from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger('django')

def send_email(to_email, subject, template, context=None):
    """
    Send an HTML email using a template
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        template (str): Path to HTML template
        context (dict): Template context variables
    """
    try:
        if context is None:
            context = {}
        
        # Add common context variables
        context.update({
            'site_url': settings.SITE_URL,
            'settings': settings,
            'logo_url': f"{settings.SITE_URL}/static/images/logo.png",
            'current_year': settings.CURRENT_YEAR
        })
        
        # Render HTML content
        html_content = render_to_string(template, context)
        
        # Create plain text version
        text_content = strip_tags(html_content)
        
        # Create email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        
        # Attach HTML content
        msg.attach_alternative(html_content, "text/html")
        
        # Send email
        msg.send()
        logger.info(f'Email sent successfully to {to_email}: {subject}')
        
    except Exception as e:
        logger.error(f'Error sending email to {to_email}: {str(e)}')
        raise

def send_contact_confirmation_email(email, name):
    """Send confirmation email to contact form submitter"""
    try:
        send_email(
            to_email=email,
            subject='Am primit mesajul tău - Răsfățul Pescarului',
            template='emails/contact_confirmation.html',
            context={'name': name}
        )
    except Exception as e:
        logger.error(f'Error sending contact confirmation email to {email}: {str(e)}')
        raise

def send_contact_admin_email(name, email, subject, message):
    """Send contact form notification to admin"""
    try:
        send_email(
            to_email=settings.ADMIN_EMAIL,
            subject='Nou mesaj de contact',
            template='emails/contact_admin.html',
            context={
                'name': name,
                'email': email,
                'message': message,
                'subject': subject
            }
        )
    except Exception as e:
        logger.error(f'Error sending contact admin email: {str(e)}')
        logger.exception('Detailed error trace:')
        raise