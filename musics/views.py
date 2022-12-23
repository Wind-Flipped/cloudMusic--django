import json

from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render,HttpResponseRedirect
from django.views.generic.base import View

from users.models import UserProfile
from .models import (
    Music_Information,
    Singer_Information,
    Album_Information,
    Songsheet_Information,
    Comment_Information,
    Feedback_Information,
    Singer_Music,
    Singer_Album,
    Album_Music,
    User_Music,
    User_Songsheet,
    Songsheet_Music,
    User_Singer,
    User_Comment_Music,
    User_Comment_Singer,
    User_Feedback_Comment,
    User_Become_Singer
)

# Create your views here.

# 歌曲信息表展示页面
class Music_Information_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        music_list = Music_Information.objects.all()
        hot_music_list = music_list.order_by('-music_popularity')[:5]
        newest_music_list = music_list.order_by('-music_public_time')[:5]
        level = range(1,len(hot_music_list) + 1)
        rank = zip(hot_music_list,level)
        music_num = music_list.count()

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            music_list = music_list.order_by('-music_popularity')
        elif sort == 'time':
            music_list = music_list.order_by('-music_public_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(music_list, 10, request=request)
        music_pages = p.page(page)

        return render(request, 'musics/Music_Information_View.html', {
            'music_pages': music_pages,
            'music_num': music_num,
            'hot_music': hot_music_list,
            'newest_music':newest_music_list,
            'rank':rank,
        })

    # 操作1：根据演唱形式或主题或关键字搜索 -- 返回搜索结果
    # 操作2：点击“歌曲详情” -- 跳转到歌曲专属页面
    def post(self, request):

        op_type = request.GET.get('op_type', '')
        music_list = Music_Information.objects.all()
        hot_music_list = music_list.order_by('-music_popularity')[:5]
        newest_music_list = music_list.order_by('-music_public_time')[:5]

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            music_list = music_list.order_by('-music_popularity')
        elif sort == 'time':
            music_list = music_list.order_by('-music_public_time')

        if op_type in ['search_type', 'search_theme', 'search_keyword']:

            if op_type == 'search_type':
                music_list = self.__get_by_type(request)
            elif op_type == 'search_theme':
                music_list = self.__get_by_theme(request)
            else:
                music_list = self.__get_by_keywords(request)

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(music_list, 10, request=request)
            music_pages = p.page(page)

            return render(request, 'musics/Music_Information_View.html', {
                'music_pages': music_pages,
                'music_num': len(music_list),
                'search':True,
                'key_music':music_list,
                'hot_music': hot_music_list,
                'newest_music': newest_music_list,
            })

        if op_type == 'check_detail':

            music_id = request.POST.get('music_id', '')
            return render(request, 'musics/Music_View.html', {
                'music_id': music_id,
            })

    # 根据关键字搜索
    def __get_by_keywords(self, request):

        keywords = request.POST.get('keywords', '')
        music_list = Music_Information.objects.filter(music_name__icontains=keywords)
        return music_list

    # 根据歌曲演唱类型搜索
    def __get_by_type(self, request):

        music_singing_type = request.POST.get('music_singing_type', '')
        music_list = Music_Information.objects.filter(music_singing_type=music_singing_type)
        return music_list

    # 根据歌曲主题搜索
    def __get_by_theme(self, request):

        music_theme = request.POST.get('music_theme', '')
        music_list = Music_Information.objects.filter(music_theme=music_theme)
        return music_list

# 歌曲专属页面
class Music_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        music_id = request.GET.get('music_id', '')
        music = Music_Information.objects.get(music_id=music_id)
        op_type = request.GET.get('op_type', '')
        if op_type == 'add_comment':
            res = self.__add_comment(request)
        elif op_type == 'add_fav_list':
            res = self.__add_fav_list(request)
        elif op_type == 'del_fav_list':
            res = self.__del_fav_list(request)
        try:
            exist_record = User_Music.objects.get(user=request.user, music=music)
            is_liked = True
        except:
            is_liked = False

        music_name = music.music_name
        music_singing_type = music.music_singing_type
        music_theme = music.music_theme
        music_duration = music.music_duration
        music_popularity = music.music_popularity
        music_link = music.music_link

        music_comment_list = User_Comment_Music.objects.filter(target_music=music).values('comment')
        comment_list = []
        for music_comment in music_comment_list:
            comment_list.append(Comment_Information.objects.get(comment_id=music_comment['comment']))

        singer_music = Singer_Music.objects.get(music=music)
        writer = singer_music.singer
        user_singer = User_Become_Singer.objects.get(singer=writer)
        user = user_singer.user

        music.music_popularity += 1
        music.save()

        return render(request, 'musics/Music_View.html', {
            'music_id': music_id,
            'music_name': music_name,
            'music_singing_type': music_singing_type,
            'music_theme': music_theme,
            'music_duration': music_duration,
            'music_popularity': music_popularity,
            'music_link': music_link,
            'comment_list': comment_list,
            'writer': writer,
            'user':user,
            'is_liked':is_liked,
        })

    # 操作1：添加或删除评论
    # 操作2：点击收藏或取消收藏
    # 操作3：点击查看评论
    def post(self, request):

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        op_type = request.GET.get('op_type', '')

        if op_type in ['add_comment', 'del_comment', 'add_fav_list', 'del_fav_list']:
            if op_type == 'add_comment':
                res = self.__add_comment(request)
            elif op_type == 'del_comment':
                res = self.__del_comment(request)
            elif op_type == 'add_fav_list':
                res = self.__add_fav_list(request)
            else:
                res = self.__del_fav_list(request)
            return HttpResponse(json.dumps(res), content_type='application/json')

        if op_type == 'check_comment':
            comment_id = request.POST.get('comment_id', '')
            return render(request, 'musics/Comment_View.html', {
                'comment_id': comment_id,
            })

    # 对该歌曲进行评论
    def __add_comment(self, request):

        music_id = request.GET.get('music_id')
        music = Music_Information.objects.get(music_id=music_id)

        comment = Comment_Information()
        comment.comment_theme = request.POST.get('comment_theme', '')
        comment.comment_grade = request.POST.get('comment_grade', '')
        comment.comment_content = request.POST.get('comment_content', '')
        comment.save()

        user_comment_music = User_Comment_Music()
        user_comment_music.user = request.user
        user_comment_music.comment = comment
        user_comment_music.target_music = music
        user_comment_music.save()

        request.user.user_exp += 10
        request.user.user_rank = get_level(request.user.user_exp)
        request.user.save()

        return {
            'status': 'success',
            'msg': '发布成功'
        }

    # 删除对该歌曲的评论
    def __del_comment(self, request):

        comment_id = request.POST.get('comment_id')
        comment = Comment_Information.objects.get(comment_id=comment_id)
        comment.delete()

        return {
            'status': 'success',
            'msg': '删除成功'
        }

    # 收藏歌曲
    def __add_fav_list(self, request):

        music_id = request.GET.get('music_id', '')
        music = Music_Information.objects.get(music_id=music_id)
        try:
            exist_record = User_Music.objects.get(user=request.user, music=music)
            return {
                'status': 'fail',
                'msg': '无法重复收藏'
            }
        except:
            pass

        user_music = User_Music()
        user_music.user = request.user
        user_music.music = music
        user_music.save()

        music.music_popularity += 10
        music.save()

        return {
            'status': 'success',
            'msg': '收藏成功'
        }

    # 取消收藏歌曲
    def __del_fav_list(self, request):

        music_id = request.GET.get('music_id', '')
        music = Music_Information.objects.get(music_id=music_id)

        try:
            exist_record = User_Music.objects.get(user=request.user, music=music)
            exist_record.delete()
            return {
                'status': 'success',
                'msg': '删除成功'
            }
        except:
            return {
                'status': 'fail',
                'msg': '收藏信息不存在'
            }



# 歌手信息表展示页面
class Singer_Information_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        singer_list = Singer_Information.objects.all()
        hot_singer_list = singer_list.order_by('-singer_popularity')[:5]
        new_singer_list = singer_list.order_by('-singer_debut_time')[:5]
        singer_num = singer_list.count()

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            singer_list = singer_list.order_by('-singer_popularity')
        elif sort == 'time':
            singer_list = singer_list.order_by('-singer_debut_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(singer_list, 10, request=request)
        singer_pages = p.page(page)

        return render(request, 'musics/Singer_Information_View.html', {
            'singer_pages': singer_pages,
            'singer_num': singer_num,
            'hot_singer': hot_singer_list,
            'new_singer':new_singer_list,
            'sort': sort,
        })

    # 操作1：根据歌手国籍或性别搜索或关键字搜索 -- 返回搜索结果
    # 操作2：点击“歌手详情” -- 跳转到歌手专属页面
    def post(self, request):

        op_type = request.POST.get('op_type', '')

        if op_type in ['search_nationality', 'search_sex', 'search_keyword']:

            if op_type == 'search_nationality':
                singer_list = self.__get_by_nationality(request)
            elif op_type == 'search_sex':
                singer_list = self.__get_by_sex(request)
            else:
                singer_list = self.__get_by_keywords(request)

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(singer_list, 10, request=request)
            singer_pages = p.page(page)

            return render(request, 'Singer_Information_View.html', {
                'singer_pages': singer_pages,
                'singer_num': len(singer_list),
            })

        if op_type == 'check_detail':

            singer_id = request.POST.get('singer_id', '')
            return render(request, 'Singer_View.html', {
                'singer_id': singer_id,
            })

    # 根据关键字搜索
    def __get_by_keywords(self, request):

        keywords = request.GET.get('keywords', '')
        singer_list = Singer_Information.objects.filter(singer_name__icontains=keywords)
        return singer_list

    # 根据歌手国籍搜索
    def __get_by_nationality(self, request):

        singer_nationality = request.POST.get('singer_nationality', '')
        singer_list = Singer_Information.objects.filter(singer_nationality=singer_nationality)
        return singer_list

    # 根据歌手性别搜索
    def __get_by_sex(self, request):

        singer_sex = request.POST.get('singer_sex', '')
        singer_list = Singer_Information.objects.filter(singer_sex=singer_sex)
        return singer_list

# 歌手专属页面
class Singer_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        singer_id = request.GET.get('singer_id', '')
        singer = Singer_Information.objects.get(singer_id=singer_id)

        singer_name = singer.singer_name
        singer_nationality = singer.singer_nationality
        singer_age = singer.singer_age
        singer_sex = singer.singer_sex
        singer_popularity = singer.singer_popularity
        singer_debut_time = singer.singer_debut_time

        singer_comment_list = User_Comment_Singer.objects.filter(singer=singer)
        comment_list = []
        for singer_comment in singer_comment_list:
            comment_list.append(singer_comment.comment)

        sing_music_list = []
        singer_sing_music_list = Singer_Music.objects.filter(singer=singer)
        for singer_sing_music in singer_sing_music_list:
            sing_music_list.append(singer_sing_music.music)

        album_list = []
        singer_album_list = Singer_Album.objects.filter(singer=singer)
        for singer_album in singer_album_list:
            album_list.append(singer_album.album)

        singer.singer_popularity += 1
        singer.save()

        return render(request, 'musics/Singer_View.html', {
            'singer_name': singer_name,
            'singer_nationality': singer_nationality,
            'singer_age': singer_age,
            'singer_sex': singer_sex,
            'singer_popularity': singer_popularity,
            'singer_debut_time': singer_debut_time,
            'comment_list': comment_list,
            'sing_music_list': sing_music_list,
            'album_list': album_list,
        })

    # 操作1：添加或删除评论
    # 操作2：点击关注或取消关注
    # 操作3：点击查看评论
    # 操作4：跳转到歌手对应用户主页
    def post(self, request):

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        op_type = request.POST.get('op_type', '')

        if op_type in ['add_comment', 'del_comment', 'add_fav_list', 'del_fav_list']:
            if op_type == 'add_comment':
                res = self.__add_comment(request)
            elif op_type == 'del_comment':
                res = self.__del_comment(request)
            elif op_type == 'add_fav_list':
                res = self.__add_fav_list(request)
            else:
                res = self.__del_fav_list(request)
            return HttpResponse(json.dumps(res), content_type='application/json')

        if op_type == 'check_comment':
            comment_id = request.POST.get('comment_id', '')
            return render(request, 'Comment_View.html', {
                'comment_id': comment_id,
            })

        if op_type == 'check_user':
            singer_id = request.POST.get('singer_id', '')
            singer = Singer_Information.objects.get(singer_id=singer_id)
            user = User_Become_Singer.objects.get(singer=singer)
            user_id = user.user_id
            return render(request, 'User_View.html', {
                'use_id': user_id,
            })

    # 对该进歌手行评论
    def __add_comment(self, request):

        singer_id = request.POST.get('singer_id')
        singer = Singer_Information.objects.get(singer_id=singer_id)

        comment = Comment_Information()
        comment.comment_theme = request.POST.get('comment_theme', '')
        comment.comment_grade = request.POST.get('comment_grade', '')
        comment.comment_content = request.POST.get('comment_content', '')
        comment.save()

        user_comment_singer = User_Comment_Singer()
        user_comment_singer.user = request.user
        user_comment_singer.comment = comment
        user_comment_singer.target_singer = singer
        user_comment_singer.save()

        request.user.user_exp += 10
        request.user.user_rank = get_level(request.user.user_exp)
        request.user.save()

        return {
            'status': 'success',
            'msg': '发布成功'
        }

    # 删除对该歌手的评论
    def __del_comment(self, request):

        comment_id = request.POST.get('comment_id')
        comment = Comment_Information.objects.get(comment_id=comment_id)
        comment.delete()

        return {
            'status': 'success',
            'msg': '删除成功'
        }

    # 关注歌手
    def __add_fav_list(self, request):

        singer_id = request.POST.get('singer_id', '')
        singer = Singer_Information.objects.get(singer_id=singer_id)

        exist_record = User_Music.objects.get(user=request.user, singer=singer)
        if exist_record:
            return {
                'status': 'fail',
                'msg': '无法重复关注'
            }

        user_singer = User_Music()
        user_singer.user = request.user
        user_singer.music = singer
        user_singer.save()

        singer.singer_popularity += 10
        singer.save()

        return {
            'status': 'success',
            'msg': '关注成功'
        }

    # 取消关注歌手
    def __del_fav_list(self, request):

        singer_id = request.POST.get('singer_id', '')
        singer = Singer_Information.objects.get(singer_id=singer_id)

        exist_record = User_Music.objects.get(user=request.user, singer=singer)
        if not exist_record:
            return {
                'status': 'fail',
                'msg': '关注信息不存在'
            }

        exist_record.delete()
        return {
            'status': 'success',
            'msg': '删除成功'
        }

# 专辑信息表展示页面
class Album_Information_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        album_list = Album_Information.objects.all()
        hot_album_list = album_list.order_by('-album_popularity')[:5]

        keywords = request.GET.get('keywords', '')
        if keywords:
            album_list = album_list.filter(album_name__icontains=keywords)

        album_num = album_list.count()

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            album_list = album_list.order_by('-album_popularity')
        elif sort == 'time':
            album_list = album_list.order_by('-album_created_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(album_list, 10, request=request)
        album_pages = p.page(page)

        return render(request, 'musics/Album_Information_View.html', {
            'album_pages': album_pages,
            'album_num': album_num,
            'hot_album': hot_album_list,
            'sort': sort,
        })

    # 操作1：根据专辑封面模式搜索或关键字 -- 返回搜索结果
    # 操作2：点击“专辑详情” -- 跳转到专辑专属页面
    def post(self, request):

        op_type = request.POST.get('op_type', '')

        if op_type in ['search_coverpage_type', 'search_keyword']:
            if op_type == 'search_coverpage_type':
                album_list = self.__get_by_coverpage_pattern(request)
            else:
                album_list = self.__get_by_keyword(request)

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(album_list, 10, request=request)
            album_pages = p.page(page)

            return render(request, 'Album_Information_View.html', {
                'album_pages': album_pages,
                'album_num': len(album_list),
            })

        if op_type == 'check_detail':

            album_id = request.POST.get('album_id', '')
            return render(request, 'Album_View.html', {
                'album_id': album_id,
            })

    # 根据关键字搜索
    def __get_by_keyword(self, request):

        keywords = request.GET.get('keywords', '')
        album_list = Album_Information.objects.filter(album_name__icontains=keywords)
        return album_list

    # 根据专辑封面模式搜索
    def __get_by_coverpage_pattern(self, request):

        album_coverpage_pattern = request.POST.get('album_coverpage_pattern', '')
        album_list = Album_Information.objects.filter(album_coverpage_pattern=album_coverpage_pattern)
        return album_list

# 专辑专属页面
class Album_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        album_id = request.GET.get('album_id', '')
        album = Album_Information.objects.get(album_id=album_id)

        album_name = album.album_name
        album_coverpage_pattern = album.album_coverpage_pattern
        album_music_num = album.album_music_num
        album_created_time = album.album_created_time
        album_popularity = album.album_popularity

        album.album_popularity += 1
        album.save()

        music_list = []
        album_music_list = Album_Music.objects.filter(album=album).values('music')
        for album_music in album_music_list:
            music_list.append(Music_Information.objects.get(music_id=album_music['music']))

        singer_album = Singer_Album.objects.get(album=album)
        singer = singer_album.singer

        return render(request, 'users/album.html', {
            'album_id': album_id,
            'album_name': album_name,
            'album_coverpage_pattern': album_coverpage_pattern,
            'album_music_num': album_music_num,
            'album_created_time': album_created_time,
            'album_popularity': album_popularity,
            'music_list': music_list,
            'singer': singer,
        })

    # 操作1：查看歌手详细信息
    # 操作2：查看歌曲详细信息
    def post(self, request):

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        op_type = request.POST.get('op_type', '')

        if op_type == 'check_singer_detail':

            singer_id = request.POST.get('singer_id', '')
            return render(request, 'Singer_View.html', {
                'singer_id': singer_id,
            })

        elif op_type == 'check_music_detail':

            music_id = request.POST.get('music_id', '')
            return render(request, 'Music_View.html', {
                'music_id': music_id,
            })

# 评论信息页面
# 评论信息页面
class Comment_View(View):

    # 进入页面时显示的信息
    def get(self, request):

        comment_id = request.GET.get('comment_id', '')
        comment = Comment_Information.objects.get(comment_id=comment_id)

        comment_theme = comment.comment_theme
        comment_grade = comment.comment_grade
        comment_content = comment.comment_content
        comment_time = comment.comment_time

        comment_feedback_list = User_Feedback_Comment.objects.filter(comment=comment)
        feedback_list = []
        for comment_feedback in comment_feedback_list:
            feedback_list.append(comment_feedback.feedback)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(feedback_list, 10, request=request)
        feedback_pages = p.page(page)

        exist_singer_record = User_Comment_Singer.objects.get(comment=comment)
        if exist_singer_record:
            author = exist_singer_record.user.user_id
            singer = exist_singer_record.singer
            name = singer.singer_name

        else:
            exist_music_record = User_Comment_Music.objects.get(comment=comment)
            author = exist_music_record.user.user_id
            music = exist_music_record.music
            name = music.music_name

        return render(request, 'Comment_View.html', {
            'comment_theme': comment_theme,
            'comment_grade': comment_grade,
            'comment_content': comment_content,
            'comment_time': comment_time,
            'target': 'musics',
            'name': name,
            'feedback_page': feedback_pages,
            'feedback_num': len(feedback_list),
            'auther': author,
        })

    # 操作1：添加或删除回帖
    # 操作2：查看评论作者个人主页
    # 操作3：查看评论对象（歌曲，歌手）专属页面
    def post(self, request):

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        op_type = request.POST.get('op_type', '')

        if op_type in ['add_feedback', 'del_feedback']:
            if op_type == 'add_feedback':
                ret = self.__add_feedback(request)
            else:
                ret = self.__del_feedback(request)
            return HttpResponse(json.dumps(ret), content_type='application/json')

        comment_id = request.POST.get('comment_id', '')
        comment = Comment_Information.objects.get(comment_id=comment_id)
        exist_music_record = User_Comment_Music.objects.get(comment=comment)
        exist_singer_record = User_Comment_Singer.objects.get(comment=comment)
        if exist_music_record:
            author = exist_music_record.user
            target = 'musics'
            music_id = exist_music_record.music.music_id
        else:
            author = exist_singer_record.user
            target = 'singer'
            singer_id = exist_singer_record.singer.singer_id

        if op_type == 'check_auther':
            user_id = author.user_id
            return render(request, 'User_View.html', {
                'user_id': user_id
            })
        elif op_type == 'check_target':
            if target == 'musics':
                return render(request, 'Music_View.html', {
                    'music_id': music_id,
                })
            else:
                return render(request, 'Singer_View.html', {
                    'singer_id': singer_id,
                })

    # 添加回帖
    def __add_feedback(self, request):

        comment_id = request.POST.get('comment_id', '')
        comment = Comment_Information.objects.get(comment_id=comment_id)

        feedback = Feedback_Information()
        feedback.feedback_theme = request.POST.get('feedback_theme', '')
        feedback.feedback_content = request.POST.get('feedback_content', '')
        feedback.save()

        user_feedback_comment = User_Feedback_Comment()
        user_feedback_comment.user = request.user
        user_feedback_comment.feedback = feedback
        user_feedback_comment.comment = comment
        user_feedback_comment.save()

        request.user.user_exp += 5
        request.user.user_rank = get_level(request.user.user_exp)
        request.user.save()

        return {
            'status': 'success',
            'msg': '回帖成功'
        }

    # 删除回帖
    def __del_feedback(self, request):

        feedback_id = request.POST.get('feedback_id', '')
        feedback = Feedback_Information.objects.get(feedback_id=feedback_id)
        feedback.delete()

        return {
            'statue': 'success',
            'msg': '删除成功'
        }

# （其他）用户页面
class User_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        user_id = request.GET.get('user_id', '')
        user = UserProfile.objects.get(user_id=user_id)

        user_name = user.user_name
        user_exp = user.user_exp
        user_rank = user.user_rank
        user_create_time = user.user_create_time
        user_is_admin = user.user_is_admin

        music_fav_list = []
        user_fav_music_list = User_Music.objects.filter(user=user)
        for user_fav_music in user_fav_music_list:
            music_fav_list.append(user_fav_music.music)

        singer_fav_list = []
        user_fav_singer_list = User_Singer.objects.filter(user=user)
        for user_fav_singer in user_fav_singer_list:
            singer_fav_list.append(user_fav_singer.singer)

        songsheet_list = []
        user_songsheet_list = User_Songsheet.objects.filter(user=user)
        for user_songsheet in user_songsheet_list:
            songsheet_list.append(user_songsheet.songsheet)

        return render(request, 'User_View.html', {
            'user_name': user_name,
            'user_exp': user_exp,
            'user_rank': user_rank,
            'user_create_time': user_create_time,
            'user_is_admin': user_is_admin,
            'fav_music_list': music_fav_list,
            'fav_singer_list': singer_fav_list,
            'songsheet_list': songsheet_list,
        })

    # 操作1：查看歌曲详情
    # 操作2：查看歌手详情
    def post(self, request):

        op_type = request.POST.get('op_type', '')

        if op_type == 'check_music_detail':

            music_id = request.POST.get('music_id', '')
            return render(request, 'Music_View', {
                'music_id': music_id
            })

        elif op_type == 'check_singer_detail':

            singer_id = request.POST.get('singer_id', '')
            return render(request, 'Singer_View', {
                'singer_id': singer_id
            })

# 本人页面
class Personal_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        user_id = request.user.user_id
        user_name = request.user.user_name
        user_password = request.user.user_password
        user_exp = request.user.user_exp
        user_rank = request.user.user_rank
        user_create_time = request.user.user_create_time
        user_is_admin = request.user.user_is_admin
        user_email = request.user.user_email

        fav_music_list = []
        user_music_list = User_Music.objects.filter(user=request.user)
        for user_music in user_music_list:
            fav_music_list.append(user_music.music)

        fav_singer_list = []
        user_singer_list = User_Singer.objects.filter(user=request.user)
        for user_singer in user_singer_list:
            fav_singer_list.append(user_singer.singer)

        songsheet_list = []
        user_songsheet_list = User_Songsheet.objects.filter(user=request.user)
        for user_songsheet in user_songsheet_list:
            songsheet_list.append(user_songsheet.songsheet)

        singer_record = User_Become_Singer.objects.filter(user=request.user)
        if not singer_record:
            return render(request, 'Personal_View.html', {
                'user_id': user_id,
                'user_name': user_name,
                'user_password': user_password,
                'user_exp': user_exp,
                'user_rank': user_rank,
                'user_create_time': user_create_time,
                'user_is_admin': user_is_admin,
                'user_email': user_email,
                'fav_music_list': fav_music_list,
                'fav_singer_list': fav_singer_list,
                'songsheet_list': songsheet_list,
            })
        else:
            singer = singer_record.singer

            singer_name = singer.singer_name
            singer_nationality = singer.singer_nationality
            singer_age = singer.singer_age
            singer_sex = singer.singer_sex
            singer_popularity = singer.singer_popularity
            singer_debut_time = singer.singer_debut_time

            singer_comment_list = User_Comment_Singer.objects.filter(singer=singer)
            comment_list = []
            for singer_comment in singer_comment_list:
                comment_list.append(singer_comment.comment)

            sing_music_list = []
            singer_sing_music_list = Singer_Music.objects.filter(singer=singer)
            for singer_sing_music in singer_sing_music_list:
                sing_music_list.append(singer_sing_music.music)

            album_list = []
            singer_album_list = Singer_Album.objects.filter(singer=singer)
            for singer_album in singer_album_list:
                album_list.append(singer_album.album)

            return render(request, 'Singer_View.html', {
                'user_id': user_id,
                'user_name': user_name,
                'user_password': user_password,
                'user_exp': user_exp,
                'user_rank': user_rank,
                'user_create_time': user_create_time,
                'user_is_admin': user_is_admin,
                'user_email': user_email,
                'fav_music_list': fav_music_list,
                'fav_singer_list': fav_singer_list,
                'songsheet_list': songsheet_list,
                'singer_name': singer_name,
                'singer_nationality': singer_nationality,
                'singer_age': singer_age,
                'singer_sex': singer_sex,
                'singer_popularity': singer_popularity,
                'singer_debut_time': singer_debut_time,
                'comment_list': comment_list,
                'sing_music_list': sing_music_list,
                'album_list': album_list,
            })

    # 操作1：查看歌曲详情
    # 操作2：查看歌手详情
    # 操作3：查看歌单详情
    # 操作4：创建歌单
    # 操作5：删除歌单
    # （歌手）操作6：演唱歌曲
    # （歌手）操作7：发布专辑
    # （歌手）操作8：删除专辑
    # （歌手）操作9：向专辑添加歌曲
    # （歌手）操作10：从专辑中删除歌曲
    def post(self, request):

        op_type = request.GET.get('op_type', '')

        if op_type == 'Check_Music_Detail':
            music_id = request.POST.get('music_id', '')
            return render(request, 'Music_View', {
                'music_id': music_id,
            })
        elif op_type == 'Check_Singer_Detail':
            singer_id = request.POST.get('singer_id', '')
            return render(request, 'Singer_View', {
                'singer_id': singer_id,
            })
        elif op_type == 'Check_Songsheet_Detail':
            songsheet_id = request.POST.get('songsheet_id', '')
            return render(request, 'Songsheet_View', {
                'songsheet_id', songsheet_id,
            })
        elif op_type in ['Create_songsheet', 'Delete_Songsheet']:
            if op_type == 'Create_songsheet':
                res = self.__add_songsheet(request)
            else:
                res = self.__del_songsheet(request)
            # songsheet = User_Songsheet.objects.filter(user=request.user).values('songsheet')
            return HttpResponseRedirect('/users/userindex/' + str(request.user.user_id))

        user_become_singer = User_Become_Singer.objects.get(user=request.user)
        if not user_become_singer:
            res = {
                'status': 'fail',
                'msg': '未注册成为歌手'
            }
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            singer = user_become_singer.singer

        if op_type == 'Sing_Song':
            res = self.__sing_song(request, singer)
            return HttpResponseRedirect('/users/create_music')

        if op_type in ['Add_Album', 'Del_Album']:
            if op_type == 'Add_Album':
                res = self.__add_album(request, singer)
            else:
                res = self.__del_album(request, singer)
            return HttpResponseRedirect('/users/userindex/' + str(request.user.user_id))

        if op_type in ['Add_Music_To_Album', 'Del_Music_From_Album']:
            if op_type == 'Add_Music_To_Album':
                album_id = request.POST.get('album_id', '')
                album = Album_Information.objects.get(album_id=album_id)
                music_id = request.GET.get('music_id', '')
                music = Music_Information.objects.get(music_id=music_id)
                res = self.__add_music_to_album(request, singer, album, music)
            else:
                album_id = request.GET.get('album_id', '')
                album = Album_Information.objects.get(album_id=album_id)
                music_id = request.GET.get('music_id', '')
                music = Music_Information.objects.get(music_id=music_id)
                res = self.__del_music_from_album(request, singer, album, music)
            return HttpResponseRedirect('/musics/Album_View/?album_id=' + str(album_id))

    # 创建歌单
    def __add_songsheet(self, request):

        songsheet_name = request.POST.get('songsheet_name', '')

        songsheet = Songsheet_Information()
        songsheet.songsheet_name = songsheet_name
        songsheet.save()

        user_songsheet = User_Songsheet()
        user_songsheet.user = request.user
        user_songsheet.songsheet = songsheet
        user_songsheet.save()

        return {'status': 'success','msg': '创建成功'}

    # 删除歌单
    def __del_songsheet(self, request):

        songsheet_id = request.GET.get('songsheet_id', '')
        songsheet = Songsheet_Information.objects.get(songsheet_id=songsheet_id)
        songsheet.delete()

        return {
            'status': 'success',
            'msg': '删除成功'
        }

    # 演唱歌曲
    def __sing_song(self, request, singer):

        music = Music_Information()
        music.music_name = request.POST.get('music_name', '')
        music.music_singing_type = request.POST.get('music_singing_type', '')
        music.music_theme = request.POST.get('music_theme', '')
        # music.music_duration = request.POST.get('music_duration', '')
        # music.music_popularity = request.POST.get('music_popularity', '')
        music.music_link = request.POST.get('music_link', '')
        music.save()

        singer_music = Singer_Music()
        singer_music.singer = singer
        singer_music.music = music
        singer_music.save()

        request.user.user_exp += 100
        request.user.user_rank = get_level(request.user.user_exp)
        request.user.save()

        return {
            'status': 'success',
            'msg': '创作成功'
        }

    # 发布专辑
    def __add_album(self, request, singer):

        album = Album_Information()
        album.album_name = request.POST.get('album_name', '')
        album.album_coverpage_pattern = request.POST.get('album_coverpage_pattern', '')
        album.save()

        singer_album = Singer_Album()
        singer_album.singer = singer
        singer_album.album = album
        singer_album.save()

        return {
            'status': 'success',
            'msg': '发布成功'
        }

    # 删除专辑

    # 删除专辑
    def __del_album(self, request, singer):

        album_id = request.GET.get('album_id', '')
        album = Album_Information.objects.get(album_id=album_id)
        album.delete()

        return {
            'status': 'success',
            'msg': '删除成功'
        }

    # 向专辑中添加歌曲
    def __add_music_to_album(self, request, singer, album, music):

        exists_record = Album_Music.objects.filter(album=album, music=music)
        if exists_record:
            res = {
                'status': 'success',
                'msg': '无法重复添加'
            }
            return HttpResponse(json.dumps(res), content_type='application/json')

        album_music = Album_Music()
        album_music.album = album
        album_music.music = music
        album_music.save()

        return {
            'status': 'success',
            'msg': '添加成功'
        }

    # 从专辑中删除歌曲
    def __del_music_from_album(self, request, singer, album, music):

        exists_record = Album_Music.objects.filter(album=album, music=music)
        if not exists_record:
            return {
                'status': 'fail',
                'msg': '不存在该歌曲'
            }

        exists_record.delete()
        return {
            'status': 'success',
            'msg': '删除成功'
        }

# 歌单专属页面
class Songsheet_View(View):

    # 进入页面时展示的信息
    def get(self, request):

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        songsheet_id = request.GET.get('songsheet_id', '')

        songsheet = Songsheet_Information.objects.get(songsheet_id=songsheet_id)
        user = User_Songsheet.objects.get(songsheet_id=songsheet_id)
        songsheet_name = songsheet.songsheet_name

        music_list = []
        join_time_list = []
        songsheet_music_list = Songsheet_Music.objects.filter(songsheet=songsheet).values('music')
        join_time = Songsheet_Music.objects.filter(songsheet=songsheet).values('join_time')

        for jt in join_time:
            join_time_list.append(jt['join_time'])
        for sst in songsheet_music_list:
            music_list.append(Songsheet_Information.objects.get(songsheet_id=sst['music']))
        music_list = zip(music_list,join_time)

        return render(request, 'users/Songsheet_View.html', {
            'songsheet_id': songsheet_id,
            'songsheet_name': songsheet_name,
            'music_list': music_list,
            'user':user,
        })

    # 操作1：添加歌曲
    # 操作2：删除歌曲
    # 操作3：查看歌曲详情
    def post(self, request):

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        op_type = request.GET.get('op_type')

        if op_type in ['Add_Music', 'Del_Music']:
            if op_type == 'Add_Music':
                res = self.__add_music(request)
            else:
                res = self.__del_music(request)
            return HttpResponse(json.dumps(res), content_type='application/json')

        if op_type == 'Check_Music_Detail':
            music_id = request.POST.get('music_id', '')
            return render(request, 'Music_View', {
                'music_id': music_id,
            })

    # 添加歌曲
    def __add_music(self, request):

        songsheet_id = request.GET.get('songsheet_id', '')
        songsheet = Songsheet_Information.objects.filter(songsheet_id=songsheet_id)
        music_id = request.POST.get('music_id', '')
        music = Music_Information.objects.filter(music_id=music_id)

        exist_record = Songsheet_Music.objects.filter(songsheet=songsheet, music=music)
        if exist_record:
            return {
                'status': 'fail',
                'msg': '无法重复添加'
            }

        songsheet_music = Songsheet_Music()
        songsheet_music.songsheet = songsheet
        songsheet_music.music = music
        songsheet_music.save()

        return {
            'status': 'success',
            'msg': '添加成功'
        }

    # 删除歌曲
    def __del_music(self, request):

        songsheet_id = request.GET.get('songsheet_id', '')
        songsheet = Songsheet_Information.objects.filter(songsheet_id=songsheet_id)
        music_id = request.GET.get('music_id', '')
        music = Music_Information.objects.filter(music_id=music_id)

        exist_record = Songsheet_Music.objects.filter(songsheet=songsheet, music=music)
        exist_record.delete()
        return {
            'status': 'success',
            'msg': '删除成功'
        }

# 用户注册成为歌手
class Singer_Registration_View(View):

    def get(self, request):
        return render(request, 'users/singer_register.html', {})

    def post(self, request):

        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        singer_name = request.POST.get('singer_name', '')
        singer_nationality = request.POST.get('singer_nationality', '')
        singer_age = request.POST.get('singer_age', '')
        singer_sex = request.POST.get('singer_sex', '')
        # singer_popularity = request.POST.get('singer_popularity', '')
        # singer_debut_time = request.POST.get('singer_debut_time', '')

        exist_record = User_Become_Singer.objects.filter(user=request.user)
        if exist_record:
            res = {
                'status': 'fail',
                'msg': '已经注册过'
            }
            return render(request,'users/singer_register.html',res)

        singer = Singer_Information()
        singer.singer_name = singer_name
        singer.singer_nationality = singer_nationality
        singer.singer_age = singer_age
        singer.singer_sex = singer_sex
        # singer.singer_popularity = singer_popularity
        # singer.singer_debut_time = singer_debut_time
        singer.save()

        user_become_singer = User_Become_Singer()
        user_become_singer.user = request.user
        user_become_singer.singer = singer
        user_become_singer.save()

        res = {
            'status': 'success',
            'msg': '注册成功'
        }
        return HttpResponseRedirect('/users/userinfo')

def get_level(exp):
    level = 1
    need_exp = 100
    remain_exp = exp
    while remain_exp >= need_exp:
        remain_exp -= need_exp
        need_exp *= 2
        level += 1
    return level
