from django.conf import settings
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm
from .encryption_util import *
from .models import Profile
from .token import account_activation_token
from django.views.decorators.cache import cache_page
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.cache import cache_page
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin, messages
from account.services import *
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import JsonResponse


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Without Cache
@api_view(['GET'])
def WithOutCache(request):
    data = serializers.serialize("json", Profile.objects.all())
    return Response(data, status=status.HTTP_200_OK)

# Per-View Cache
@api_view(['GET'])
@cache_page(CACHE_TTL)
def PerViewCache(request):
    data = serializers.serialize("json", Profile.objects.all())
    return Response(data, status=status.HTTP_200_OK)

# Per-Data Cache
@api_view(['GET'])
def PerDataCache(request):
    # Check if Data exist in cache
    if 'user_list' in cache:
        user_list = cache.get('user_list')
        return Response(user_list, status=status.HTTP_200_OK)
    # Else add into cache them send to the response
    else:
        data = serializers.serialize("json", Profile.objects.all())
        cache.set("user_list", data, timeout=CACHE_TTL)
        return Response(data, status=status.HTTP_200_OK)


@require_http_methods(['GET', 'POST'])
def register(request):
    permission_classes = (AllowAny)
    """
    user register new account
    :param request:
    :method POST:
    :return render register page
    """
    # check request method
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        # validate form
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            messages.success(
                request, 'We have sent you an email, please confirm your email address to complete registration')
            return redirect('login')

            # for msg in form.error_messages:
            #     messages.error(request, f"{msg}: {form.error_messages[msg]}")
    # no requested data
    else:
        form = UserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})



def activate_account(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login_auth(request, user)
        messages.success(
            request, ('Your account has been activate successfully'))
        return redirect('login')
    else:
        messages.warning(
            request, 'Activation link is invalid, Please Register Again!')
        return redirect('register')


@require_http_methods(['GET', 'POST'])
def login(request):
    """
    user login

    :param request:
    :method POST:
    :return render register page
    """
    # check request method
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        # validate form
        if form.is_valid():
            # if data does valid, get fields
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                email=email, username=username, password=password)
            login_auth(request, user)
            # message [success]
            messages.success(request, 'Success login')
            # Redirect to login-page
            return redirect('/')
    # no requested data
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'auth/login.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has Been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'profile': Profile.objects.get(user_account_name=request.user.id),
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile_page/profile.html', context)
