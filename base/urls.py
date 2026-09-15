from django.urls import path

from . import (
    login_view,
    categories_view,
    index_view,
    location_view,
    bus_view,
    schedule_view,
    booking_view,
    user_findtrip_view,
)
#conda activate busbuzz_py312

urlpatterns = [

    # =========================================================
    # ROOT / COMMON
    # =========================================================

    path(
        '',
        index_view.admin_load_home,
        name='admin_load_home'
    ),

    path(
        'admin/load_error500/',
        index_view.admin_load_error500,
        name='admin_load_error500'
    ),


    # =========================================================
    # AUTHENTICATION
    # =========================================================

    path(
        'admin/load_login/',
        login_view.admin_load_login,
        name='admin_load_login'
    ),

    path(
        'admin/load_logout/',
        login_view.admin_load_logout,
        name='admin_load_logout'
    ),

    path(
        'user/load_user/',
        login_view.user_load_user,
        name='user_load_user'
    ),


    # =========================================================
    # DASHBOARDS
    # =========================================================

    path(
        'admin/load_dashboard/',
        login_view.admin_load_dashboard,
        name='admin_load_dashboard'
    ),

    path(
        'user/load_dashboard/',
        login_view.user_load_dashboard,
        name='user_load_dashboard'
    ),


    # =========================================================
    # ADMIN - CATEGORIES
    # =========================================================

    path(
        'admin/load_categories/',
        index_view.admin_load_categories,
        name='admin_load_categories'
    ),

    path(
        'admin/insert_categories/',
        categories_view.admin_insert_categories,
        name='admin_insert_categories'
    ),

    path(
        'admin/view_categories/',
        categories_view.admin_view_categories,
        name='admin_view_categories'
    ),

    path(
        'admin/edit_categories/',
        categories_view.admin_edit_categories,
        name='admin_edit_categories'
    ),

    path(
        'admin/update_categories/',
        categories_view.admin_update_categories,
        name='admin_update_categories'
    ),

    path(
        'admin/delete_categories/',
        categories_view.admin_delete_categories,
        name='admin_delete_categories'
    ),


    # =========================================================
    # ADMIN - LOCATIONS
    # =========================================================

    path(
        'admin/load_locations/',
        location_view.admin_load_locations,
        name='admin_load_locations'
    ),

    path(
        'admin/insert_locations/',
        location_view.admin_insert_locations,
        name='admin_insert_locations'
    ),

    path(
        'admin/view_locations/',
        location_view.admin_view_locations,
        name='admin_view_locations'
    ),

    path(
        'admin/edit_locations/',
        location_view.admin_edit_locations,
        name='admin_edit_locations'
    ),

    path(
        'admin/update_locations/',
        location_view.admin_update_locations,
        name='admin_update_locations'
    ),

    path(
        'admin/delete_locations/',
        location_view.admin_delete_locations,
        name='admin_delete_locations'
    ),


    # =========================================================
    # ADMIN - BUSES
    # =========================================================

    path(
        'admin/load_bus/',
        bus_view.admin_load_bus,
        name='admin_load_bus'
    ),

    path(
        'admin/insert_bus/',
        bus_view.admin_insert_bus,
        name='admin_insert_bus'
    ),

    path(
        'admin/view_bus/',
        bus_view.admin_view_bus,
        name='admin_view_bus'
    ),

    path(
        'admin/edit_bus/',
        bus_view.admin_edit_bus,
        name='admin_edit_bus'
    ),

    path(
        'admin/update_bus/',
        bus_view.admin_update_bus,
        name='admin_update_bus'
    ),

    path(
        'admin/delete_buses/',
        bus_view.admin_delete_bus,
        name='admin_delete_bus'
    ),


    # =========================================================
    # ADMIN - SCHEDULES
    # =========================================================

    path(
        'admin/load_schedule/',
        schedule_view.admin_load_schedule,
        name='admin_load_schedule'
    ),

    path(
        'admin/insert_schedule/',
        schedule_view.admin_insert_schedule,
        name='admin_insert_schedule'
    ),

    path(
        'admin/view_schedule/',
        schedule_view.admin_view_schedule,
        name='admin_view_schedule'
    ),

    path(
        'admin/edit_schedule/',
        schedule_view.admin_edit_schedule,
        name='admin_edit_schedule'
    ),

    path(
        'admin/update_schedule/',
        schedule_view.admin_update_schedule,
        name='admin_update_schedule'
    ),

    path(
        'admin/delete_schedule/',
        schedule_view.admin_delete_schedule,
        name='admin_delete_schedule'
    ),


    # =========================================================
    # ADMIN - BOOKINGS
    # =========================================================

    path(
        'admin/load_managebooking/',
        booking_view.admin_load_booking,
        name='admin_view_managebooking'
    ),

    path(
        'admin/mark_booking_paid/',
        booking_view.admin_mark_booking_paid,
        name='admin_mark_booking_paid'
    ),


    # =========================================================
    # CUSTOMER - TRIP SEARCH
    # =========================================================

    path(
        'user/load_findtrip/',
        user_findtrip_view.user_load_findtrip,
        name='user_load_findtrip'
    ),

    path(
        'user/check_availability/',
        user_findtrip_view.user_check_availability,
        name='user_check_availability'
    ),


    # =========================================================
    # CUSTOMER - BOOKINGS
    # =========================================================

    path(
        'user/load_bookingform/',
        user_findtrip_view.user_load_bookingform,
        name='user_load_bookingform'
    ),

    path(
        'user/create_booking/',
        user_findtrip_view.user_create_booking,
        name='user_create_booking'
    ),

    path(
        'user/my_trips/',
        user_findtrip_view.user_my_trips,
        name='user_my_trips'
    ),

    path(
        'user/cancel_booking/',
        user_findtrip_view.user_cancel_booking,
        name='user_cancel_booking'
    ),

    path(
        'user/ticket/<int:booking_id>/',
        user_findtrip_view.user_view_ticket,
        name='user_view_ticket'
    ),


    # =========================================================
    # LEGACY / NEEDS REVIEW
    # =========================================================

    # This appears to belong to the older user registration flow.
    # Verify no active form posts here before removing.
    # path(
    #     'user/insert_user/',
    #     user_view.user_insert_user,
    #     name='user_insert_user'
    # ),

    # Legacy / unfinished bus-stop functionality.
    # Review before deciding whether it belongs in V1.
    # path(
    #     'admin/load_addbusstop/',
    #     index_view.admin_load_addbusstop,
    #     name='admin_load_addbusstop'
    # ),
]