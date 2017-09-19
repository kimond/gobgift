from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect


def logout(request):
    auth_logout(request)
    return redirect('/')


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    return render(request, 'home.html')


def app(request):
    return render(request, 'app.html')


@login_required
def done(request):
    """Login complete view, displays user data"""
    return render(request, 'home.html')


def validation_sent(request):
    return render(request, 'home.html', dict(
        validation_sent=True,
        email=request.session.get('email_validation_address')
    ))
