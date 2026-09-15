from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .decorators import admin_only
from .models import CategoriesVO, BusesVO


# =========================================================
# ADMIN - LOAD ADD BUS
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_load_bus(request):
    try:
        category_vo_list = CategoriesVO.objects.filter(
            category_status='1'
        )

        return render(
            request,
            "admin/addBus.html",
            context={"category_vo_list": category_vo_list}
        )

    except Exception as ex:
        print("Exception in admin_load_bus:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - INSERT BUS
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_insert_bus(request):
    try:
        bus_number = request.POST.get(
            "busesNumber",
            ""
        ).strip()

        bus_seats = request.POST.get(
            "busesSeats",
            ""
        ).strip()

        bus_status = request.POST.get("busesStatus")
        bus_category_id = request.POST.get("busesCategoryId")

        # -----------------------------
        # Validation
        # -----------------------------

        if not bus_number:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Bus number is required."}
            )

        if not bus_seats:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Number of seats is required."}
            )

        try:
            bus_seats = int(bus_seats)
        except (TypeError, ValueError):
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Bus seats must be a valid number."}
            )

        if bus_seats <= 0:
            return render(
                request,
                "admin/viewError.html",
                context={
                    "message": "Bus seats must be greater than zero."
                }
            )

        if bus_status not in ["1", "2"]:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Invalid bus status."}
            )

        if not bus_category_id:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Bus category is required."}
            )

        category_vo = get_object_or_404(
            CategoriesVO,
            category_id=bus_category_id
        )

        # -----------------------------
        # Create Bus
        # -----------------------------

        BusesVO.objects.create(
            bus_number=bus_number,
            bus_seats=bus_seats,
            bus_status=bus_status,
            bus_category_vo=category_vo,
        )

        return redirect("admin_view_bus")

    except Exception as ex:
        print("Exception in admin_insert_bus:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - VIEW BUSES
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_view_bus(request):
    try:
        buses_vo_list = (
            BusesVO.objects
            .select_related("bus_category_vo")
            .all()
        )

        return render(
            request,
            "admin/viewBuses.html",
            context={"buses_vo_list": buses_vo_list}
        )

    except Exception as ex:
        print("Exception in admin_view_bus:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - EDIT BUS
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_edit_bus(request):
    try:
        bus_id = request.GET.get("busId")

        buses_vo_list = BusesVO.objects.filter(
            bus_id=bus_id
        )

        category_vo_list = CategoriesVO.objects.all()

        context = {
            "buses_vo_list": buses_vo_list,
            "category_vo_list": category_vo_list,
        }

        return render(
            request,
            "admin/editBus.html",
            context
        )

    except Exception as ex:
        print("Exception in admin_edit_bus:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - UPDATE BUS
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_update_bus(request):
    try:
        bus_id = request.POST.get("busId")

        bus_number = request.POST.get(
            "busesNumber",
            ""
        ).strip()

        bus_seats = request.POST.get(
            "busesSeats",
            ""
        ).strip()

        bus_status = request.POST.get("busesStatus")
        bus_category_id = request.POST.get("busesCategoryId")

        # -----------------------------
        # Validation
        # -----------------------------

        if not bus_number:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Bus number is required."}
            )

        if not bus_seats:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Number of seats is required."}
            )

        try:
            bus_seats = int(bus_seats)
        except (TypeError, ValueError):
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Bus seats must be a valid number."}
            )

        if bus_seats <= 0:
            return render(
                request,
                "admin/viewError.html",
                context={
                    "message": "Bus seats must be greater than zero."
                }
            )

        if bus_status not in ["1", "2"]:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Invalid bus status."}
            )

        if not bus_category_id:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Bus category is required."}
            )

        # -----------------------------
        # Get Existing Records
        # -----------------------------

        buses_vo = get_object_or_404(
            BusesVO,
            bus_id=bus_id
        )

        category_vo = get_object_or_404(
            CategoriesVO,
            category_id=bus_category_id
        )

        # -----------------------------
        # Update Existing Bus
        # -----------------------------

        buses_vo.bus_number = bus_number
        buses_vo.bus_seats = bus_seats
        buses_vo.bus_status = bus_status
        buses_vo.bus_category_vo = category_vo

        buses_vo.save()

        return redirect("admin_view_bus")

    except Exception as ex:
        print("Exception in admin_update_bus:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - DELETE BUS
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_delete_bus(request):
    try:
        bus_id = request.POST.get("busId")

        buses_vo = get_object_or_404(
            BusesVO,
            bus_id=bus_id
        )

        buses_vo.delete()

        return redirect("admin_view_bus")

    except Exception as ex:
        print("Exception in admin_delete_bus:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )