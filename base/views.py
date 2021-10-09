from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm

# Create your views here.

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        user = authenticate(request, 
                            username=username, 
                            password=password
                            )
        if user is not None:
            login(request, user)
            return redirect('flux')
        else:
            messages.error(request, 'Username or password is incorrect.')
    context = {}
    return render(request, 'base/login_register.html', context)

def register(request):
    context = {}
    return render(request, 'base/register.html', context)

def flux(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    all_obj = []
    [all_obj.append(ticket) for ticket in tickets]
    [all_obj.append(review) for review in reviews]
    all = sorted(all_obj, key=lambda x: x.time_created, reverse=True)
    noitem = False
    if len(all_obj) == 0:
        noitem = True
    context = {'all_obj': all, 'noitem': noitem}
    return render(request, 'base/flux.html', context)

def abo(request):
    return render(request, 'base/abo.html')

def create_ticket(request):
    ticketForm = TicketForm()
    if request.method == "POST":
        ticketForm = TicketForm(request.POST)
        if ticketForm.is_valid():
            ticketForm.save()
            return redirect('flux')
    context = {'ticketForm': ticketForm}
    return render(request, 'base/create_ticket.html', context)

def update_own_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketForm(instance=ticket)

    context = {}
    return render(request, 'base/modify_own_ticket.html', context)

def create_critique(request):
    reviewForm = ReviewForm()
    if request.method == "POST":
        reviewForm = ReviewForm(request.POST)
        if reviewForm.is_valid():
            reviewForm.save()
            return redirect('flux')
    context = {'reviewForm': reviewForm}
    return render(request, 'base/create_critique.html', context)

def answer_ticket(request):
    return render(request, 'base/answer_ticket.html')

def own_posts(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    ticket = Ticket.objects.filter(user=request.user)
    review = Review.objects.filter(user=request.user)
    all_posts = []
    for dico in review:
        dico.rating = [i for i in range(dico.rating)]
    [all_posts.append(i) for i in ticket]
    [all_posts.append(i) for i in review]
    all = sorted(all_posts, key=lambda x: x.time_created, reverse=True)
    context = { 'all_posts': all, 'tickets': tickets, 'reviews': reviews }
    return render(request, 'base/own_posts.html', context)

def update_own_critique(request):
    return render(request, 'base/update_own_critique.html')

    # 1:56:20 update
