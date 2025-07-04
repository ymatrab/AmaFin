# Generated by Django 5.2 on 2025-05-19 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_alter_fx_hist_refinancement_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incomes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enregistrement', models.DateField()),
                ('societe', models.CharField(choices=[('ENOSIS', 'ENOSIS'), ('AMAP', 'AMAP'), ('AMAD', 'AMAD'), ('SULFO', 'SULFO'), ('ENGINUP', 'ENGINUP'), ('FMCG', 'FMCG'), ('LAC', 'LAC'), ('TODAYWORKS', 'TODAYWORKS')], max_length=20)),
                ('document', models.CharField(choices=[('Facture', 'Facture'), ('Avance', 'Avance')], max_length=10)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=20)),
                ('week', models.DateField()),
                ('banque', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.bank')),
            ],
        ),
    ]
