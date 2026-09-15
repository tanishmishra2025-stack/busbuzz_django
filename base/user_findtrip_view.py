import uuid
from django.db import transaction
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .decorators import allowed_users
from .models import LocationsVO, ScheduleVO, BookingsVO
from django.utils import timezone
from django.views.decorators.http import require_POST
@login_required(login_url="admin_load_login")
@allowed_users(allowed_roles=["customer"])
def user_load_findtrip(request):

    locations_vo_list = LocationsVO.objects.filter(
        locations_status='1'
    )

    context = {
        "locations_vo_list": locations_vo_list,
        "min_date": date.today(),
        "page_title": "Find Trip",
        "active_page": "find_trip",
    }

    return render(
        request,
        "user/findTrip.html",
        context
    )

@login_required(login_url="admin_load_login")
@allowed_users(allowed_roles=["customer"])
def user_check_availability(request):
    try:
        if request.method != "POST":
            return render(
                request,
                "user/viewError.html",
                context={"message": "Invalid request method."},
            )

        travel_date = request.POST.get("date")
        departure_id = request.POST.get("departure")
        destination_id = request.POST.get("destination")

        if not travel_date or not departure_id or not destination_id:
            return render(
                request,
                "user/viewError.html",
                context={"message": "Please provide all trip details."},
            )

        if departure_id == destination_id:
            return render(
                request,
                "user/viewError.html",
                context={
                    "message":
                        "Departure and destination cannot be the same."
                },
            )

        date = datetime.strptime(
            travel_date,
            "%Y-%m-%d",
        ).date()

        today = datetime.today().date()

        if date < today:
            locations_vo_list = LocationsVO.objects.filter(
                locations_status=1
            )

            return render(
                request,
                "user/findTrip.html",
                context={
                    "locations_vo_list": locations_vo_list,
                    "min_date": today.strftime("%Y-%m-%d"),
                    "error_message": "You cannot search for a past trip.",
                },
            )

        depart = get_object_or_404(
            LocationsVO,
            locations_id=departure_id,
            locations_status=1,
        )

        destination = get_object_or_404(
            LocationsVO,
            locations_id=destination_id,
            locations_status=1,
        )

        schedules = ScheduleVO.objects.filter(
            schedule_status=1,
            trip_scheduled__date=date,
            depart_locations_vo=depart,
            destination_locations_vo=destination,
        ).select_related(
            "schedule_bus_vo",
            "depart_locations_vo",
            "destination_locations_vo",
        )

        context = {
            "schedules": schedules,
            "data": {
                "date": date,
                "departure": depart,
                "destination": destination,
            },
        }

        return render(
            request,
            "user/searchedTripResult.html",
            context,
        )

    except ValueError:
        return render(
            request,
            "user/viewError.html",
            context={"message": "Invalid travel date."},
        )

    except Exception as ex:
        print("Exception in user_check_availability:", ex)

        return render(
            request,
            "user/viewError.html",
            context={"message": ex},
        )


