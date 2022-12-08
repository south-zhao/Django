# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AddrArea(models.Model):
    id = models.IntegerField(primary_key=True)
    addr = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.addr

    area = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addr_area'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.ForeignKey('User', models.DO_NOTHING, db_column='name', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    tele = models.CharField(max_length=255, blank=True, null=True)
    addr = models.CharField(max_length=255, blank=True, null=True)
    num = models.IntegerField()
    wid = models.ForeignKey('Water', models.DO_NOTHING, db_column='wid', blank=True, null=True)
    work = models.ForeignKey('Work', models.DO_NOTHING, to_field='area', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customer'


class CustomerAction(models.Model):
    record = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.record

    id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    kind = models.ForeignKey('Water', models.DO_NOTHING, db_column='kind', blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customer_action'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Money(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.id

    b_fee = models.IntegerField()
    s_fee = models.IntegerField()
    profit = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'money'


class Provider(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    wid = models.ForeignKey('Water', models.DO_NOTHING, db_column='wid', blank=True, null=True)
    supply = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'provider'


class ProviserAction(models.Model):
    record = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.record)

    supplier = models.ForeignKey(Provider, models.DO_NOTHING, db_column='supplier', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    kind = models.IntegerField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'proviser_action'


class RootS(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'root_s'


class StoreHouse(models.Model):
    sid = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.sid)

    wid = models.ForeignKey('Water', models.DO_NOTHING, db_column='wid', blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)
    input = models.IntegerField(blank=True, null=True)
    output = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'store house'


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = 'user'


class Water(models.Model):
    wid = models.AutoField(primary_key=True)

    def __str__(self):
        return self.type

    type = models.CharField(max_length=255, blank=True, null=True)
    buy = models.IntegerField(blank=True, null=True)
    sell = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'water'


class Work(models.Model):
    wid = models.AutoField(primary_key=True)
    area = models.IntegerField(blank=True, null=True, unique=True)

    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    tele = models.CharField(max_length=30, blank=True, null=True)
    total = models.IntegerField()
    b_time = models.TimeField(blank=True, null=True)
    f_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'work'


class WorkAction(models.Model):
    record = models.ForeignKey(CustomerAction, models.DO_NOTHING, db_column='record', primary_key=True)

    def __str__(self):
        return str(self.record)

    id = models.ForeignKey(Work, models.DO_NOTHING, db_column='id', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    tele = models.CharField(max_length=255, blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    c_id = models.IntegerField(blank=True, null=True)
    c_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'work_action'
