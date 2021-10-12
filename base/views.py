import os, re
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket, Review, UserFollow
from .forms import TicketForm, ReviewForm
from base.models import Review, Ticket


def loginPage(request):
    if request.user is not None:
        logout(request)
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
            not_valid=True
    return render(request, 'base/login_register.html')

@login_required(login_url='/')
def flux(request):
    if request.method == 'GET':
        actualuser = User.objects.get(username=request.user.username)
        followeds = [i.followed_user for i in UserFollow.objects.filter(user=actualuser)]
        followeds.append(actualuser)
        tickets = Ticket.objects.all()
        reviews = Review.objects.all()
        for dico in reviews:
            dico.note = [i for i in range(dico.note)]
        all_obj = []
        for ticket in tickets:
            for i in followeds:
                if (ticket.user == i or ticket.user == actualuser):
                    all_obj.append(ticket)
        for review in reviews:
            for i in followeds:
                if (review.user == i or review.user == actualuser):
                    all_obj.append(review)
        all = sorted(all_obj, key=lambda x: x.time_created, reverse=True)
        noitem = False
        if len(all_obj) == 0:
            noitem = True
        already_answered = []
        for rev in reviews:
            for tick in tickets:
                if rev.ticket == tick:
                    already_answered.append(tick.pk)
        followeds.remove(actualuser)
        lst_followeds = followeds
        if len(followeds) == 0:
            followeds = False
        else:
            followeds = True
        
        context = {
            'all_obj': all,
            'noitem': noitem,
            'already_answered': already_answered,
            'followeds': followeds,
            'lst_followeds': lst_followeds
            }
        return render(request, 'base/flux.html', context)

@login_required(login_url='/')
def abo(request):
    actualuser = User.objects.get(username=request.user.username)
    followeds = [i.followed_user for i in UserFollow.objects.filter(user=actualuser)]
    q = None
    res_search = None
    try:
        if request.method == 'GET':
            q = request.GET.get('q').lower()
        if q is not None:
            try:
                res_search = User.objects.get(username=q)
            except:
                res_search = 'nobody'
    except AttributeError:
        users = User.objects.all()
        context = {'users': users, 
                'res_search': res_search,
                'followeds': followeds
                    }
        return render(request, 'base/abo.html', context)
    if request.method == 'POST':
            q = request.GET.get('q').lower()
            followed = User.objects.get(username=q)
            actualuser = User.objects.get(username=request.user.username)
            if followed not in followeds:
                new = UserFollow.objects.create(
                    user = actualuser,
                    followed_user = followed
                    )
                new.save()
            users = User.objects.all()
            followeds = [i.followed_user for i in UserFollow.objects.filter(user=actualuser)]
            context = {'users': users, 'res_search': res_search, 'followeds': followeds}
            return render(request, 'base/abo.html', context)
    users = User.objects.all()
    followeds = [i.followed_user for i in UserFollow.objects.filter(user=actualuser)]
    context = {'users': users, 'res_search': res_search, 'followeds': followeds}
    return render(request, 'base/abo.html', context)

@login_required(login_url='/')
def create_ticket(request):
    ticketForm = TicketForm(request.POST, request.FILES)
    actualuser = User.objects.get(username=request.user)
    if request.method == "POST":
        ticket = Ticket.objects.create(
            titre = request.POST.get('titre'),
            description = request.POST.get('description'),
            image = request.FILES.get('image'),
            user = actualuser
        )
        ticket.save()
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
    reviewForm = ReviewForm(request.POST, request.FILES)
    if request.method == 'POST' and request.POST.get('type_produit') != None:
        for i,j in request.POST.items():
            if i == "note":
                if int(j) not in range(0,5):
                    message = messages.error(request, 'la note est incorrecte, elle doit être comprise entre 0 et 5')
                    context = {'reviewForm': reviewForm, "message": message}
                    return render(request, 'base/create_critique.html', context)
        actualuser = User.objects.get(username=request.user)
        review = Review.objects.create(
            type_produit = request.POST.get('type_produit'),
            titre_produit = request.POST.get('titre_produit'),
            description_produit = request.POST.get('description_produit'),
            image_produit = request.FILES.get('image_produit'),
            note = request.POST.get('note'),
            titre_critique = request.POST.get('titre_critique'),
            user = actualuser,
            description_critique = request.POST.get('description_critique')            
        )
        review.save()
        return redirect('flux')
    context = {'reviewForm': reviewForm}
    return render(request, 'base/create_critique.html', context)

@login_required(login_url='/')
def answer_ticket(request, pk):
    tick = Ticket.objects.get(id=pk)
    reviewForm = ReviewForm()
    if request.method == 'POST':
        review = Review.objects.create(
            ticket = tick,
            type_produit = request.POST.get('type_produit'),
            titre_produit = tick.titre,
            description_produit = tick.description,
            image_produit = tick.image,
            note = request.POST.get('note'),
            titre_critique = request.POST.get('titre_critique'),
            user = request.user,
            description_critique = request.POST.get('description_critique')
        )
        review.save()
        return redirect('flux')
    context = {'reviewForm': reviewForm, 'ticket': tick}
    return render(request, 'base/answer_ticket.html', context)

@login_required(login_url='/')
def update_own_critique(request):
    if request.method == 'POST':
        [print(i,j) for i,j in request.POST.items()]
    return render(request, 'base/update_own_critique.html')


@login_required(login_url='/')
def own_posts(request):
    noitem = True
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    all_posts = []
    for dico in reviews:
        dico.note = [i for i in range(dico.note)]
    [all_posts.append(i) for i in tickets]
    [all_posts.append(i) for i in reviews]
    all = sorted(all_posts, key=lambda x: x.time_created, reverse=True)
    if len(all) > 0:
        noitem = False
    if request.method == 'POST':
        for i,j in request.POST.items():

            if j == "supprimer" and 'review' in i:
                pk = re.findall("\d+", i)[0]
                Review.objects.filter(pk=pk).delete()
                return redirect('own')
            elif j == "modifier" and 'review' in i:
                pk = re.findall("\d+", i)[0]
                review = Review.objects.get(id=pk)
                reviewForm = ReviewForm()
                context = {"review": i, "reviewForm": reviewForm}
                return render(request, 'base/update_own_critique.html', context)
            elif j == "supprimer" and 'ticket' in i:
                pk = re.findall("\d+", i)[0]
                Ticket.objects.filter(pk=pk).delete()
                return redirect('own')
            elif j == "modifier" and 'ticket' in i:
                pk = re.findall("\d+", i)[0]
                review = Review.objects.get(id=pk)
                reviewForm = ReviewForm()
                context = {"review": review, "reviewForm": reviewForm}
                return render(request, 'base/update_own_critique.html', context)
    context = { 'all_posts': all, 'noitem': noitem }
    return render(request, 'base/own_posts.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/', {'messages': ""})

def register(request):
    messages.error(request, "")
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('flux')
        else:
            messages.error(request, "Une erreur s'est produite...")
    context = {'form': form}
    return render(request, 'base/register.html', context)
