from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import UserProfile
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import Glucose
from interactions.models import Post


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']  # This can be email or username
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='userauth.authentication.EmailBackend')
            return redirect('userauth:glucose_log')  
        else:
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password.'
                })

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.',
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.',
            })
        UserProfile.objects.create(user=user)
        login(request, user, backend='userauth.authentication.EmailBackend')  
        return redirect('core:index')  
    else:
        return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('userauth:login') 


@login_required
def glucose_log_view(request):
    """
    Allows the user to record their glucose level.
    """
    if request.method == 'POST':
        # Get the values from the form
        glucose = request.POST.get('glucose')
        entry_date = request.POST.get('date')

        # Get the currently logged-in user
        user = request.user

        # Add the data to the glucose level log
        glucose_log = Glucose(user=user, glucose_level=glucose, entry_date=entry_date)
        glucose_log.save()

    # Fetch the glucose log of the logged-in user
    user_glucose_log = Glucose.objects.filter(user=request.user)

    return render(request, 'user_profile.html', {
        'user_glucose_log': user_glucose_log
    })

@login_required
def glucose_log_delete(request, glucose_id):
    '''
    It allows the user to delete a glucose record from their weight log
    '''
    # get the glucose log of the logged in user
    glucose_recorded = Glucose.objects.filter(id=glucose_id)

    if request.method == 'POST':
        glucose_recorded.delete()
        return redirect('userauth:glucose_log')

    return render(request, 'glucose_log_delete.html')



def home_view(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['email'] = request.user.email
    return render(request, 'auth/home.html', context)


def profile_detail(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    posts = Post.objects.filter(author=profile.user)
    like_count = sum(post.liked_by.count() for post in posts)
    like_count = format_count(like_count)
    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "posts": posts,
            "like_count": like_count,
        },
    )


def format_count(count):
    if count > 999:
        return f"{count // 1000}.{count // 100 % 10}k"
    return str(count)


@login_required
def my_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    posts = Post.objects.filter(author=request.user)
    like_count = sum(post.liked_by.count() for post in posts)

    return render(
        request,
        "my_profile.html",
        {"profile": profile, "posts": posts, "like_count": like_count},
    )
