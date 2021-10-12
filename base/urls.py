from django.urls import path
from . import views



urlpatterns = [
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name="register"),
    path('flux/', views.flux, name='flux'),
    path('abo/', views.abo, name='abo'),
    path('create-ticket/', views.create_ticket, name='ticket'),
    path('create-critique/', views.create_critique, name='critique'),
    path('answer-ticket/<str:pk>/', views.answer_ticket, name='answer'),
    path('own-posts/', views.own_posts, name='own'),
    path('update-own-critiaue/', views.update_own_critique, name='update-own-critique'),
    path('update-own-ticket/<str>/', views.update_own_ticket, name='update-own-ticket'),
]
 