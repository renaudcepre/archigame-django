from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render


@login_required
def profile_view(request: WSGIRequest):
    print("sdfhoiuh")
    return render(request, 'users/profile.html', {'user': request.user})
