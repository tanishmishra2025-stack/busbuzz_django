from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .decorators import admin_only
from .models import BusesVO, LocationsVO, ScheduleVO
@login_required(login_url="admin_load_login")
@admin_only
def admin_load_schedule(request):
    try:
        locations_vo_list = LocationsVO.objects.filter(
            locations_status="1"
        )

        buses_vo_list = BusesVO.objects.filter(
            bus_status="1"
        )

        return render(
            request,
            "admin/addSchedule.html",
            context={
                "buses_vo_list": buses_vo_list,
                "locations_vo_list": locations_vo_list,
            },
        )

    except Exception as ex:
        print("Exception in admin_load_schedule:", ex)

        return render(
            request,
            "admin/viewError.html",
            context={"message": ex},
        )


@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_insert_schedule(request):
    try:

        trip_scheduled = request.POST.get("tripScheduled")
        schedule_fare = request.POST.get("scheduleFare")
        schedule_status = request.POST.get("scheduleStatus", "1")
        if schedule_status not in ["1", "2"]:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Invalid schedule status."},
            )

        try:
            schedule_fare = float(schedule_fare)
        except (TypeError, ValueError):
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Fare must be a valid number."},
            )

        if schedule_fare < 0:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Fare cannot be negative."},
            )
        schedule_bus_id = request.POST.get("scheduleBusId")
        depart_locations_id = request.POST.get("departLocationsId")
        destination_locations_id = request.POST.get(
            "destinationLocationsId"
        )

        # Basic server-side validation
        if not all(
            [
                trip_scheduled,
                schedule_fare,
                schedule_bus_id,
                depart_locations_id,
                destination_locations_id,
            ]
        ):
            return render(
                request,
                "admin/viewError.html",
                context={
                    "message": "All schedule fields are required."
                },
            )

        if depart_locations_id == destination_locations_id:
            return render(
                request,
                "admin/viewError.html",
                context={
                    "message": (
                        "Departure and destination "
                        "locations cannot be the same."
                    )
                },
            )

        buses_vo = get_object_or_404(
            BusesVO,
            bus_id=schedule_bus_id,
        )

        depart_location_vo = get_object_or_404(
            LocationsVO,
            locations_id=depart_locations_id,
        )

        destination_location_vo = get_object_or_404(
            LocationsVO,
            locations_id=destination_locations_id,
        )

        ScheduleVO.objects.create(
            trip_scheduled=trip_scheduled,
            schedule_fare=schedule_fare,
            schedule_status=schedule_status,
            schedule_bus_vo=buses_vo,
            depart_locations_vo=depart_location_vo,
            destination_locations_vo=destination_location_vo,
        )

        return redirect("admin_view_schedule")

    except Exception as ex:
        print("Exception in admin_insert_schedule:", ex)

        return render(
            request,
            "admin/viewError.html",
            context={"message": ex},
        )


@login_required(login_url="admin_load_login")
@admin_only
def admin_view_schedule(request):
    try:
        schedule_vo_list = ScheduleVO.objects.select_related(
            "schedule_bus_vo",
            "depart_locations_vo",
            "destination_locations_vo",
        ).all()

        return render(
            request,
            "admin/viewSchedule.html",
            context={
                "schedule_vo_list": schedule_vo_list
            },
        )

    except Exception as ex:
        print("Exception in admin_view_schedule:", ex)

        return render(
            request,
            "admin/viewError.html",
            context={"message": ex},
        )

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_delete_schedule(request):
    try:

        schedule_id = request.POST.get("scheduleId")

        schedule_vo = get_object_or_404(
            ScheduleVO,
            schedule_id=schedule_id,
        )

        schedule_vo.delete()

        return redirect("admin_view_schedule")

    except Exception as ex:
        print("Exception in admin_delete_schedule:", ex)

        return render(
            request,
            "admin/viewError.html",
            context={"message": ex},
        )

@login_required(login_url="admin_load_login")
@admin_only
def admin_edit_schedule(request):
    try:
        schedule_id = request.GET.get("scheduleId")

        schedule_vo = get_object_or_404(
            ScheduleVO.objects.select_related(
                "schedule_bus_vo",
                "depart_locations_vo",
                "destination_locations_vo",
            ),
            schedule_id=schedule_id,
        )

        buses_vo_list = BusesVO.objects.all()

        locations_vo_list = LocationsVO.objects.all()

        context = {
            "schedule_vo": schedule_vo,

            # Keep this temporarily because the current
            # editSchedule.html may still loop over it.
            "schedule_vo_list": [schedule_vo],

            "buses_vo_list": buses_vo_list,
            "locations_vo_list": locations_vo_list,
        }

        return render(
            request,
            "admin/editSchedule.html",
            context,
        )

    except Exception as ex:
        print("Exception in admin_edit_schedule:", ex)

        return render(
            request,
            "admin/viewError.html",
            context={"message": ex},
        )


@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_update_schedule(request):
    try:
        schedule_id = request.POST.get("scheduleId")

        trip_scheduled = request.POST.get("tripScheduled")
        schedule_fare = request.POST.get("scheduleFare")
        schedule_status = request.POST.get("scheduleStatus")
        if schedule_status not in ["1", "2"]:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Invalid schedule status."},
            )

        try:
            schedule_fare = float(schedule_fare)
        except (TypeError, ValueError):
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Fare must be a valid number."},
            )

        if schedule_fare < 0:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Fare cannot be negative."},
            )
        schedule_bus_id = request.POST.get("scheduleBusId")
        depart_locations_id = request.POST.get("departLocationsId")
        destination_locations_id = request.POST.get(
            "destinationLocationsId"
        )

        if not all(
            [
                schedule_id,
                trip_scheduled,
                schedule_fare,
                schedule_status,
                schedule_bus_id,
                depart_locations_id,
                destination_locations_id,
            ]
        ):
            return render(
                request,
                "admin/viewError.html",
                context={
                    "message": "All schedule fields are required."
                },
            )

        if depart_locations_id == destination_locations_id:
            return render(
                request,
                "admin/viewError.html",
                context={
                    "message": (
                        "Departure and destination "
                        "locations cannot be the same."
                    )
                },
            )

        schedule_vo = get_object_or_404(
            ScheduleVO,
            schedule_id=schedule_id,
        )

        buses_vo = get_object_or_404(
            BusesVO,
            bus_id=schedule_bus_id,
        )

        depart_location_vo = get_object_or_404(
            LocationsVO,
            locations_id=depart_locations_id,
        )

        destination_location_vo = get_object_or_404(
            LocationsVO,
            locations_id=destination_locations_id,
        )

        # Update the existing ScheduleVO.
        # Do NOT create another ScheduleVO or BusesVO.
        schedule_vo.trip_scheduled = trip_scheduled
        schedule_vo.schedule_fare = schedule_fare
        schedule_vo.schedule_status = schedule_status

        schedule_vo.schedule_bus_vo = buses_vo
        schedule_vo.depart_locations_vo = depart_location_vo
        schedule_vo.destination_locations_vo = (
            destination_location_vo
        )

        schedule_vo.save()

        return redirect("admin_view_schedule")

    except Exception as ex:
        print("Exception in admin_update_schedule:", ex)

        return render(
            request,
            "admin/viewError.html",
            context={"message": ex},
        )