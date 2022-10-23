from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from .forms import RegisterForm, LoginForm, PwdmodifyForm, ForgetpwdForm, UpUserInfoForm
from .models import UserProfile, EmailVerification
from django.contrib.auth.hashers import make_password  # 密码
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from utils.email_send import send_link_email  # 邮箱
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.
import re
import json


class IndexView(View):
    """显示首页"""

    def get(self, request):
        return render(request, 'index.html')


class RegisterView(View):
    """用户注册功能"""

    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  # 正则验证有效性

    # TODO 考虑直接发邮件，验证码
    @classmethod
    def isValid(email):
        if re.fullmatch(RegisterView.regex, email):
            return True
        else:
            return False

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            name = request.POST.get('name', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(user_email=email):  # 判断邮箱是否已经注册过了
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户邮箱已经存在！'})
            elif UserProfile.objects.filter(user_name=name):  # 判断用户名是否已存在
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户名已经存在！'})
            elif not RegisterView.isValid(email):  # 只有邮箱有效才保存
                return render(request, 'register.html', {'register_form': register_form, 'msg': '邮箱错误'})
            else:
                user_profile = UserProfile()
                user_profile.username = name
                user_profile.password = name
                user_profile.email = email
                # 父类的属性，用于验证用户名密码
                # user_profile.user_name = name
                # user_profile.user_email = email
                # user_profile.user_password = make_password(password)
                user_profile.is_active = False
                user_profile.save()
                try:
                    send_link_email(email)  # 发送激活邮件
                except AttributeError:
                    return render(request, 'register.html', {'msg': '邮箱错误'})
                # 跳转到登录界面
                return redirect('../login')

        else:
            error = register_form.errors  # 拿到自定义规则或自带规则的错误信息
            '''
            第二层全局错误,__all__:全局错误信息
            如果全局错误里不为空，则取错误
            '''
            if register_form.errors.get("__all__"):
                # 取全局钩子函数的匹配报错信息的方法
                g_error = register_form.errors.get("__all__")[0]
                # 只选取第一个错误
            return render(request, 'register.html', locals())  # 把错误数据渲染到模板


class RegisterActiveView(View):
    """注册激活功能"""

    def get(self, request, url_active_code):
        regis_actives = EmailVerification.objects.filter(code=url_active_code, is_delete=0)
        if regis_actives:
            for regis_active in regis_actives:
                email = regis_active.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

                regis_active.is_delete = 1
                regis_active.save()
                return render(request, 'register_active_sucessed.html', {})
        else:
            return render(request, 'register_active_failed.html', {})


class LoginView(View):
    """用户登录功能"""

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_user = request.POST.get('username', '')
            login_password = request.POST.get('password', '')
            user = authenticate(user_name=login_user, user_password=login_password)
            if user:  # 通过验证
                if user.is_active:  # 已激活
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户不存在'})
            else:
                return render(request, 'login.html', {'login_form': login_form, 'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ForgetpwdView(View):
    """登录页面点击忘记密码"""

    def get(self, request):
        forgetpwd_form = ForgetpwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        """获取邮箱并发送重置密码链接"""
        forgetpwd_form = ForgetpwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                try:
                    send_link_email(email, send_type='forget')  # 发送重置密码链接
                except AttributeError:
                    return render(request, 'forgetpwd.html', {'msg': '邮箱错误'})
                return render(request, "email_send_success.html",
                              {'email': email, 'msg': '请前往查收并点击链接重置密码'})
            else:
                return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form, 'msg': '该邮箱未注册'})
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


class PwdresetView(View):
    """密码重置链接处理,点击转向密码重置页面"""

    def get(self, request, url_pwdreset_code):
        pwdreset_code = url_pwdreset_code
        users = EmailVerification.objects.filter(code=pwdreset_code, is_delete=0)
        if users:
            for user in users:
                email = user.email
                return render(request, 'password_reset.html', {'email': email, 'pwdreset_code': pwdreset_code})
        else:
            return render(request, 'register_active_failed.html')


class PwdmodifyView(View):
    """密码重置功能"""

    def post(self, request):
        """密码重置处理"""
        pwdmodify_form = PwdmodifyForm(request.POST)
        if pwdmodify_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            pwdmodify_email = request.POST.get('email', '')
            pwdmodify_code = request.POST.get('pwdreset_code', '')
            if password1 == password2:
                pwdmodify_user = UserProfile.objects.get(email=pwdmodify_email)
                pwdmodify_user.password = make_password(password1)
                pwdmodify_user.save()

                pwdmodify_code_es = EmailVerification.objects.filter(code=pwdmodify_code)
                for pwdmodify_code_e in pwdmodify_code_es:
                    pwdmodify_code_e.is_delete = 1
                    pwdmodify_code_e.save()

                    return render(request, 'login.html', {'pwdreset_msg': '密码重置成功，请登录'})
            else:
                return render(request, 'password_reset.html',
                              {'pwdmodify_form': pwdmodify_form, 'msg': '两次输入不一致，请重新输入'})
        else:
            return render(request, 'password_reset.html', {'pwdmodify_form': pwdmodify_form})


class LogoutView(View):
    """注销登录功能"""

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class UserInfoView(View):
    """用户的个人中心"""

    def get(self, request):
        """进入个人中心"""
        user = request.user.username
        if not user:  # 未登录
            return render(request, 'login.html', {'pwdreset_msg': '您还未登录...'})
        else:
            return render(request, 'usercenter-info.html')


class UploadUserInfoView(LoginRequiredMixin, View):
    """个人中心的个人资料修改"""

    def post(self, request):
        user_form = UpUserInfoForm(request.POST, instance=request.user)
        res = dict()
        if user_form.is_valid():
            user = UserProfile.objects.get(id=request.user.id)
            user.username = request.POST.get('user_name', '')
            user.save()

            res['status'] = 'success'
        else:
            res = user_form.errors
        return HttpResponse(json.dumps(res), content_type='application/json')


class UploadPwdView(LoginRequiredMixin, View):
    """个人中心的密码修改"""

    def post(self, request):
        pwdmodify_form = PwdmodifyForm(request.POST)
        res = dict()
        if pwdmodify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                res['status'] = 'fail'
                res['msg'] = '两次密码不一致'
                return HttpResponse(json.dumps(res), content_type='application/json')

            user = request.user
            user.password = make_password(pwd2)
            user.save()

            res['status'] = 'success'
            res['msg'] = '密码修改成功'
        else:
            res = pwdmodify_form.errors
        return HttpResponse(json.dumps(res), content_type='application/json')

# def page_not_look(request):
#     """全局403配置"""
#     from django.shortcuts import render_to_response
#     response = render_to_response('403.html',{})
#     response.status_code = 403
#     return response
#
# def page_not_found(request):
#     """全局404配置"""
#     from django.shortcuts import render_to_response
#     response = render_to_response('404.html',{})
#     response.status_code = 404
#     return response
#
# def page_error(request):
#     """全局500配置"""
#     from django.shortcuts import render_to_response
#     response = render_to_response('500.html',{})
#     response.status_code = 500
#     return response
