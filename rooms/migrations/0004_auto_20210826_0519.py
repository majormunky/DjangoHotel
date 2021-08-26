# Generated by Django 3.2.4 on 2021-08-26 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_room_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='bed',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bed',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
