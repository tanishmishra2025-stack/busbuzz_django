from django.contrib import admin

from . models import (LoginVO, UserVO, CategoriesVO, LocationsVO, BusesVO,
                    ScheduleVO, BookingsVO)
# Register your models here.
admin.site.register(LoginVO)
admin.site.register(UserVO)
admin.site.register(CategoriesVO)
admin.site.register(LocationsVO)
admin.site.register(BusesVO)
admin.site.register(ScheduleVO)
admin.site.register(BookingsVO)