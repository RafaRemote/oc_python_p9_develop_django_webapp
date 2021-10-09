from django.forms import ModelForm
from .models import Ticket, Review

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
