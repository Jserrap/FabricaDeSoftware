# Generated by Django 5.0.3 on 2024-03-09 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiUFC', '0002_remove_lutadormodel_ultimaluta_lutadormodel_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lutadormodel',
            name='data',
        ),
        migrations.RemoveField(
            model_name='lutadormodel',
            name='evento',
        ),
        migrations.RemoveField(
            model_name='lutadormodel',
            name='lutador1',
        ),
        migrations.RemoveField(
            model_name='lutadormodel',
            name='lutador2',
        ),
        migrations.RemoveField(
            model_name='lutadormodel',
            name='metodo',
        ),
        migrations.RemoveField(
            model_name='lutadormodel',
            name='rounds',
        ),
        migrations.RemoveField(
            model_name='lutadormodel',
            name='vencedor',
        ),
        migrations.AddField(
            model_name='lutadormodel',
            name='ultimaLuta',
            field=models.JSONField(blank=True, max_length=500, null=True, verbose_name='ultimaLuta'),
        ),
    ]
