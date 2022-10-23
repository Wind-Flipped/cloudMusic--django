import random  # 随机模块
import string  # python自带的字符串模块

from django.core.mail import send_mail

from users.models import EmailVerification
from cloudMusic_master.settings import EMAIL_FROM  # 引入自定义的配置


def send_link_email(email, send_type='register'):
    """发送邮件，内容为验证链接"""
    emailinfo = EmailVerification()
    emailinfo.email = email
    emailinfo.send_type = send_type
    emailinfo.code = send_code_email()
    if send_type == 'register':
        email_subject = '高山流水觅知音网站激活邮件（请勿回复）'
        email_message = '欢迎您注册高山流水觅知音网站账号，请点击下面的链接完成激活:\nhttp://127' \
                        '.0.0.1:8000/users/active/' + emailinfo.code
        send_mail(email_subject, email_message, EMAIL_FROM, [email])
        emailinfo.save()
    elif send_type == 'forget':
        email_subject = '高山流水觅知音网站密码重置邮件（请勿回复）'
        email_message = '欢迎您使用高山流水觅知音网站平台，请点击下面的链接重置登录密码:\nhttp://127' \
                        '.0.0.1:8000/users/pwdreset/' + emailinfo.code
        send_mail(email_subject, email_message, EMAIL_FROM, [email])
        emailinfo.save()
    elif send_type == 'update_email':
        pass


def send_code_email(link_code_length=16):
    """生成随机邮箱验证码，作为验证链接的一部分"""
    link_code = ''
    chars = string.ascii_letters + str(string.digits)
    chars_length = len(chars)
    for i in range(link_code_length-1):
        link_code += chars[random.randint(0, chars_length-1)]
    return link_code
