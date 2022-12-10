from django import forms
# from captcha.fields import CaptchaField  # 验证码验证模块
from .models import UserProfile
from django.core.exceptions import ValidationError  #错误管理


class RegisterForm(forms.Form):
    """注册信息验证"""
    email = forms.EmailField(required=True,max_length=30)
    password = forms.CharField(required=True, min_length=6, max_length=20)
    name = forms.CharField(required=True,max_length=20)
    r_password = forms.CharField(required=True, min_length=6, max_length=20)
    # captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

    def clean_pwd(self):
        val = self.cleaned_data.get('password')  # 先取值
        if val.isdigit():  # 判断是否是数字
            raise ValidationError("密码不能是纯数字")
        else:
            return val

    def clean(self):  # 全局钩子
        pwd = self.cleaned_data.get("password")
        r_pwd = self.cleaned_data.get("r_password")
        # 上面两个，有可能自带规则或自定义规则未通过，则get取值是空
        if pwd and r_pwd:  # 如果两个都通过了第一层说明clean_data中有值就是true
            if pwd == r_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            '''
            如果两个只要有其中一个不在clean_data里，那就没必要在比较了，
            因为本身就已经在errors里了
            '''
        return self.cleaned_data



class LoginForm(forms.Form):
    """登录信息验证"""
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20)


class ForgetpwdForm(forms.Form):
    """忘记密码信息验证"""
    email = forms.EmailField(required=True)
    # captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class PwdmodifyForm(forms.Form):
    """密码重置信息验证"""
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)

    def clean_pwd(self):
        val = self.cleaned_data.get('password1')  # 先取值
        if val.isdigit():  # 判断是否是数字
            raise ValidationError("密码不能是纯数字")
        else:
            return val

    def clean(self):  # 全局钩子
        pwd = self.cleaned_data.get("password1")
        r_pwd = self.cleaned_data.get("password2")
        # 上面两个，有可能自带规则或自定义规则未通过，则get取值是空
        if pwd and r_pwd:  # 如果两个都通过了第一层说明clean_data中有值就是true
            if pwd == r_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            '''
            如果两个只要有其中一个不在clean_data里，那就没必要在比较了，
            因为本身就已经在errors里了
            '''
        return self.cleaned_data


class UpUserInfoForm(forms.ModelForm):
    """个人中心的个人资料的修改"""

    class Meta:
        model = UserProfile
        fields = ['username']
