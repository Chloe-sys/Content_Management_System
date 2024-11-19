from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, PosterRegistrationForm, PosterLoginForm
from .models import User_Profile, Poster
from content_system.models import Post, PostSubscription
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the User instance
            
            # Create User_Profile with additional fields
            profile = User_Profile(
                user=user,
                username=user.username,  # Copying username from User model
                email=user.email,  # Copying email from User model
                bio=form.cleaned_data.get('bio'),
                profile_picture=form.cleaned_data.get('profile_picture')
            )
            profile.password = user.password  # Copy the hashed password if necessary
            profile.save()  # Save the User_Profile instance

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to the login page
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Check credentials against the database
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('dashboard')  # Redirect to the landing page or dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')  # Error message for invalid credentials
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('landing')  # Redirect to login page after logout

def landing(request):
    return render(request, 'users/landing.html')



def dashboard(request):
    if request.user.is_authenticated:
        # Get posts the user has subscribed to
        subscribed_posts = Post.objects.filter(subscribers__user=request.user)

        # Get all posts for browsing
        all_posts = Post.objects.exclude(subscribers__user=request.user)

        return render(request, 'users/dashboard.html', {
            'subscribed_posts': subscribed_posts,
            'all_posts': all_posts,
        })
    else:
        return redirect('login')


def poster_register(request):
    if request.method == 'POST':
        form = PosterRegistrationForm(request.POST)
        if form.is_valid():
            poster = form.save(commit=False)  # Create an instance without saving
            poster.set_password(form.cleaned_data['password'])  # Hash the password
            poster.save()  # Save the Poster instance
            messages.success(request, 'Poster registration successful.')
            return redirect('poster_login')
    else:
        form = PosterRegistrationForm()
    return render(request, 'users/poster_register.html', {'form': form})


def poster_login(request):
    if request.method == 'POST':
        form = PosterLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check credentials against the database
            try:
                poster = Poster.objects.get(username=username)
                if poster.check_password(password):  # Use the check_password method
                    request.session['poster_id'] = poster.id  # Store the poster ID in the session
                    return redirect('post_list')  # Redirect to the poster's dashboard or posts
                else:
                    messages.error(request, 'Invalid username or password.')
            except Poster.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
    else:
        form = PosterLoginForm()
    return render(request, 'users/poster_login.html', {'form': form})


def poster_logout(request):
    logout(request)  # Log out the poster user
    return redirect('landing')  # Redirect to the landing page after logging out



