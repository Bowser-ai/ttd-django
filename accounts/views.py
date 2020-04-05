from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


def send_login_email(request):
    email = request.POST.get('email', None)
    send_mail('Your login link for Superlists',
            'Use this link to log in',
            'noreply@superlists.com',
            [email]
            )
    messages.success(
            request,
            'Check your email, we\'ve sent you a link you can use to log in.'
            )
    return redirect('/')

