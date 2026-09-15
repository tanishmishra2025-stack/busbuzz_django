"""
BUSBUZZ LEGACY USER MODULE

This module belongs to the original BusBuzz authentication/user system.

V1 now uses Django's built-in authentication system:
    django.contrib.auth.models.User
    Django Groups
    Django sessions
    UserCreationForm

The functions below are retained only as historical/reference code.

IMPORTANT:
- Do not expose user_insert_user through urls.py.
- user_insert_user stores a legacy UserVO password directly and must not
  be used by the current application.
- admin_view_user uses the legacy UserVO model and is not part of the
  current V1 user-management flow.

Future cleanup:
These legacy models/views can be removed after the V1 project history
has been documented.
"""
import bcrypt
import random
import smtplib
import string
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required

from project.settings import admin_role
from .models import LoginVO, UserVO

def user_insert_user(request):
    try:
        user_vo = UserVO()

        user_vo.user_firstname = request.POST.get('userFirstname')
        user_vo.user_lastname = request.POST.get('userLastname')
        user_vo.user_email = request.POST.get('userEmail')
        user_vo.user_password = request.POST.get('userPassword')

        user_vo.save()
        return render(request, 'admin/login.html')
    except Exception as ex:
        print("user_insert_user route exception occured>>>>>>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})

# LEGACY USER MANAGEMENT VIEW
# Not currently exposed through urls.py.
# @login_required(admin_role)
@login_required(login_url='admin_load_login')
def admin_view_user(request):
    try:
        user_vo_list = UserVO.objects.select_related(
            'user_login_vo').select_related('user_area_vo').all()
        return render(request, 'admin/viewUser.html',
                      context={'user_vo_list': user_vo_list})

    except Exception as ex:
        print("admin_view_user route exception occured>>>>>>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})
