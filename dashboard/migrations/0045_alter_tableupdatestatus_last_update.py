# Generated by Django 5.2 on 2025-06-24 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0044_alter_escompte_date_de_payement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableupdatestatus',
            name='last_update',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
    ]
