# Generated by Django 5.1 on 2024-09-07 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_alter_enrollment_payment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='reference',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