@login_required(login_url="admin_load_login")
@allowed_users(allowed_roles=["customer"])
def user_load_bookingform(request, schedPK=None, pk=None):
    try:
        context = {
            "page_title": "Manage Booking",
            "schedule": None,
            "book": None,
            "available_seats": 0,
            "already_booked": 0,
            "remaining_user_limit": 0,
            "max_bookable": 0,
        }

        schedule_id = schedPK or request.GET.get("scheduleId")

        if schedule_id:
            schedule = get_object_or_404(
                ScheduleVO.objects.select_related(
                    "schedule_bus_vo",
                    "depart_locations_vo",
                    "destination_locations_vo",
                ),
                schedule_id=schedule_id,
                schedule_status='1',
            )

            MAX_SEATS_PER_USER = 4

            already_booked = (
                BookingsVO.objects.filter(
                    booking_user=request.user,
                    booking_schedule_vo=schedule,
                    booking_status__in=['1', '2'],
                )
                .aggregate(
                    total=Sum("booking_seats")
                )["total"]
                or 0
            )

            available_seats = schedule.count_available()

            remaining_user_limit = (
                MAX_SEATS_PER_USER - already_booked
            )

            max_bookable = min(
                available_seats,
                max(remaining_user_limit, 0)
            )

            context["schedule"] = schedule
            context["available_seats"] = available_seats
            context["already_booked"] = already_booked
            context["remaining_user_limit"] = remaining_user_limit
            context["max_bookable"] = max_bookable

        if pk is not None:
            context["book"] = get_object_or_404(
                BookingsVO,
                booking_id=pk,
                booking_user=request.user,
            )

        context["schedule_vo_list"] = ScheduleVO.objects.filter(
            schedule_status='1'
        ).select_related(
            "schedule_bus_vo",
            "depart_locations_vo",
            "destination_locations_vo",
        )

        return render(
            request,
            "user/bookingForm.html",
            context,
        )

    except Exception as ex:
        print("Exception in user_load_bookingform:", ex)

        return render(
            request,
            "user/viewError.html",
            context={"message": ex},
        )

@login_required(login_url="admin_load_login")
@allowed_users(allowed_roles=["customer"])
def user_create_booking(request):
    try:
        if request.method != "POST":
            return redirect("user_load_findtrip")

        schedule_id = request.POST.get("scheduleId")
        booking_name = request.POST.get("name", "").strip()
        seats_value = request.POST.get("seats")

        if not schedule_id or not booking_name or not seats_value:
            return render(
                request,
                "user/viewError.html",
                context={
                    "message": "Please provide all booking details."
                },
            )

        try:
            requested_seats = int(seats_value)
        except (TypeError, ValueError):
            return render(
                request,
                "user/viewError.html",
                context={
                    "message": "Number of seats must be a valid number."
                },
            )

        if requested_seats < 1:
            return render(
                request,
                "user/viewError.html",
                context={
                    "message": "You must book at least one seat."
                },
            )

        MAX_SEATS_PER_USER = 4

        with transaction.atomic():

            schedule = get_object_or_404(
                ScheduleVO.objects.select_for_update().select_related(
                    "schedule_bus_vo",
                    "depart_locations_vo",
                    "destination_locations_vo",
                ),
                schedule_id=schedule_id,
                schedule_status='1',
            )

            # --------------------------------------------
            # 1. Check total bus availability
            # --------------------------------------------
            available_seats = schedule.count_available()

            if requested_seats > available_seats:
                return render(
                    request,
                    "user/viewError.html",
                    context={
                        "message":
                            f"Only {available_seats} seat(s) are currently available."
                    },
                )

            # --------------------------------------------
            # 2. Check how many seats THIS USER
            #    already booked for THIS schedule
            # --------------------------------------------
            already_booked = (
                    BookingsVO.objects.filter(
                        booking_user=request.user,
                        booking_schedule_vo=schedule,
                        booking_status__in=['1', '2'],
                    )
                    .aggregate(
                        total=Sum("booking_seats")
                    )["total"]
                    or 0
            )

            remaining_user_limit = (
                    MAX_SEATS_PER_USER - already_booked
            )

            # User already reached the limit
            if remaining_user_limit <= 0:
                messages.error(
                    request,
                    "You have already booked the maximum 4 seats for this trip."
                )

                return redirect(
                    f"{reverse('user_load_bookingform')}?scheduleId={schedule.schedule_id}"
                )

            # Requested seats would exceed the limit
            if requested_seats > remaining_user_limit:
                messages.error(
                    request,
                    f"You can book only {remaining_user_limit} more seat(s) "
                    f"for this trip."
                )

                return redirect(
                    f"{reverse('user_load_bookingform')}?scheduleId={schedule.schedule_id}"
                )

            # --------------------------------------------
            # 3. Generate booking code
            # --------------------------------------------
            booking_code = (
                    "BB-" + uuid.uuid4().hex[:10].upper()
            )

            # --------------------------------------------
            # 4. Create booking linked to logged-in user
            # --------------------------------------------
            booking = BookingsVO.objects.create(
                booking_code=booking_code,
                booking_name=booking_name,
                booking_user=request.user,
                booking_schedule_vo=schedule,
                booking_seats=requested_seats,
                booking_status='1',
            )

        return render(
            request,
            "user/bookingSuccess.html",
            context={
                "booking": booking,
                "schedule": schedule,
            },
        )

    except Exception as ex:
        print("Exception in user_create_booking:", ex)

        return render(
            request,
            "user/viewError.html",
            context={"message": ex},
        )

