from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='admin').exists():
                return redirect("admin_load_dashboard")
            if request.user.groups.filter(name='customer').exists():
                return redirect("user_load_dashboard")

            return HttpResponseForbidden("Your account does not have "
                                         "an assigned role.")
        return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden('You are not authorized to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    @wraps(view_func)
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.filter(name="admin").exists():
            return view_func(request, *args, **kwargs)

        if request.user.groups.filter(name="customer").exists():
            return redirect("user_load_dashboard")

        return HttpResponseForbidden('You are not authorized to view this page')

    return wrapper_function