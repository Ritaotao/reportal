from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Profile, Role
from .forms import SignInForm, SignUpForm, UserForm, ProfileForm


# Create your views here.
def signin(request):
    title = "Sign in"
    next = request.GET.get('next')
    form = SignInForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            user = authenticate(request, username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('/')
    return render(request, 'account/signin.html', {'form': form, "title": title})


def signup(request):
    title = "Sign up"
    form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/account/')
    return render(request, "account/signin.html", {"form": form, "title": title})


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required(login_url='login')
def profile_view(request):
    user = User.objects.get(pk=request.user.id)
    profile, _ = Profile.objects.get_or_create(user=request.user)

    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=profile)

    if request.user.is_authenticated:
        if request.method == "POST":
            user_form = UserForm(request.POST, instance=user)
            profile_form = ProfileForm(request.POST, instance=profile) 
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('/account/')
        return render(request, "account/profile.html", {
            "user_form": user_form,
            "profile_form": profile_form,
        })
    else:
        raise PermissionDenied