"""
BusBuzz V1 Authentication

The current application uses Django's built-in authentication system:

- Django User model
- Django Groups for admin/customer roles
- Django sessions
- Django authenticate/login/logout
- UserCreationForm-based customer registration

Legacy BusBuzz authentication previously experimented with:

- LoginVO-based authentication
- bcrypt password hashing
- JWT access and refresh tokens
- device/browser identity verification
- cookie-based token sessions
- OTP password reset
- user blocking

That legacy authentication system is not part of BusBuzz V1.
V1 uses Django's built-in authentication framework instead.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.db.models import Sum
from django.utils import timezone
from datetime import date, datetime
from .models import (
    CreateUserForm,
    BusesVO,
    ScheduleVO,
    BookingsVO,
)
from .decorators import admin_only, unauthenticated_user
from .models import BookingsVO, CreateUserForm

def admin_load_login(request):
    try:
        if request.user.is_authenticated:
            if request.user.groups.filter(name="admin").exists():
                return redirect("admin_load_dashboard")

            if request.user.groups.filter(name="customer").exists():
                return redirect("user_load_dashboard")

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)

                if user.groups.filter(name="admin").exists():
                    return redirect("admin_load_dashboard")

                if user.groups.filter(name="customer").exists():
                    return redirect("user_load_dashboard")

                logout(request)
                messages.error(
                    request,
                    "Your account does not have an assigned role."
                )

            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )

        return render(request, "admin/login.html")

    except Exception as ex:
        print("Exception in admin_load_login:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )
@login_required(login_url="admin_load_login")
def admin_load_logout(request):
    logout(request)
    return redirect("admin_load_login")
@unauthenticated_user
def user_load_user(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            customer_group, created = Group.objects.get_or_create(
                name="customer"
            )

            user.groups.add(customer_group)

            messages.success(
                request,
                f"Account created successfully! {username}"
            )

            return redirect("admin_load_login")

    context = {"form": form}

    return render(
        request,
        "admin/register.html",
        context
    )
@login_required(login_url="admin_load_login")
@admin_only
def admin_load_dashboard(request):
    today = date.today()
    now = datetime.now()
    # =====================================================
    # TOP DASHBOARD STATISTICS
    # =====================================================

    new_bookings_today = BookingsVO.objects.filter(
        booking_date_created__date=today
    ).count()

    departures_today = ScheduleVO.objects.filter(
        trip_scheduled__date=today,
        schedule_status='1'
    ).count()

    total_routes = ScheduleVO.objects.filter(
        schedule_status='1'
    ).values(
        'depart_locations_vo',
        'destination_locations_vo'
    ).distinct().count()

    total_buses = BusesVO.objects.filter(
        bus_status='1'
    ).count()

    # =====================================================
    # BOOKING STATISTICS
    # =====================================================

    total_customers = User.objects.filter(
        groups__name='customer'
    ).distinct().count()

    pending_bookings = BookingsVO.objects.filter(
        booking_status='1'
    ).count()

    paid_bookings = BookingsVO.objects.filter(
        booking_status='2'
    ).count()

    cancelled_bookings = BookingsVO.objects.filter(
        booking_status='3'
    ).count()

    # =====================================================
    # BUSINESS SUMMARY
    # =====================================================

    paid_booking_list = BookingsVO.objects.filter(
        booking_status='2'
    ).select_related(
        'booking_schedule_vo'
    )

    total_paid_revenue = sum(
        booking.total_payable()
        for booking in paid_booking_list
    )

    total_seats_booked = BookingsVO.objects.filter(
        booking_status__in=['1', '2']
    ).aggregate(
        total=Sum('booking_seats')
    )['total'] or 0

    # =====================================================
    # LATEST BOOKINGS
    # =====================================================

    latest_bookings = BookingsVO.objects.select_related(
        'booking_user',
        'booking_schedule_vo',
        'booking_schedule_vo__depart_locations_vo',
        'booking_schedule_vo__destination_locations_vo'
    ).order_by(
        '-booking_date_created'
    )[:5]

    # =====================================================
    # NEXT DEPARTURES
    # =====================================================

    next_departures = ScheduleVO.objects.filter(
        trip_scheduled__gte=now,
        schedule_status='1'
    ).select_related(
        'schedule_bus_vo',
        'depart_locations_vo',
        'destination_locations_vo'
    ).order_by(
        'trip_scheduled'
    )[:5]

    # =====================================================
    # ATTENTION NEEDED
    # =====================================================

    pending_attention = BookingsVO.objects.filter(
        booking_status='1'
    ).select_related(
        'booking_user',
        'booking_schedule_vo',
        'booking_schedule_vo__depart_locations_vo',
        'booking_schedule_vo__destination_locations_vo'
    ).order_by(
        'booking_date_created'
    )[:5]

    context = {
        'new_bookings_today': new_bookings_today,
        'departures_today': departures_today,
        'total_routes': total_routes,
        'total_buses': total_buses,

        'total_customers': total_customers,
        'pending_bookings': pending_bookings,
        'paid_bookings': paid_bookings,
        'cancelled_bookings': cancelled_bookings,

        'total_paid_revenue': total_paid_revenue,
        'total_seats_booked': total_seats_booked,

        'latest_bookings': latest_bookings,
        'next_departures': next_departures,
        'pending_attention': pending_attention,
    }

    return render(
        request,
        'admin/index.html',
        context
    )
@login_required(login_url="admin_load_login")
def user_load_dashboard(request):

    # Admin should use the admin dashboard
    if request.user.groups.filter(name="admin").exists():
        return redirect("admin_load_dashboard")

    # Only customers can access customer dashboard
    if not request.user.groups.filter(name="customer").exists():
        return HttpResponseForbidden(
            "You are not authorized to view this page"
        )


    # -----------------------------------------
    # CURRENT USER'S ACTIVE BOOKINGS
    # -----------------------------------------

    bookings = BookingsVO.objects.filter(
        booking_user=request.user,
        booking_status__in=["1", "2"],
    )


    # -----------------------------------------
    # TOTAL BOOKINGS
    # -----------------------------------------

    booking_count = bookings.count()


    # -----------------------------------------
    # TOTAL SEATS BOOKED
    # -----------------------------------------

    total_seats = (
        bookings.aggregate(
            total=Sum("booking_seats")
        )["total"]
        or 0
    )


    # -----------------------------------------
    # UPCOMING BOOKINGS
    # -----------------------------------------

    upcoming_bookings = bookings.filter(
        booking_schedule_vo__trip_scheduled__gte=timezone.now(),
        booking_schedule_vo__schedule_status="1",
    )


    # Count unique upcoming trips
    upcoming_count = (
        upcoming_bookings
        .values("booking_schedule_vo_id")
        .distinct()
        .count()
    )


    # -----------------------------------------
    # NEAREST UPCOMING TRIP
    # -----------------------------------------

    next_booking = (
        upcoming_bookings
        .select_related(
            "booking_schedule_vo",
            "booking_schedule_vo__schedule_bus_vo",
            "booking_schedule_vo__depart_locations_vo",
            "booking_schedule_vo__destination_locations_vo",
        )
        .order_by(
            "booking_schedule_vo__trip_scheduled"
        )
        .first()
    )


    # -----------------------------------------
    # DASHBOARD CONTEXT
    # -----------------------------------------

    context = {
        "page_title": "Dashboard",
        "active_page": "home",

        "upcoming_count": upcoming_count,
        "booking_count": booking_count,
        "total_seats": total_seats,
        "next_booking": next_booking,
    }


    return render(
        request,
        "user/index.html",
        context
    )

# def admin_validate_login(request):
#     try:
#         login_username = request.POST.get('loginUsername')
#         print("login_username>>>>>>>", login_username)
#         login_password = request.POST.get('loginPassword').encode(
#             config.get("ALGORITHMS", "ENCODING"))
#
#         login_vo_list = LoginVO.objects.filter(login_username=login_username)
#         if len(login_vo_list) == 0:
#             error_message = 'Username and Password is incorrect !'
#             messages.info(request, error_message)
#             return redirect('/')
#         else:
#             login_dict = model_to_dict(login_vo_list[0])
#             if not login_dict['login_status']:
#                 error_message = 'You have been temporarily blocked by admin !'
#                 messages.info(request, error_message)
#                 return redirect('/')
#             else:
#                 login_id = login_dict['login_id']
#                 login_username = login_dict['login_username']
#                 login_role = login_dict['login_role']
#
#                 hashed_login_password = login_dict['login_password'] \
#                     .encode(config.get("ALGORITHMS", "ENCODING"))
#                 if bcrypt.checkpw(login_password, hashed_login_password):
#                     insert_client_identity(request, login_id)
#                     if login_role == 'admin':
#                         response = redirect(admin_load_dashboard)
#                         response.set_cookie(
#                             config.get("TOKENS", "ACCESSTOKEN"),
#                             value=jwt.encode({
#                                 'public_id': login_username,
#                                 'role': login_role,
#                                 'exp': datetime.utcnow() + timedelta(
#                                     minutes=config.getint("TIME",
#                                                           "ACCESS_TOKEN_EXP"))
#                             }, SECRET_KEY,
#                                 config.get("ALGORITHMS", "HASH_ALGORITHM")),
#                             max_age=config.getint("TIME",
#                                                   "ACCESS_TOKEN_MAX_AGE"))
#
#                         refresh = jwt.encode({
#                             'public_id': login_username,
#                             'exp': datetime.utcnow() + timedelta(
#                                 hours=config.getint("TIME",
#                                                     "REFRESH_TOKEN_EXP"))
#                         }, SECRET_KEY,
#                             config.get("ALGORITHMS", "HASH_ALGORITHM"))
#
#                         response.set_cookie(
#                             config.get("TOKENS", "REFRESHTOKEN"),
#                             value=refresh,
#                             max_age=config.getint("TIME",
#                                                   "REFRESH_TOKEN_MAX_AGE"))
#                         return response
#
#                     elif login_role == 'user':
#                         response = redirect(user_load_dashboard)
#                         response.set_cookie(
#                             config.get("TOKENS", "ACCESSTOKEN"),
#                             value=jwt.encode({
#                                 'public_id': login_username,
#                                 'role': login_role,
#                                 'exp': datetime.utcnow() + timedelta(
#                                     minutes=config.getint("TIME",
#                                                           "ACCESS_TOKEN_EXP"))
#                             }, SECRET_KEY,
#                                 config.get("ALGORITHMS", "HASH_ALGORITHM")),
#                             max_age=config.getint("TIME",
#                                                   "ACCESS_TOKEN_MAX_AGE"))
#
#                         refresh = jwt.encode({
#                             'public_id': login_username,
#                             'exp': datetime.utcnow() + timedelta(
#                                 hours=config.getint("TIME",
#                                                     "REFRESH_TOKEN_EXP"))
#                         }, SECRET_KEY,
#                             config.get("ALGORITHMS", "HASH_ALGORITHM"))
#
#                         response.set_cookie(
#                             config.get("TOKENS", "REFRESHTOKEN"),
#                             value=refresh,
#                             max_age=config.getint("TIME",
#                                                   "REFRESH_TOKEN_MAX_AGE"))
#                         return response
#                     else:
#                         return redirect(admin_logout_session)
#                 else:
#                     error_message = 'password is incorrect !'
#                     messages.info(request, error_message)
#                     return redirect('/')
#     except Exception as ex:
#         print("admin_validate_login route exception occured>>>>>>>>>>", ex)
#         return render(request, 'admin/viewError.html', context={'message': ex})
#
#
#
# def admin_logout_session(request, *user_name):
#     try:
#         if len(user_name) != 0 and user_name[0] is not None:
#             login_vo = LoginVO()
#
#             login_vo.login_username = user_name[0]
#
#             login_vo_list = LoginVO.objects.filter(
#                 login_username=login_vo.login_username).all()
#
#             login_id = login_vo_list[0].login_id
#
#             device_list = DeviceInfoVO.objects. \
#                 filter(device_login_vo_id=login_id).all()
#             for device_vo in device_list:
#                 device_vo.delete()
#
#             response = redirect('/')
#             response.set_cookie(config.get("TOKENS", "ACCESSTOKEN"),
#                                 max_age=config.getint("TIME",
#                                                       "TIME_OUT_MAX_AGE"))
#             response.set_cookie(config.get("TOKENS", "REFRESHTOKEN"),
#                                 max_age=config.getint("TIME",
#                                                       "TIME_OUT_MAX_AGE"))
#             return response
#
#         elif request.COOKIES.get(
#                 config.get("TOKENS", "REFRESHTOKEN")) is not None:
#             refreshtoken = request.COOKIES.get(
#                 config.get("TOKENS", "REFRESHTOKEN"))
#
#             data = jwt.decode(refreshtoken, SECRET_KEY,
#                               config.get("ALGORITHMS", "HASH_ALGORITHM"))
#
#             login_vo = LoginVO()
#             device_vo = DeviceInfoVO()
#
#             login_vo.login_username = data['public_id']
#
#             login_vo_list = LoginVO.objects.filter(
#                 login_username=login_vo.login_username).all()
#
#             login_vo = login_vo_list[0]
#
#             device_list = DeviceInfoVO.objects.filter(
#                 device_login_vo_id=login_vo.login_id).all()
#             if len(device_list) != 0:
#                 for device in device_list:
#                     if bcrypt.checkpw(get_client_identity(request).encode(
#                             config.get("ALGORITHMS", "ENCODING")),
#                             device.device_identity.encode(
#                                 config.get("ALGORITHMS", "ENCODING"))):
#                         device_vo = device
#                         break
#                 device_vo = DeviceInfoVO.objects.get(device_id
#                                                      =device_vo.device_id)
#                 device_vo.delete()
#             response = redirect('/')
#             response.set_cookie(config.get("TOKENS", "ACCESSTOKEN"),
#                                 max_age=config.getint("TIME",
#                                                       "TIME_OUT_MAX_AGE"))
#             response.set_cookie(config.get("TOKENS", "REFRESHTOKEN"),
#                                 max_age=config.getint("TIME",
#                                                       "TIME_OUT_MAX_AGE"))
#             return response
#
#         else:
#             response = redirect('/')
#             response.set_cookie(config.get("TOKENS", "ACCESSTOKEN"),
#                                 max_age=config.getint("TIME",
#                                                       "TIME_OUT_MAX_AGE"))
#             response.set_cookie(config.get("TOKENS", "REFRESHTOKEN"),
#                                 max_age=config.getint("TIME",
#                                                       "TIME_OUT_MAX_AGE"))
#             return response
#     except Exception as ex:
#         print("admin_logout_session route exception occured>>>>>>>>>>", ex)
#         return render(request, 'admin/viewError.html', context={'message': ex})
#
# def admin_block_user(request):
#     try:
#         login_id = request.GET.get('loginId')
#         login_vo = LoginVO.objects.get(login_id=login_id)
#         login_vo.login_status = False
#         login_vo.save()
#         return redirect("/admin/view_user")
#
#     except Exception as ex:
#         print("admin_block_user route exception occured>>>>>>>>>>", ex)
#         return render(request, 'admin/viewError.html', context={'message': ex})
#
# def user_load_forget_password(request):
#     try:
#         return render(request, 'user/forgetPassword.html')
#     except Exception as ex:
#         print("user_load_forget_password route exception occured>>>>>>>>>>",
#               ex)
#         return render(request, 'user/viewError.html', context={'message': ex})
#
#
#
# def user_validate_login_username(request):
#     try:
#         login_username = request.POST.get("loginUsername")
#         login_vo_list = LoginVO.objects.filter(login_username=login_username)
#         login_list = [model_to_dict(i) for i in login_vo_list]
#         len_login_list = len(login_list)
#         if len_login_list == 0:
#             error_message = 'username is incorrect !'
#             messages.info(request, error_message)
#             return redirect('/user/load_forget_password')
#         else:
#             login_id = login_list[0]['login_id']
#             request.session['session_login_id'] = login_id
#             login_username = login_list[0]['login_username']
#             sender = "noreplypython@yahoo.com"
#             receiver = login_username
#             msg = MIMEMultipart()
#             msg['From'] = sender
#             msg['To'] = receiver
#             msg['Subject'] = "PYTHON OTP"
#             otp = random.randint(1000, 9999)
#             request.session['session_otp_number'] = otp
#             message = str(otp)
#             msg.attach(MIMEText(message, 'plain'))
#             server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
#             server.starttls()
#             server.login(sender, "dbzivjinwbndvvey")
#             text = msg.as_string()
#             server.sendmail(sender, receiver, text)
#             server.quit()
#             return render(request, 'user/otpValidation.html')
#     except Exception as ex:
#         print("user_validate_login_username route exception occured>>>>>>>>>>",
#               ex)
#         return render(request, 'user/viewError.html', context={'message': ex})
#
#
# def user_validate_otp_number(request):
#     try:
#         otp_number = int(request.POST.get("otpNumber"))
#         session_otp_number = request.session.get('session_otp_number')
#         if otp_number == session_otp_number:
#             return render(request, 'user/resetPassword.html')
#         else:
#             request.session.flush()
#
#             error_message = 'otp is incorrect !'
#             messages.info(request, error_message)
#             return redirect('/user/load_forget_password')
#     except Exception as ex:
#         print("user_validate_otp_number route exception occured>>>>>>>>>>", ex)
#         return render(request, 'user/viewError.html', context={'message': ex})
#
#
# def user_insert_reset_password(request):
#     try:
#         login_password = request.POST.get("loginPassword")
#         salt = bcrypt.gensalt(rounds=12)
#         hashed_login_password = bcrypt.hashpw(
#             login_password.encode(config.get("ALGORITHMS", "ENCODING")),
#             salt).decode(config.get("ALGORITHMS", "ENCODING"))
#         login_id = request.session.get("session_login_id")
#         login_vo = LoginVO.objects.get(login_id=login_id)
#         login_vo.login_password = hashed_login_password
#         login_vo.save()
#         return redirect('/')
#     except Exception as ex:
#         print("user_insert_reset_password route exception occured>>>>>>>>>>",
#               ex)
#         return render(request, 'user/viewError.html', context={'message': ex})