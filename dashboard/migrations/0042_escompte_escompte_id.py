# Generated by Django 5.2 on 2025-06-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0041_escompte'),
    ]

    operations = [
        migrations.AddField(
            model_name='escompte',
            name='escompte_id',
            field=models.IntegerField(default=1, editable=False, unique=True, verbose_name='Code Escompte'),
            preserve_default=False,
        ),
    ]
