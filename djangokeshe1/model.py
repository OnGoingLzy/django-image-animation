from django.db import models

# 利用django的inspectdb，django通过setting当中的database配置信息找到数据库表，并输出到默认输出设备
#
# python .\manage.py inspectdb
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Sum


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


class Chat(models.Model):
    sender = models.ForeignKey('User', models.DO_NOTHING)
    receiver = models.ForeignKey('User', models.DO_NOTHING)
    message = models.TextField()
    sent_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'chat'


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


class ChatCountManager(models.Manager):
    pass


class ChatCount(models.Model):
    user_id = models.IntegerField()
    chat_date = models.DateField()
    count = models.IntegerField()

    class Meta:
        db_table = 'chat_count'
        unique_together = (('user_id', 'chat_date'),)
        managed = False


class Message(models.Model):
    conversation_id = models.IntegerField()
    message_text = models.TextField()
    is_generated = models.IntegerField()

    class Meta:
        managed = False


class Conversation(models.Model):
    user_id = models.IntegerField()
    start_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'conversation'


class Order(models.Model):
    userid = models.IntegerField()
    order_id = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=3)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order'


class User(models.Model):
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11, blank=True)
    password = models.CharField(max_length=50)
    chat_count = models.IntegerField()
    is_premium = models.IntegerField()
    premium_start_date = models.DateField(blank=True, null=True)
    premium_end_date = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'phone_number'

    # def register(self):
    #     # 检查是否已存在相同电话号码的用户
    #     if User.objects.filter(phone_number=self.phone_number).exists():
    #         return False  # 如果存在，返回False表示创建失败
    #     self.save()
    #     return True

    def check_password(self, raw_password):
        """
        使用给定的密码检查用户密码是否匹配。
        """
        return raw_password == self.password

    class Meta:
        managed = False
        db_table = 'user'


