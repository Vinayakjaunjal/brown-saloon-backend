from twilio.rest import Client
from django.conf import settings
from django.contrib import admin
from .models import Appointment
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect

def format_phone(number):
    # Agar number + se start nahi hota hai to +91 add kar do
    if not number.startswith("+"):
        return "+91" + number
    return number

def send_sms(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_number
    )

from django.contrib import admin
from .models import Appointment, Service

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "date", "time", "status")
    list_filter = ("status", "date","service")
    search_fields = ("name", "email", "phone")
    list_editable = ("status",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:  # status change hone par
            if obj.status == "Confirmed":
                subject = "Appointment Confirmed ✅"
                customer_html = render_to_string("customer_confirm_email.html", {"appointment": obj})
                admin_html = render_to_string("admin_confirm_email.html", {"appointment": obj})

                email1 = EmailMessage(subject, customer_html, "yourmail@example.com", [obj.email])
                email1.content_subtype = "html"   # 👈 HTML mail
                email1.send()
                
                customer_sms = f"Hello {obj.name}, your appointment on {obj.date} at {obj.time} has been Confirmed."
                send_sms(format_phone(obj.phone), customer_sms)

                email2 = EmailMessage(subject, admin_html, "yourmail@example.com", ["admin@example.com"])
                email2.content_subtype = "html"   # 👈 HTML mail
                email2.send()
                
                admin_sms = f"Appointment for {obj.name} on {obj.date} at {obj.time} has been Confirmed." 
                send_sms(settings.ADMIN_MOBILE, admin_sms)

            elif obj.status == "Rejected":
                subject = "Appointment Rejected ❌"
                customer_html = render_to_string("customer_reject_email.html", {"appointment": obj})
                admin_html = render_to_string("admin_reject_email.html", {"appointment": obj})

                email1 = EmailMessage(subject, customer_html, "yourmail@example.com", [obj.email])
                email1.content_subtype = "html"   # 👈 HTML mail
                email1.send()
                
                customer_sms = f"Hello {obj.name}, your appointment on {obj.date} at {obj.time} has been Rejected."
                send_sms(format_phone(obj.phone), customer_sms)

                email2 = EmailMessage(subject, admin_html, "yourmail@example.com", ["admin@example.com"])
                email2.content_subtype = "html"   # 👈 HTML mail
                email2.send()
                
                admin_sms = f"Appointment for {obj.name} on {obj.date} at {obj.time} has been Rejected."
                send_sms(settings.ADMIN_MOBILE, admin_sms)

        # Redirect back to admin page after save
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))