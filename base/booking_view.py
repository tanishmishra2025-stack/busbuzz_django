from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .decorators import admin_only
from .models import BookingsVO


@login_required(login_url='admin_load_login')
@admin_only
def admin_load_booking(request):
    try:

        bookings = (
            BookingsVO.objects
            .select_related(
                "booking_user",
                "booking_schedule_vo",
                "booking_schedule_vo__schedule_bus_vo",
                "booking_schedule_vo__depart_locations_vo",
                "booking_schedule_vo__destination_locations_vo",
            )
            .order_by("-booking_date_created")
        )

        context = {
            "bookings": bookings,
            "active_page": "manage_booking",
        }

        return render(
            request,
            "admin/viewBookings.html",
            context
        )

    except Exception as ex:
        print("Exception in admin_load_booking:", ex)

        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


@login_required(login_url='admin_load_login')
@admin_only
@require_POST
def admin_mark_booking_paid(request):
    try:

        booking_id = request.POST.get("bookingId")

        booking = get_object_or_404(
            BookingsVO,
            booking_id=booking_id
        )

        if booking.booking_status == '1':
            booking.booking_status = '2'
            booking.save(update_fields=["booking_status"])

        return redirect("admin_view_managebooking")

    except Exception as ex:
        print("Exception in admin_mark_booking_paid:", ex)

        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )