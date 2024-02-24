from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render


@login_required
def profile_view(request: WSGIRequest):
    return render(request, 'crud/users/profile.html', {'user': request.user})

def logout_view(request):
    print("LOGOUT")
    logout(request)