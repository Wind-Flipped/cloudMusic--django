from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime
# Create your models here.
class UserProfile(AbstractUser):
    user_id = models.AutoField(primary_key=True, verbose_name="用户id")
    # user_name = models.CharField(max_length=20, verbose_name="用户名", null=False)
    # user_password = models.CharField(max_length=20, verbose_name="密码", null=False)
    user_exp = models.IntegerField(verbose_name="经验值", null=False, default=0)
    user_rank = models.IntegerField(verbose_name="用户等级", null=False, default=1)
    user_create_time = models.DateField(verbose_name="用户创建时间", null=False, auto_now_add=False)
    user_is_admin = models.BooleanField(verbose_name="是否为管理员", null=False, default=False)
    # user_email = models.EmailField(verbose_name="用户邮箱", null=False)

    class Meta:
        managed = True;
        db_table = "user_profile"

class EmailVerification(models.Model):
    """邮箱验证相关"""
    email = models.EmailField(max_length=50, null=True, verbose_name='邮箱')
    code = models.CharField(max_length=50, verbose_name='验证信息')
    send_type = models.CharField(max_length=20, verbose_name='验证码类型',
                                 choices=(('register', '注册'), ('forget', '修改密码'), ('update_email', '修改邮箱')),
                                 default='register')
    send_time = models.DateTimeField(verbose_name='添加时间', default=datetime.datetime.now)
    is_delete = models.BooleanField(verbose_name='是否已验证', default=False)

    class Meta:
        verbose_name = '邮箱验证信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email