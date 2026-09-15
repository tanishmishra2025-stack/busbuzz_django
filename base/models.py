from django.db import models
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum

# =========================================================
# LEGACY AUTHENTICATION MODELS
# =========================================================
#
# Retained for database/migration compatibility and project history.
# BusBuzz V1 uses Django's built-in User model and Groups instead.
# Do not use LoginVO or UserVO for new V1 functionality.

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2']
class LoginVO(models.Model):
    login_id = models.AutoField(db_column="login_id", primary_key=True,
                                null=False)
    login_username = models.CharField(db_column="login_username",
                                      max_length=200, default="", null=False)
    login_password = models.CharField(db_column="login_password",
                                      max_length=200, default="", null=False)
    login_role = models.CharField(db_column="login_role", max_length=10,
                                  default="", null=False)
    login_status = models.BooleanField(db_column="login_status", max_length=1,
                                       default="", null=False)

    def __str__(self):
        return '{} {} {}'.format(self.login_username,
                                 self.login_password,
                                 self.login_role, )

    def __as_dict__(self):
        return {
            "login_id": self.login_id,
            "login_username": self.login_username,
            "login_password": self.login_password,
            "login_role": self.login_role,
            "login_status": self.login_status
        }

    class Meta:
        db_table = "login_table"

class UserVO(models.Model):
    user_id = models.AutoField(db_column="user_id", primary_key=True,
                               null=False)
    user_firstname = models.CharField(db_column="user_firstname",
                                      max_length=200, default="", null=False)
    user_lastname = models.CharField(db_column="user_lastname", max_length=200,
                                     default="", null=False)
    user_email = models.EmailField(db_column="user_email", max_length=200, default="", null=False)

    user_password = models.CharField(db_column="user_password", max_length=200, default="", null=False)

    user_login_vo = models.ForeignKey(LoginVO, db_column="user_login_id",
                                      on_delete=models.CASCADE, default="")

    def __str__(self):
        return '{} {} {} {}'.format(self.user_firstname, self.user_lastname,
                                       self.user_email,
                                       self.user_password,)

    def __as_dict__(self):
        return {
            "user_id": self.user_id,
            "user_firstname": self.user_firstname,
            "user_lastname": self.user_lastname,
            "user_email": self.user_email,
            "user_password": self.user_password,
            "user_login_vo": self.user_login_vo,

            }

    class Meta:
        db_table = "user_table"

class CategoriesVO(models.Model):
    category_id = models.AutoField(db_column="category_id", primary_key=True,
                                   null=False,)
    category_name = models.CharField(
        db_column="category_name", max_length=255,
                                     default="", null=False)
    category_description = models.TextField(db_column="category_description",
                                            max_length=255, default="",
                                            null=False)

    category_status = models.CharField(db_column="category_status", max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)

    category_date_created = models.DateTimeField(db_column="category_date_created",
                                            default=timezone.now)

    category_date_updated = models.DateTimeField(db_column="category_date_updated",
                                            auto_now= True)

    def __str__(self):
        return '{}'.format(self.category_name,)

    def __as_dict__(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_description": self.category_description,
            "category_status": self.category_status,
            "category_date_created": self.category_date_created,
            "category_date_updated": self.category_date_updated,

             }

    class Meta:
        db_table = "categories_table"


class LocationsVO(models.Model):
    locations_id = models.AutoField(db_column="locations_id", primary_key=True,
                                   null=False)
    locations_name = models.CharField(db_column="locations_name",
                             max_length=255,
                                     default="", null=False)
    locations_date_created = models.DateTimeField(db_column="locations_date_created",
                                            default=timezone.now)
    locations_status = models.CharField(db_column="locations_status", max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)
    locations_date_updated = models.DateTimeField(db_column="locations_date_updated", auto_now=True)

    def __str__(self):
        return '{} '.format(self.locations_name,)

    def __as_dict__(self):
        return {
            "locations_id": self.locations_id,
            "locations_name": self.locations_name,
            "locations_status": self.locations_status,
            "locations_date_created": self.locations_date_created,
            "locations_date_updated": self.locations_date_updated,
               }

    class Meta:
        db_table = "locations_table"


