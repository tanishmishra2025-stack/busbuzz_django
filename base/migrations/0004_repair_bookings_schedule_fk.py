from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_remove_schedulevo_schedule_code"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE bookings_table
                ADD COLUMN booking_schedule_id INT NOT NULL;
            """,
            reverse_sql="""
                ALTER TABLE bookings_table
                DROP COLUMN booking_schedule_id;
            """,
        ),
    ]