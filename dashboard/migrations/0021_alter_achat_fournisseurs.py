# Generated by Django 5.2 on 2025-05-20 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_alter_engagement_invoice_remove_achat_date_echeance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat',
            name='fournisseurs',
            field=models.CharField(max_length=255, verbose_name='Fournisseurs'),
        ),
    ]
