from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Appointment

@receiver(post_save, sender=Appointment)
def send_status_update_email(sender, instance, created, **kwargs):
    if not created:  # sirf update hone pe
        if instance.status == "Confirmed":
            # Customer email
            customer_html = render_to_string("customer_confirm_email.html", {"appointment": instance})
            customer_email = EmailMessage(
                "Your Appointment is Confirmed ✅", customer_html,
                "vinayakjaunjal2003@gmail.com", [instance.email]
            )
            customer_email.content_subtype = "html"
            customer_email.send()

            # Admin email
            admin_html = render_to_string("admin_confirm_email.html", {"appointment": instance})
            admin_email = EmailMessage(
                "Appointment Confirmed", admin_html,
                "vinayakjaunjal2003@gmail.com", ["vinayakjaunjal2003@gmail.com"]
            )
            admin_email.content_subtype = "html"
            admin_email.send()

        elif instance.status == "Rejected":
            # Customer email
            customer_html = render_to_string("customer_reject_email.html", {"appointment": instance})
            customer_email = EmailMessage(
                "Your Appointment is Rejected ❌", customer_html,
                "vinayakjaunjal2003@gmail.com", [instance.email]
            )
            customer_email.content_subtype = "html"
            customer_email.send()

            # Admin email
            admin_html = render_to_string("admin_reject_email.html", {"appointment": instance})
            admin_email = EmailMessage(
                "Appointment Rejected", admin_html,
                "vinayakjaunjal2003@gmail.com", ["vinayakjaunjal2003@gmail.com"]
            )
            admin_email.content_subtype = "html"
            admin_email.send()
