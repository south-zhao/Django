# Generated by Django 2.2.12 on 2022-10-28 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water_system', '0004_addrarea'),
    ]

    operations = [
        migrations.CreateModel(
            name='RootS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'root_s',
                'managed': True,
            },
        ),
    ]
