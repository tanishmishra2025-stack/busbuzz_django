from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .decorators import admin_only


# =========================================================
# ROOT / COMMON
# =========================================================

def admin_load_home(request):
    if request.user.is_authenticated:

        if request.user.groups.filter(name='admin').exists():
            return redirect('admin_load_dashboard')

        if request.user.groups.filter(name='customer').exists():
            return redirect('user_load_dashboard')

    return redirect('admin_load_login')


def admin_load_error500(request):
    try:
        return render(request, "admin/viewError500.html")

    except Exception as ex:
        print("Exception in admin_load_error500:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - CATEGORIES
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_load_categories(request):
    try:
        return render(request, "admin/addCategories.html")

    except Exception as ex:
        print("Exception in admin_load_categories:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )

# =========================================================
# LEGACY / DEFERRED FUNCTIONALITY
# =========================================================

# BusBuzz originally included a bus-stop / area management feature.
# The workflow was incomplete and is intentionally excluded from V1.
# Its old admin_load_addbusstop view and URL are not exposed.
# This functionality may be redesigned for a future BusBuzz version.
