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

    def __str__(self):
        return self.user


PRODUCT_CHOICES = (
    ("Livre","Livre"),
    ("Article","Article"),
)

class Ticket(models.Model):
    title = models.CharField(max_length=128),
    description = models.TextField(max_length=2048,
                                   blank=True
                                   )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE
                             )
    image = models.ImageField(upload_to='static/images/',
                              null=True,
                              blank=True
                              )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True
                               )
    product_type = models.CharField(max_length=8,
                                    choices=PRODUCT_CHOICES,
                                    default="Livre"
                                    )
    product_title = models.CharField(max_length=128,
                                     null=False,
                                     blank=True
                                    )
    product_description = models.TextField(max_length=8192,
                                           null=True,
                                           blank=True
                                           )
    product_image = models.ImageField(upload_to='static/images/',
                                      null=True,
                                      blank=True
                                      )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],
                                              blank=True
                                              )
    headline = models.CharField(max_length=128,
                                blank=True    
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE
                             )
    body = models.TextField(max_length=8192,
                            null=True,
                            blank=True
                            )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ticket} ==> {self.headline}'
    