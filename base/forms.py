from django.forms import ModelForm
from .models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'titre',
            'description',
            'image'
        ]


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
