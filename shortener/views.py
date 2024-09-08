from django.shortcuts import get_object_or_404, redirect, render
from .models import ShortenedURL
from django.http import HttpResponse
from django.contrib import messages
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('url')

        # Verify if the provided URL is real and accessible
        try:
            response = requests.get(original_url, timeout=5)  # after 5 seconds
            if response.status_code == 200:
                # URL is valid, proceed to create a shortened URL
                
                # Check if the user is authenticated
                if request.user.is_authenticated:
                    new_short_url = ShortenedURL.objects.create(original_url=original_url, created_by=request.user)
                else:
                    new_short_url = ShortenedURL.objects.create(original_url=original_url)  # No created_by if user is anonymous
                
                shortened_url = request.build_absolute_uri(f'/{new_short_url.short_code}')
                return render(request, 'shortener/index.html', {'shortened_url': shortened_url})

            else:
                # URL returned a non-success status code
                messages.error(request, f'The provided URL is not accessible (Status Code: {response.status_code}).')

        except requests.exceptions.RequestException:
            # Handle any request exceptions (e.g., invalid URL, no connection)
            messages.error(request, 'The provided URL is invalid or cannot be reached.')

    return render(request, 'shortener/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            messages.success(request, 'Account created successfully!')
            return redirect('shorten_url')  # Redirect to the home page or shorten URL page after successful signup
    else:
        form = UserCreationForm()  # Render the empty form when the request method is GET

    return render(request, 'registration/signup.html', {'form': form})  # Always return a response

def user_links(request):
    # Handle deleting all links
    if 'delete_all' in request.POST:
        ShortenedURL.objects.filter(created_by=request.user).delete()
        return redirect('user_links')
    
    # Handle deleting individual links
    if 'delete_link' in request.POST:
        link_id = request.POST.get('link_id')
        ShortenedURL.objects.filter(id=link_id, created_by=request.user).delete()
        return redirect('user_links')

    # Get all links for the logged-in user and generate the full URLs
    user_links = ShortenedURL.objects.filter(created_by=request.user)
    for link in user_links:
        # Ensure the URL is built from the root (by prepending '/')
        link.full_url = request.build_absolute_uri(f'/{link.short_code}')
    return render(request, 'shortener/user_links.html', {'user_links': user_links})
''' OLD
def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('url')
        new_short_url = ShortenedURL.objects.create(original_url=original_url)
        shortened_url = request.build_absolute_uri(f'/{new_short_url.short_code}')  # Generates full URL
        return render(request, 'shortener/index.html', {'shortened_url': shortened_url})
    return render(request, 'shortener/index.html')
'''
def redirect_url(request, short_code):
    short_url = get_object_or_404(ShortenedURL, short_code=short_code)
    return redirect(short_url.original_url)
