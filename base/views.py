from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Ticket, Review, UserFollow
from .forms import TicketForm, ReviewForm


def loginPage(request):
    page = 'login'
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
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='/')
def flux(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    for dico in reviews:
        dico.rating = [i for i in range(dico.rating)]
    all_obj = []
    [all_obj.append(ticket) for ticket in tickets]
    [all_obj.append(review) for review in reviews]
    all = sorted(all_obj, key=lambda x: x.time_created, reverse=True)
    noitem = False
    if len(all_obj) == 0:
        noitem = True
    context = {'all_obj': all, 'noitem': noitem}
    return render(request, 'base/flux.html', context)

@login_required(login_url='/')
def abo(request):
    return render(request, 'base/abo.html')

@login_required(login_url='/')
def create_ticket(request):
    ticketForm = TicketForm()
    if request.method == "POST":
        print(request.POST)
        ticketForm = TicketForm(request.POST)
        if ticketForm.is_valid():
            ticketForm.save()
            return redirect('flux')
    context = {'ticketForm': ticketForm}
    return render(request, 'base/create_ticket.html', context)

@login_required(login_url='/')
def update_own_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketForm(instance=ticket)

    context = {}
    return render(request, 'base/modify_own_ticket.html', context)

@login_required(login_url='/')
def create_critique(request):
    reviewForm = ReviewForm(request.POST, request.FILES or None)
    if request.method == 'POST' and request.POST.get('product_type') != None:
        print('--------------------------------------------------------')
        print('--------------------------------------------------------')
        print('--------------------------------------------------------')
        print('--------------------------------------------------------')
        actualuser = User.objects.get(username=request.user)
        review = Review.objects.create(
            product_type = request.POST.get('product_type'),
            product_description = request.POST.get('product_description'),
            product_image = request.POST.get('produt_image'),
            rating = request.POST.get('rating'),
            headline = request.POST.get('headline'),
            user = actualuser,
            body = request.POST.get('body')            
        )
        review.save()
        return redirect('flux')
    context = {'reviewForm': reviewForm}
    return render(request, 'base/create_critique.html', context)

@login_required(login_url='/')
def answer_ticket(request):
    return render(request, 'base/answer_ticket.html')

@login_required(login_url='/')
def own_posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    all_posts = []
    for dico in reviews:
        dico.rating = [i for i in range(dico.rating)]
    [all_posts.append(i) for i in tickets]
    [all_posts.append(i) for i in reviews]
    all = sorted(all_posts, key=lambda x: x.time_created, reverse=True)
    context = { 'all_posts': all }
    return render(request, 'base/own_posts.html', context)

@login_required(login_url='/')
def update_own_critique(request):
    return render(request, 'base/update_own_critique.html')

    # 1:56:20 update


def logoutUser(request):
    logout(request)
    return redirect('/')

def register(request):
    page = "register"
    context = {}
    return render(request, 'base/register.html', context)
