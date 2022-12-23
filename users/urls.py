from django.urls import path, include
from . import views

urlpatterns = [
    # 登录
    path('login/', views.LoginView.as_view(), name='login'),
    # 注册
    path('register/', views.RegisterView.as_view(), name='register'),
    # 首页 主体为音乐
    path('index/', views.IndexView.as_view(), name='index'),
    # 注册激活链接
    path('active/<url_active_code>/', views.RegisterActiveView.as_view(),name='register_active'),
    # 个人中心
    path('userinfo/', views.UserInfoView.as_view(), name='userinfo'),
    # 个人中心——密码修改
    path('uploadpwd/', views.UploadPwdView.as_view(), name='uploadpwd'),
    # 个人中心——基本资料修改
    path('mymessage/', views.UploadUserInfoView.as_view(), name='mymessage'),
    # 忘记密码
    path('forgetpwd/', views.ForgetpwdView.as_view(), name='forgetpwd'),
    # 重置密码链接
    path('pwdreset/<url_pwdreset_code>/', views.PwdresetView.as_view(), name='pwdreset'),
    # 重置密码处理
    path('pwdmodify/', views.PwdmodifyView.as_view(), name='pwdmodify'),
    # 注销登录/登出
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # 用户个人资料界面
    path('userindex/<int:user_id>', views.UserIndex.as_view(), name='userindex'),
    # 歌手写歌界面
    path('create_music/',views.CreateMusic.as_view(),name='create_music'),
    # 修改用户（歌手）个人信息
    path('upload_info/',views.UploadUserInfo.as_view(),name='upload_info'),
]
