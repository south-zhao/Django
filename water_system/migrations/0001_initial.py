# Generated by Django 4.1.1 on 2022-10-26 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('tele', models.CharField(blank=True, max_length=255, null=True)),
                ('addr', models.CharField(blank=True, max_length=255, null=True)),
                ('num', models.IntegerField()),
            ],
            options={
                'db_table': 'customer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_fee', models.IntegerField()),
                ('s_fee', models.IntegerField()),
                ('profit', models.IntegerField()),
            ],
            options={
                'db_table': 'money',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('supply', models.IntegerField()),
            ],
            options={
                'db_table': 'provider',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Water',
            fields=[
                ('wid', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('buy', models.IntegerField(blank=True, null=True)),
                ('sell', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'water',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('wid', models.AutoField(primary_key=True, serialize=False)),
                ('area', models.IntegerField(blank=True, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('tele', models.CharField(blank=True, max_length=30, null=True)),
                ('total', models.IntegerField()),
                ('b_time', models.TimeField(blank=True, null=True)),
                ('f_time', models.TimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'work',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='WorkAction',
            fields=[
                ('record', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('c_id', models.IntegerField(blank=True, null=True)),
                ('c_name', models.CharField(blank=True, max_length=255, null=True)),
                ('id', models.ForeignKey(blank=True, db_column='id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='water_system.work')),
            ],
            options={
                'db_table': 'work_action',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StoreHouse',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False)),
                ('sum', models.IntegerField(blank=True, null=True)),
                ('input', models.IntegerField(blank=True, null=True)),
                ('output', models.IntegerField(blank=True, null=True)),
                ('wid', models.ForeignKey(blank=True, db_column='wid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='water_system.water')),
            ],
            options={
                'db_table': 'store house',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProviserAction',
            fields=[
                ('record', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('kind', models.IntegerField(blank=True, null=True)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('money', models.IntegerField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('supplier', models.ForeignKey(blank=True, db_column='supplier', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='water_system.provider')),
            ],
            options={
                'db_table': 'proviser_action',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='provider',
            name='wid',
            field=models.ForeignKey(blank=True, db_column='wid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='water_system.water'),
        ),
        migrations.CreateModel(
            name='CustomerAction',
            fields=[
                ('record', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('kind', models.IntegerField(blank=True, null=True)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('money', models.IntegerField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('id', models.ForeignKey(blank=True, db_column='id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='water_system.customer')),
            ],
            options={
                'db_table': 'customer_action',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='wid',
            field=models.ForeignKey(blank=True, db_column='wid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='water_system.water'),
        ),
        migrations.AddField(
            model_name='customer',
            name='work',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='water_system.work', to_field='area'),
        ),
    ]
