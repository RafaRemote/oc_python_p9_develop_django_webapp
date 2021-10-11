from django.forms import ModelForm
from .models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = '__all__'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'type_produit',
            'titre_produit',
            'description_produit',
            'image_produit',
            'note',
            'titre_critique',
            'description_critique'
        ]


