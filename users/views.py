import math

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
from django.core.exceptions import ObjectDoesNotExist
from musics.models import User_Become_Singer,Songsheet_Information,User_Songsheet,User_Music,Singer_Music,Music_Information,Album_Information,Singer_Album

class IndexView(View):
    """显示首页"""

    def get(self, request):
        return render(request, 'musics/index.html')


class RegisterView(View):
    """用户注册功能"""

    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  # 正则验证有效性

    # TODO 考虑直接发邮件，验证码
    @classmethod
    def isValid(self,email):
        if re.fullmatch(RegisterView.regex, email):
            return True
        else:
            return False

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'users/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            name = request.POST.get('name', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(email=email):  # 判断邮箱是否已经注册过了
                return render(request, 'users/register.html', {'register_form': register_form, 'msg': '用户邮箱已经存在！'})
            elif UserProfile.objects.filter(username=name):  # 判断用户名是否已存在
                return render(request, 'users/register.html', {'register_form': register_form, 'msg': '用户名已经存在！'})
            elif not RegisterView.isValid(email):  # 只有邮箱有效才保存
                return render(request, 'users/register.html', {'register_form': register_form, 'msg': '邮箱错误'})
            else:
                user_profile = UserProfile()
                user_profile.username = name
                user_profile.password = password
                user_profile.email = email
                # 父类的属性，用于验证用户名密码
                # user_profile.user_name = name
                # user_profile.user_email = email
                # user_profile.user_password = make_password(password)
                user_profile.is_active = True
                user_profile.save()
                # try:
                #     send_link_email(email)  # 发送激活邮件
                # except AttributeError:
                #     return render(request, 'users/register.html', {'msg': '邮箱错误'})
                # 跳转到登录界面
                return redirect('../login')

        else:
            # error = register_form.errors  # 拿到自定义规则或自带规则的错误信息
            '''
            第二层全局错误,__all__:全局错误信息
            如果全局错误里不为空，则取错误
            '''
            # if register_form.errors.get("__all__"):
            #     # 取全局钩子函数的匹配报错信息的方法
            #     g_error = register_form.errors.get("__all__")[0]
            #     # 只选取第一个错误
            return render(request, 'users/register.html', {'register_form': register_form,'msg': '输入信息有误'})  # 把错误数据渲染到模板


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
        return render(request, 'users/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_user = request.POST.get('username', '')
            login_password = request.POST.get('password', '')
            try:
                user = UserProfile.objects.get(username=login_user)
                if user.password == login_password:
                    login(request,user)
                    return HttpResponseRedirect('/users/userinfo')
                else:
                    return render(request,'users/login.html',{'msg':'用户密码错误'})
            except ObjectDoesNotExist as e:
                return render(request, 'users/login.html', {'msg': '用户不存在'})
            # user = authenticate(username=login_user, password=login_password)
            # if user:  # 通过验证
            #     if user.is_active:  # 已激活
            #         login(request, user)
            #         return HttpResponseRedirect(reverse('index'))
            #     else:
            #         return render(request, 'users/login.html', {'msg': '用户不存在'})
            # else:
            #     return render(request, 'users/login.html', {'login_form': login_form, 'msg': '用户名或密码错误'})
        else:
            return render(request, 'users/login.html', {'login_form': login_form,'msg': '输入信息有误'})


class ForgetpwdView(View):
    """登录页面点击忘记密码"""

    def get(self, request):
        forgetpwd_form = ForgetpwdForm()
        return render(request, 'pwdmodify.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        """获取邮箱并发送重置密码链接"""
        forgetpwd_form = ForgetpwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                # try:
                #     send_link_email(email, send_type='forget')  # 发送重置密码链接
                # except AttributeError:
                #     return render(request, 'pwdmodify.html', {'msg': '邮箱错误'})
                return render(request, "email_send_success.html",
                              {'email': email, 'msg': '请前往查收并点击链接重置密码'})
            else:
                return render(request, 'pwdmodify.html', {'forgetpwd_form': forgetpwd_form, 'msg': '该邮箱未注册'})
        else:
            return render(request, 'pwdmodify.html', {'forgetpwd_form': forgetpwd_form})


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

    def get(self, request):
        pwdmodify_form = PwdmodifyForm()
        return render(request, 'users/pwdmodify.html', {'pwdmodify_form': pwdmodify_form})
    def post(self, request):
        """密码重置处理"""
        pwdmodify_form = PwdmodifyForm(request.POST)
        if pwdmodify_form.is_valid():
            username = request.POST.get('username','')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            user = UserProfile.objects.get(username=username)
            if user:
                if user.email != email:
                    return render(request,'users/pwdmodify.html',{'pwdmodify_form': pwdmodify_form, 'msg': '账号对应邮箱错误'})
                else:
                    user.password = password1
                    user.save()
                    return render(request, 'users/login.html', {'pwdreset_msg': '密码重置成功，请登录'})
            # pwdmodify_code = request.POST.get('pwdreset_code', '')
            # if password1 == password2:
            #     pwdmodify_user = UserProfile.objects.get(email=pwdmodify_email)
            #     pwdmodify_user.password = make_password(password1)
            #     pwdmodify_user.save()

                # pwdmodify_code_es = EmailVerification.objects.filter(code=pwdmodify_code)
                # for pwdmodify_code_e in pwdmodify_code_es:
                #     pwdmodify_code_e.is_delete = 1
                #     pwdmodify_code_e.save()
            else:
                return render(request, 'users/pwdmodify.html',
                              {'pwdmodify_form': pwdmodify_form, 'msg': '该账号不存在'})
        else:
            return render(request, 'users/pwdmodify.html',
                              {'pwdmodify_form': pwdmodify_form, 'msg': '输入错误'})


class LogoutView(View):
    """注销登录功能"""

    def get(self, request):
        logout(request)
        return render(request,'users/login.html',{'msg': '请重新登陆'})


class UserInfoView(View):
    """用户的个人中心"""

    def get(self, request):
        """进入个人中心"""
        user = request.user
        if not user:  # 未登录
            return render(request, 'users/login.html', {'pwdreset_msg': '您还未登录...'})
        else:
            musics = []
            albums = []
            try:
                user_singer = User_Become_Singer.objects.get(user=user)
                if user_singer:
                    is_singer = True
                else:
                    user_singer = False
                singer = user_singer.singer
                singer_music = Singer_Music.objects.filter(singer=singer).values('music')
                singer_album = Singer_Album.objects.filter(singer=singer).values('album')

                for sm in singer_music:
                    musics.append(Music_Information.objects.get(music_id=sm['music']))

                for al in singer_album:
                    albums.append(Album_Information.objects.get(album_id=al['album']))

            except:
                singer = {}
                is_singer = False
            songsheet = User_Songsheet.objects.filter(user=user)
            music = User_Music.objects.filter(user=user)
            songsheet_num = songsheet.count()
            music_num = music.count()
            return render(request, 'users/userinfo.html',{'singer':singer,'is_singer':is_singer,
                                                          'songsheet_num':songsheet_num,'music_num':music_num,
                                                          'musics':musics,'albums':albums,'music':music})

class UserIndex(View):
    """其他用户的个人资料"""

    def get(self, request, user_id):
        """进入个人中心"""
        try:
            user = UserProfile.objects.get(user_id=user_id)
        except:
            return render(request, 'users/login.html', {'pwdreset_msg': '您查询的用户不存在...'})
        musics = []
        albums = []
        try:
            user_singer = User_Become_Singer.objects.get(user=user)
            is_singer = True
            singer = user_singer.singer
            singer_music = Singer_Music.objects.filter(singer=singer).values('music')
            singer_album = Singer_Album.objects.filter(singer=singer).values('album')

            for sm in singer_music:
                musics.append(Music_Information.objects.get(music_id=sm['music']))

            for al in singer_album:
                albums.append(Album_Information.objects.get(album_id=al['album']))
        except:
            singer = {}
            is_singer = False
        user_songsheet = User_Songsheet.objects.filter(user=user)
        songsheets = user_songsheet.values('songsheet')
        songsheet = []
        for sst in songsheets:
            songsheet.append(Songsheet_Information.objects.get(songsheet_id=sst['songsheet']))
        create_time = user_songsheet.values('create_time')
        update_time = user_songsheet.values('update_time')
        user_music = User_Music.objects.filter(user=user).values('music')
        music = []
        for um in user_music:
            music.append(Music_Information.objects.get(music_id=um['music']))
        user_need_exp = math.pow(2,user.user_rank - 1) * 100
        remain_exp = get_exp(user.user_exp,user.user_rank)
        return render(request, 'users/userindex.html',{'user':user,'is_singer':is_singer,'singer':singer,'songsheet':songsheet,'music':music,'user_need_exp':user_need_exp,
                                                       'musics':musics,'albums':albums,'remain_exp':remain_exp})

class CreateMusic(View):
    def get(self,request):
        user = request.user
        try:
            singer = User_Become_Singer.objects.get(user=user).singer
            is_singer = True
        except:
            return render(request,'users/userinfo.html',{'msg':'您还不是一位歌手，请点击成为歌手，再发布歌曲'})

        return render(request, 'users/create_music.html', {'singer': singer, 'is_singer': is_singer,'user':user})

class UploadUserInfo(View):
    def get(self,request):
        user = request.user
        try:
            singer = User_Become_Singer.objects.get(user=user).singer
            is_singer = True
            return render(request,'users/upload_info.html',{'user':user,'singer':singer,'is_singer':is_singer})
        except:
            is_singer = False
            return render(request,'users/upload_info.html',{'user':user,'is_singer':is_singer})

    def post(self,request):
        user = request.user
        user.user_nickname = request.POST.get('user_nickname','')
        user.user_saying = request.POST.get('user_saying','')
        user.save()
        try:
            singer = User_Become_Singer.objects.get(user=user).singer
            singer.singer_name = request.POST.get('singer_name','')
            singer.singer_age = request.POST.get('singer_age','')
            singer.singer_nationality = request.POST.get('singer_nationality','')
            singer.singer_sex = request.POST.get('singer_sex','')
            singer.save()
        except:
            pass
        return render(request,'users/userinfo.html',{})

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

def get_exp(exp,level):
    for i in range(1,level):
        exp -= 100 * math.pow(2,i-1)
    return exp

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
