# Generated by Django 5.0.6 on 2024-07-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_saler_reg_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
