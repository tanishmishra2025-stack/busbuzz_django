from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_add_booking_schedule_fk"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE bookings_table
                MODIFY COLUMN booking_code VARCHAR(100) NOT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]