from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import threading


def send_email(subject, recipient_email, context):
    # Render HTML email template
    html_content = render_to_string("emails/email_template.html", context)

    # Create email object
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=f"Rent Home <{settings.EMAIL_HOST_USER}>",
        to=[recipient_email],
    )

    # Set email to HTML content type
    email.content_subtype = "html"
    email.send()

'''
use Python's threading module to send emails in a separate thread.
This allows the main thread to continue processing requests without waiting for the email to send.
'''

def send_html_email(subject, recipient_email, context):

    # Start a new thread to send email.
    thread = threading.Thread(
        target=send_email, args=(subject, recipient_email, context)
    )
    thread.start()


