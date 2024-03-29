# Generated by Django 5.0.3 on 2024-03-08 22:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UltimaLutaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True, null=True)),
                ('evento', models.CharField(blank=True, max_length=50, null=True, verbose_name='Evento')),
                ('lutador1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome do lutador')),
                ('lutador2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome do lutador')),
                ('vencedor', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vencedor')),
                ('rounds', models.IntegerField(blank=True, null=True, verbose_name='Round')),
                ('metodo', models.CharField(blank=True, max_length=150, null=True, verbose_name='Método de vitória')),
            ],
        ),
        migrations.CreateModel(
            name='LutadorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome do lutador')),
                ('ultimaLuta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiUFC.ultimalutamodel')),
            ],
        ),
    ]
