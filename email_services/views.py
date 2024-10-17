from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_html_email(subject, recipient_email, context):

    # Render HTML email template
    html_content = render_to_string("emails/email_template.html", context)

    # Create email object
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient_email],
    )

    # Set email to HTML content type
    email.content_subtype = "html"
    email.send()
