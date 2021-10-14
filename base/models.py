from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class UserFollow(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="following"
                             )
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name="followed_by"
                                      )

    class Meta:
        unique_together = ['user', 'followed_user', ]


PRODUCT_CHOICES = (
    ("Livre", "Livre"),
    ("Article", "Article"),
)


class Ticket(models.Model):
    titre = models.CharField(max_length=128,
                             blank=True
                             )
    description = models.TextField(max_length=2048,
                                   blank=True
                                   )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True
                             )
    image = models.ImageField(upload_to='images',
                              null=True,
                              blank=True
                              )
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True
                               )
    type_produit = models.CharField(max_length=8,
                                    choices=PRODUCT_CHOICES,
                                    default="Livre"
                                    )
    titre_produit = models.CharField(max_length=128)
    description_produit = models.TextField(max_length=8192,
                                           null=True,
                                           blank=True
                                           )
    image_produit = models.ImageField(upload_to='images',
                                      null=True,
                                      blank=True,
                                      )
    note = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],
                                            blank=True
                                            )
    titre_critique = models.CharField(max_length=128,
                                      blank=True
                                      )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True
                             )
    description_critique = models.TextField(max_length=8192,
                                            null=True,
                                            blank=True
                                            )
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return f'Produit: {self.titre_produit}, Son ticket: {self.ticket}'
