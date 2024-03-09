# Generated by Django 5.0.3 on 2024-03-09 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiUFC', '0006_lutadormodel_cartel_alter_lutadormodel_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lutadormodel',
            name='cartel',
        ),
        migrations.AddField(
            model_name='lutadormodel',
            name='cartelNoUFC',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Cartel do lutador no UFC: v-d-nc'),
        ),
    ]