class BusesVO(models.Model):
    bus_id = models.AutoField(db_column="bus_id", primary_key=True)

    bus_number = models.CharField(db_column="bus_number",
                                        max_length=255, default="",
                                        null=False)
    bus_seats = models.IntegerField(db_column="bus_seats", default=100,
                         null=False)
    bus_status = models.CharField(db_column="bus_status",
                                        max_length=2, choices=(
        ('1', 'Active'), ('2', 'Inactive')), default=1)
    bus_date_created = models.DateTimeField(
        db_column="bus_date_created",
        default=timezone.now)

    bus_date_updated = models.DateTimeField(
        db_column="bus_date_updated",
        auto_now=True)

    bus_category_vo = models.ForeignKey(CategoriesVO,
                                                on_delete=models.CASCADE,
                                                db_column="bus_category_id")

    def __str__(self):
        return '{} {}'.format(self.bus_number,
                              self.bus_seats)

    def __as_dict__(self):
        return {
            "bus_id": self.bus_id,
            "bus_number": self.bus_number,
            "bus_status": self.bus_status,
            "bus_seats": self.bus_seats,
            "bus_date_created": self.bus_date_created,
            "bus_date_updated": self.bus_date_updated,
            "bus_category_vo": self.bus_category_vo,
        }

    class Meta:
        db_table = "buses_table"

class ScheduleVO(models.Model):
    schedule_id = models.AutoField(db_column="schedule_id", primary_key=True)
    #schedule_code = models.CharField(db_column="",max_length=100 ,
    # default=True)
    trip_scheduled = models.DateTimeField(db_column="trip_scheduled",default=timezone.now)

    schedule_bus_vo = models.ForeignKey(BusesVO, on_delete=models.CASCADE, db_column="schedule_bus_id")
    depart_locations_vo = models.ForeignKey(LocationsVO, on_delete= models.CASCADE ,
                                            related_name='depart_schedules',
                               db_column="depart_locations_id")
    destination_locations_vo = models.ForeignKey(LocationsVO, on_delete=
    models.CASCADE,related_name='destination_schedules',
                                                 db_column="destination_locations_id")
    schedule_fare = models.FloatField(db_column="schedule_fare", default=0,
                                      null=False)
    schedule_status = models.CharField(db_column="schedule_status",
                                       max_length=2,
                                       choices=(('1', 'Active'), ('2', 'Cancelled')),
                                       default='1')
    trip_scheduled_date_created = models.DateTimeField(
        db_column="trip_scheduled_created", default=timezone.now)

    trip_scheduled_date_updated = models.DateTimeField(
        db_column="trip_scheduled_updated", auto_now=True)

    def __str__(self):
        return f"Schedule {self.schedule_id} - {self.schedule_bus_vo.bus_number}"


    def __as_dict__(self):
        return {
            "schedule_id": self.schedule_id,
            "trip_scheduled": self.trip_scheduled,
            "schedule_bus_vo": self.schedule_bus_vo,
            "depart_locations_vo": self.depart_locations_vo,
            "destination_locations_vo": self.destination_locations_vo,
            "schedule_fare": self.schedule_fare,
            "schedule_status": self.schedule_status,
            "trip_scheduled_date_created": self.trip_scheduled_date_created,
            "trip_scheduled_date_updated": self.trip_scheduled_date_updated,

        }
    # def count_available(self):
    #     booked = BookingVO.objects.filter(booking_schedule_vo=self).aggregate(Sum('bus_seats'))['seats__sum']
    #     return self.schedule_bus_vo.bus_seats - booked

    def count_available(self):
        booked_seats = BookingsVO.objects.filter(
            booking_schedule_vo=self,
            booking_status__in=['1', '2'],
        ).aggregate(
            total_booked=Sum('booking_seats')
        )['total_booked']

        if booked_seats is None:
            booked_seats = 0

        available_seats = self.schedule_bus_vo.bus_seats - booked_seats

        return max(available_seats, 0)
    class Meta:
        db_table = "schedule_table"

class BookingsVO(models.Model):
    booking_id = models.AutoField(
        db_column="booking_id",
        primary_key=True
    )

    booking_code = models.CharField(
        db_column="booking_code",
        max_length=100
    )

    booking_name = models.CharField(
        max_length=250,
        db_column="booking_name"
    )

    booking_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="booking_user_id",
    )

    booking_schedule_vo = models.ForeignKey(
        ScheduleVO,
        db_column="booking_schedule_id",
        on_delete=models.CASCADE
    )

    booking_seats = models.IntegerField(
        db_column="booking_seats",
        default=0
    )

    booking_status = models.CharField(
        db_column="booking_status",
        max_length=2,
        choices=(
            ('1', 'Pending'),
            ('2', 'Paid'),
            ('3', 'Cancelled'),
        ),
        default='1'
    )

    booking_date_created = models.DateTimeField(
        db_column="booking_date_created",
        default=timezone.now
    )

    booking_date_updated = models.DateTimeField(
        db_column="booking_date_updated",
        auto_now=True
    )

    def __str__(self):
        return str(
            self.booking_code + ' - ' + self.booking_name
        )

    def total_payable(self):
        return (
            self.booking_seats *
            self.booking_schedule_vo.schedule_fare
        )

    class Meta:
        db_table = "bookings_table"

