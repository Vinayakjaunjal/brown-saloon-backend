from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Appointment
from .forms import AppointmentForm
from .models import Service

def home(request):
    services = Service.objects.all()
    return render(request, 'index.html')

def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = AppointmentForm()
    return render(request, 'book.html', {'form': form})

def book_appointment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email_address")
        phone = request.POST.get("phone")
        category = request.POST.get("category")
        date = request.POST.get("date")
        time = request.POST.get("time")
        message = request.POST.get("message")

        # Save Appointment
        appointment = Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=category,
            date=date,
            time=time,
            message=message,
            status="Pending"
        )

        # ----------- EMAILS -------------
        # Admin ko new booking email
        admin_html = render_to_string("admin_new_email.html", {"appointment": appointment})
        admin_email = EmailMessage(
            "New Appointment Request", admin_html,
            "vinayakjaunjal2003@gmail.com", ["vinayakjaunjal2003@gmail.com"]
        )
        admin_email.content_subtype = "html"
        admin_email.send()

        # Customer ko acknowledgement email
        customer_html = render_to_string("customer_ack_email.html", {"appointment": appointment})
        customer_email = EmailMessage(
            "We Received Your Appointment Request ✅", customer_html,
            "vinayakjaunjal2003@gmail.com", [email]
        )
        customer_email.content_subtype = "html"
        customer_email.send()

        return render(request, 'thanks.html', {"name": name, "date": date, "time": time})

    return redirect("home")