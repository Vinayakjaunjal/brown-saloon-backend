from django import forms
from .models import Appointment, Service

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'service', 'date', 'time', 'message']

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        empty_label="Select Service",
        widget=forms.Select(attrs={'class': 'input-field'})
    )
