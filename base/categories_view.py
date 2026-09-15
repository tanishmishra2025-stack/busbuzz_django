from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .decorators import admin_only
from .models import CategoriesVO


# =========================================================
# ADMIN - INSERT CATEGORY
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_insert_categories(request):
    try:
        category_name = request.POST.get("categoryName", "").strip()
        category_description = request.POST.get(
            "categoryDescription",
            ""
        ).strip()
        category_status = request.POST.get("categoryStatus")

        if not category_name:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Category name is required."}
            )

        if category_status not in ["1", "2"]:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Invalid category status."}
            )

        CategoriesVO.objects.create(
            category_name=category_name,
            category_description=category_description,
            category_status=category_status,
        )

        return redirect("admin_view_categories")

    except Exception as ex:
        print("Exception in admin_insert_categories:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - VIEW CATEGORIES
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_view_categories(request):
    try:
        category_vo_list = CategoriesVO.objects.all()

        return render(
            request,
            "admin/viewCategories.html",
            context={"category_vo_list": category_vo_list}
        )

    except Exception as ex:
        print("Exception in admin_view_categories:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - EDIT CATEGORY
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
def admin_edit_categories(request):
    try:
        category_id = request.GET.get("categoryId")

        category_vo_list = CategoriesVO.objects.filter(
            category_id=category_id
        )

        return render(
            request,
            "admin/editCategories.html",
            context={
                "category_vo_list": category_vo_list
            }
        )

    except Exception as ex:
        print("Exception in admin_edit_categories:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )
# =========================================================
# ADMIN - UPDATE CATEGORY
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_update_categories(request):
    try:
        category_id = request.POST.get("categoryId")
        category_name = request.POST.get("categoryName", "").strip()
        category_description = request.POST.get(
            "categoryDescription",
            ""
        ).strip()
        category_status = request.POST.get("categoryStatus")

        if not category_name:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Category name is required."}
            )

        if category_status not in ["1", "2"]:
            return render(
                request,
                "admin/viewError.html",
                context={"message": "Invalid category status."}
            )

        category_vo = get_object_or_404(
            CategoriesVO,
            category_id=category_id
        )

        category_vo.category_name = category_name
        category_vo.category_description = category_description
        category_vo.category_status = category_status

        category_vo.save()

        return redirect("admin_view_categories")

    except Exception as ex:
        print("Exception in admin_update_categories:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )


# =========================================================
# ADMIN - DELETE CATEGORY
# =========================================================

@login_required(login_url="admin_load_login")
@admin_only
@require_POST
def admin_delete_categories(request):
    try:
        category_id = request.POST.get("categoryId")

        category_vo = get_object_or_404(
            CategoriesVO,
            category_id=category_id
        )

        category_vo.delete()

        return redirect("admin_view_categories")

    except Exception as ex:
        print("Exception in admin_delete_categories:", ex)
        return render(
            request,
            "admin/viewError.html",
            context={"message": ex}
        )