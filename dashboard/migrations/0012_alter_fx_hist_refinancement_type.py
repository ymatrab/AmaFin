# Generated by Django 5.2 on 2025-05-19 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_alter_fx_hist_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fx_hist',
            name='refinancement_type',
            field=models.CharField(editable=False),
        ),
    ]
