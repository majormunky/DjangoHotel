# Generated by Django 3.2.4 on 2021-07-28 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_booking_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='check_in_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
