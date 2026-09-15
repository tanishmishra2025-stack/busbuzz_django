from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .decorators import admin_only
from .models import LocationsVO


# =========================================================
# ADMIN - LOAD ADD LOCATION
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_load_locations(request):
    try:
        return render(request, "admin/addLocation.html")

    except Exception as ex:
        print("Exception in admin_load_locations:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - INSERT LOCATION
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_insert_locations(request):
    try:
        locations_name = request.POST.get(
            "locationsName",
            ""
        ).strip()

        locations_status = request.POST.get("locationStatus")

        if not locations_name:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Location name is required."}
            )

        if locations_status not in ["1", "2"]:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Invalid location status."}
            )

        LocationsVO.objects.create(
            locations_name=locations_name,
            locations_status=locations_status,
        )

        return redirect("admin_view_locations")

    except Exception as ex:
        print("Exception in admin_insert_locations:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - VIEW LOCATIONS
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_view_locations(request):
    try:
        locations_vo_list = LocationsVO.objects.all()

        return render(
            request,
            "admin/viewLocations.html",
            context={"locations_vo_list": locations_vo_list}
        )

    except Exception as ex:
        print("Exception in admin_view_locations:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - EDIT LOCATION
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_edit_locations(request):
    try:
        locations_id = request.GET.get("locationsId")

        locations_vo_list = LocationsVO.objects.filter(
            locations_id=locations_id
        )

        return render(
            request,
            "admin/editLocations.html",
            context={"locations_vo_list": locations_vo_list}
        )

    except Exception as ex:
        print("Exception in admin_edit_locations:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - UPDATE LOCATION
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_update_locations(request):
    try:
        locations_id = request.POST.get("locationsId")

        locations_name = request.POST.get(
            "locationsName",
            ""
        ).strip()

        locations_status = request.POST.get("locationStatus")

        if not locations_name:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Location name is required."}
            )

        if locations_status not in ["1", "2"]:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Invalid location status."}
            )

        locations_vo = get_object_or_404(
            LocationsVO,
            locations_id=locations_id
        )

        locations_vo.locations_name = locations_name
        locations_vo.locations_status = locations_status

        locations_vo.save()

        return redirect("admin_view_locations")

    except Exception as ex:
        print("Exception in admin_update_locations:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - DELETE LOCATION
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_delete_locations(request):
    try:
        locations_id = request.POST.get("locationsId")

        locations_vo = get_object_or_404(
            LocationsVO,
            locations_id=locations_id
        )

        locations_vo.delete()

        return redirect("admin_view_locations")

    except Exception as ex:
        print("Exception in admin_delete_locations:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )