# Generated by Django 2.2.12 on 2022-11-16 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('water_system', '0006_auto_20221116_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='work',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='water_system.Work', to_field='area'),
        ),
    ]
