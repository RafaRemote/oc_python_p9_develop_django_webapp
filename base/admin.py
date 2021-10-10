from django.contrib import admin

from .models import Ticket, Review, UserFollow

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollow)