@login_required(login_url="admin_load_login")
@allowed_users(allowed_roles=["customer"])
def user_my_trips(request):

    bookings = (
        BookingsVO.objects
        .filter(
            booking_user=request.user
        )
        .select_related(
            "booking_schedule_vo",
            "booking_schedule_vo__schedule_bus_vo",
            "booking_schedule_vo__depart_locations_vo",
            "booking_schedule_vo__destination_locations_vo",
        )
        .order_by(
            "-booking_date_created"
        )
    )

    context = {
        "bookings": bookings,
        "page_title": "My Trips",
        "active_page": "my_trips",
    }

    return render(
        request,
        "user/myTrips.html",
        context
    )

@login_required(login_url="admin_load_login")
@allowed_users(allowed_roles=["customer"])
def user_view_ticket(request, booking_id):

    booking = get_object_or_404(
        BookingsVO.objects.select_related(
            "booking_user",
            "booking_schedule_vo",
            "booking_schedule_vo__schedule_bus_vo",
            "booking_schedule_vo__depart_locations_vo",
            "booking_schedule_vo__destination_locations_vo",
        ),
        booking_id=booking_id,
        booking_user=request.user,
        booking_status='2',
    )

    context = {
        "booking": booking,
        "schedule": booking.booking_schedule_vo,
        "page_title": "Ticket",
        "active_page": "my_trips",
    }

    return render(
        request,
        "user/ticket.html",
        context
    )
@login_required(login_url="admin_load_login")
@allowed_users(allowed_roles=["customer"])
@require_POST
def user_cancel_booking(request):

    booking_id = request.POST.get("bookingId")

    if not booking_id:
        messages.error(
            request,
            "Invalid booking."
        )
        return redirect("user_my_trips")

    booking = get_object_or_404(
        BookingsVO.objects.select_related(
            "booking_schedule_vo"
        ),
        booking_id=booking_id,
        booking_user=request.user,
    )

    # Only Pending bookings can be cancelled by customer.
    if booking.booking_status != '1':

        if booking.booking_status == '2':
            messages.error(
                request,
                "Paid bookings cannot be cancelled automatically."
            )

        elif booking.booking_status == '3':
            messages.info(
                request,
                "This booking has already been cancelled."
            )

        else:
            messages.error(
                request,
                "This booking cannot be cancelled."
            )

        return redirect("user_my_trips")


    # Do not allow cancellation after departure.
    if booking.booking_schedule_vo.trip_scheduled <= timezone.now():

        messages.error(
            request,
            "This booking cannot be cancelled because the trip has already departed."
        )

        return redirect("user_my_trips")


    booking.booking_status = '3'

    booking.save(
        update_fields=[
            "booking_status",
            "booking_date_updated",
        ]
    )


    messages.success(
        request,
        f"Booking {booking.booking_code} has been cancelled successfully."
    )

    return redirect("user_my_trips")
# def user_load_bookingform(request, schedPK=None, pk=None):
#
#     try:
#
#         schedule_vo_list = ScheduleVO.objects.filter(schedule_status= 1).all()
#         return render(request, "user/bookingform.html", context={
#             'schedule_vo_list': schedule_vo_list})
#
#     except Exception as ex:
#         print("in user_load_bookingform function exception occured>>>>>", ex)
#         return render(request, 'admin/viewError.html', context={'message': ex})
