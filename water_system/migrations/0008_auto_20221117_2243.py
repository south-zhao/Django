# Generated by Django 2.2.12 on 2022-11-17 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('water_system', '0007_auto_20221116_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workaction',
            name='record',
            field=models.ForeignKey(db_column='record', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='water_system.CustomerAction'),
        ),
    ]
