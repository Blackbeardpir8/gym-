# Generated by Django 5.1 on 2024-09-10 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_alter_enrollment_date_of_joining'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('select_date', models.DateField()),
                ('login', models.TimeField()),
                ('logout', models.TimeField()),
                ('select_workout', models.CharField(max_length=100)),
                ('trained_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authapp.trainer')),
            ],
        ),
    ]
