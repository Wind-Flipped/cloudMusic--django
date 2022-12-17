import json

from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render
from django.views.generic.base import View
from utils.mixin_utils import LoginRequiredMixin

import datetime

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
    User_Relationship
)

# Create your views here.

# Part One: Entity Display Views

# Display Music Information
class Music_Information_View(View):

    @ staticmethod
    def get(request):

        # Get All The Music Information
        music_list = Music_Information.objects.all()
        hot_music_list = music_list.order_by('-music_popularity')[:5]

        # Search The Keyword
        keywords = request.GET.get('keywords', '')
        if keywords:
            music_list = music_list.filter(name__icontains=keywords)

        # Total Number Of Songs
        music_num = music_list.count()

        # Sort The Music List By Popularity
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            music_list = music_list.order_by('-music_popularity')
        elif sort == 'time':
            music_list = music_list.order_by('-')

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(music_list, 10, request=request)
        music_pages = p.page(page)

        return render(request, 'Music_Information.html', {
            'music_pages': music_pages,
            'music_num': music_num,
            'hot_music': hot_music_list,
            'sort': sort,
        })

# Display Singer Information
class Singer_Information_View(View):

    def get(self, request):

        # Get All The Singer Information
        singer_list = Singer_Information.objects.all()
        hot_singer_list = singer_list.order_by('-singer_popularity')[:5]

        # Search The Keyword
        keywords = request.GET.get('keywords', '')
        if keywords:
            singer_list = singer_list.filter(name__icontains=keywords)

        # Total Number Of Singers
        singer_num = singer_list.count()

        # Sort The Singer List By Popularity
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            singer_list = singer_list.order_by('-singer_popularity')

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(singer_list, 10, request=request)
        singer_pages = p.page(page)

        return render(request, 'Singer_Information.html', {
            'singer_pages': singer_pages,
            'singer_num': singer_num,
            'hot_singer': hot_singer_list,
            'sort': sort,
        })

# Display Album Information
class Album_Information_View(View):

    def get(self, request):

        # Get All The Album Information
        album_list = Album_Information.objects.all()
        hot_album_list = album_list.order_by('-album_popularity')[:5]

        # Search The Keyword
        keywords = request.GET.get('keywords', '')
        if keywords:
            album_list = album_list.filter(name__icontains=keywords)

        # Total Number Of Albums
        album_num = album_list.count()

        # Sort The Album List By Popularity
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            album_list = album_list.order_by('-album_popularity')

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(album_list, 10, request=request)
        album_pages = p.page(page)

        return render(request, 'Album_Information.html', {
            'album_pages': album_pages,
            'album_num': album_num,
            'hot_album': hot_album_list,
            'sort': sort,
        })

# Part Two: Entity Detailed Information Query

# Query Music Information In Detail
class Get_Music_Detailed_Information(View):

    def __get_by_name(self, request):

        # Get Music Information
        music_name = request.POST.get('music_name', '')
        music_list = Music_Information.objects.filter(music_name=music_name)
        return music_list

    def __get_by_type(self, request):

        # Get Music Information
        music_singing_type = request.POST.get('music_singing_type', '')
        music_list = Music_Information.objects.filter(music_singing_type=music_singing_type)
        return music_list

    def __get_by_theme(self, request):

        # Get Music Information
        music_theme = request.POST.get('music_theme', '')
        music_list = Music_Information.objects.filter(music_theme=music_theme)
        return music_list

    def post(self, request):

        # Three Query Type: Name, Singing_Type, Theme
        query_type = request.POST.get('query_type', '')

        # Query By Name
        if query_type == 'Name':
            music_list = self.__get_by_name(request)
        # Query By Singing Type
        elif query_type == 'Singing_Type':
            music_list = self.__get_by_type(request)
        # Query By Theme
        elif query_type == 'Theme':
            music_list = self.__get_by_theme(request)
        hot_music_list = music_list.order_by('-music_popularity')[:5]

        # Total Number Of Music
        music_num = music_list.count()

        # Sort The Music List By Popularity
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            music_list = music_list.order_by('-music_popularity')

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(music_list, 10, request=request)
        music_pages = p.page(page)

        return render(request, 'Music_Detailed_Information.html', {
            'music_pages': music_pages,
            'music_num': music_num,
            'hot_music': hot_music_list,
            'sort': sort,
        })

# Query Singer Information By singer_name
class Get_Singer_Information_By_Name(View):

    def __get_by_name(self, request):

        # Get Singer Information
        singer_name = request.POST.get('singer_name', '')
        singer_list = Singer_Information.objects.filter(singer_name=singer_name)
        return singer_list

    def __get_by_nationality(self, request):

        # Get Singer Information
        singer_nationality = request.POST.get('singer_nationality', '')
        singer_list = Singer_Information.objects.filter(singer_nationality=singer_nationality)
        return singer_list

    def __get_by_sex(self, request):

        # Get Singer Information
        singer_sex = request.POST.get('singer_sex', '')
        singer_list = Singer_Information.objects.filter(singer_sex=singer_sex)
        return singer_list

    def post(self, request):

        # Two Query Type: Name, Nationality
        query_type = request.POST.get('query_type', '')

        # Query By Name
        if query_type == 'Name':
            singer_list = self.__get_by_name(request)
        # Query By Nationality
        elif query_type == 'Nationality':
            singer_list = self.__get_by_nationality(request)
        hot_singer_list = singer_list.order_by('-singer_popularity')[:5]

        # Total Number Of Singers
        singer_num = singer_list.count()

        # Sort The Singer List By Popularity
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            singer_list = singer_list.order_by('-singer_popularity')

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(singer_list, 10, request=request)
        singer_pages = p.page(page)

        return render(request, 'Singer_Detailed_Information.html', {
            'singer_pages': singer_pages,
            'singer_num': singer_num,
            'hot_singer': hot_singer_list,
            'sort': sort,
        })

# Query Album Information By album_name
class Get_Album_Information_By_Name(View):

    def __get_by_name(self, request):

        # Get Album Information
        album_name = request.POST.get('album_name', '')
        album_list = Album_Information.objects.filter(album_name=album_name)
        return album_list

    def __get_by_coverpage_pattern(self, request):

        # Get Album Information
        album_coverpage_pattern = request.POST.get('album_coverpage_pattern', '')
        album_list = Album_Information.objects.filter(album_coverpage_pattern=album_coverpage_pattern)
        return album_list

    def post(self, request):

        # Two Query Type: Name, Coverpage Pattern
        query_type = request.POST.get('query_type', '')

        # Query By Name
        if query_type == 'Name':
            album_list = Get_Album_Information_By_Name.__get_by_name(request)
        # Query By Coverage Pattern
        elif query_type == 'Coverpage Pattern':
            album_list = Get_Album_Information_By_Name.__get_by_coverpage_pattern(request)
        hot_album_list = album_list.order_by('-album_popularity')[:5]

        # Total Number Of Albums
        album_num = album_list.count()

        # Sort The Album List By Popularity
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            album_list = album_list.order_by('-album_popularity')

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(album_list, 10, request=request)
        album_pages = p.page(page)

        return render(request, 'Get_Album_Information_By_Coverpage_Pattern.html', {
            'album_pages': album_pages,
            'album_num': album_num,
            'hot_album': hot_album_list,
            'sort': sort,
        })

# Part Three: Entity RelationShip Query Without Login

# Singer-Music RelationShip
class Singer_Music_View(View):

    def __get_music_by_singer(self, request):

        # Get Music Information
        singer_name = request.POST.get('singer_name', '')
        singer = Singer_Information.objects.get(singer_name=singer_name)
        singer_music_list = Singer_Music.objects.filter(singer=singer)

        music_list = []
        for singer_music in singer_music_list:
            music = singer_music.music
            music_list.append(music)
        return music_list

    def __get_singer_by_music(self, request):

        # Get Singer Information
        music_name = request.POST.get('music_name', '')
        music = Music_Information.objects.get(music_name=music_name)
        singer_music_list = Singer_Music.objects.filter(music=music)

        singer_list = []
        for singer_music in singer_music_list:
            singer = singer_music.singer
            singer_list.append(singer)
        return singer_list

    def post(self, request):

        # Two Query Type: Get Music By Singer, Get Singer By Music
        query_type = request.POST.get('query_type', '')

        # Query Singer By Music
        if query_type == 'singer':
            ret_list = self.__get_singer_by_music(request)
        # Query Music By Singer
        elif query_type == 'music':
            ret_list = self.__get_music_by_singer(request)
        else:
            ret_list = []

        return render(request, 'Singer_Music.html', {
            'result_list': ret_list,
            'result_num': len(ret_list),
        })

# Singer-Album RelationShip
class Singer_Album_View(View):

    def __get_album_by_singer(self, request):

        # Get Album Information
        singer_name = request.POST.get('singer_name', '')
        singer = Singer_Information.objects.get(singer_name=singer_name)
        singer_album_list = Singer_Album.objects.filter(singer=singer)

        album_list = []
        for singer_album in singer_album_list:
            album = singer_album.album
            album_list.append(album)
        return album_list

    def __get_singer_by_album(self, request):

        # Get Singer Information
        album_name = request.POST.get('album_name', '')
        album = Album_Information.objects.get(album_name=album_name)
        singer_album_list = Singer_Album.objects.filter(album=album)

        singer_list = []
        for singer_album in singer_album_list:
            singer = singer_album.singer
            singer_list.append(singer)
        return singer_list

    def post(self, request):

        # Two Query Type: Get Album By Singer, Get Singer By Album
        query_type = request.POST.get('query_type', '')

        # Query Album By Singer
        if query_type == 'album':
            ret_list = self.__get_album_by_singer(request)
        # Query Singer By Album
        elif query_type == 'singer':
            ret_list = self.__get_singer_by_album(request)
        else:
            ret_list = []

        return render(request, 'Singer_Album.html', {
            'result_list': ret_list,
            'result_num': len(ret_list),
        })

# Album-Music RelationShip
class Album_Music_View(View):

    def __get_music_by_album(self, request):

        # Get Music Information
        album_name = request.POST.get('album_name', '')
        album = Album_Information.objects.get(album_name=album_name)
        album_music_list = Album_Music.objects.filter(album=album)

        music_list = []
        for album_music in album_music_list:
            music = album_music.music
            music_list.append(music)
        return music_list

    def __get_album_by_music(self, request):

        # Get Album Information
        music_name = request.POST.get('music_name', '')
        music = Music_Information.objects.get(music_name=music_name)
        album_music_list = Album_Music.objects.filter(music=music)

        album_list = []
        for album_music in album_music_list:
            album = album_music.album
            album_list.append(album)
        return album_list

    def post(self, request):

        # Two Query Type: Get Music By Album, Get Album By Singer
        query_type = request.POST.get('query_type', '')

        # Query Music By Album
        if query_type == 'music':
            ret_list = self.__get_music_by_album(request)
        # Query Album By Music
        elif query_type == 'album':
            ret_list = self.__get_album_by_music(request)
        else:
            ret_list = []

        return render(request, 'Album_Music.html', {
            'result_list': ret_list,
            'result_num': len(ret_list),
        })

# Query Comment Information
class Comment_View(View):

    def __get_by_music(self, request):

        # Get Comment Information
        music_name = request.POST.get('music_name', '')
        music = Music_Information.objects.filter(music_name=music_name)
        music_comment_list = User_Comment_Music.objects.filter(music=music)
        music_comment_list = music_comment_list.order_by("-comment_time")

        comment_list = []
        for music_comment in music_comment_list:
            comment = music_comment.comment
            comment_list.append(comment)
        return comment_list

    def __get_by_singer(self, request):

        # Get Comment Information
        singer_name = request.POST.get('singer_name', '')
        singer = Singer_Information.filter(singer_name=singer_name)
        singer_comment_list = User_Comment_Singer.objects.filter(singer=singer)
        singer_comment_list = singer_comment_list.order_by("-comment_time")

        comment_list = []
        for singer_comment in singer_comment_list:
            comment = singer_comment.comment
            comment_list.append(comment)
        return comment_list

    def post(self, request):

        # Two Query Type: Get By Music, Get By Singer
        query_type = request.POST.get('query_type', '')

        # Query Comment By Music
        if query_type == 'music':
            comment_list = self.__get_by_music(request)
        # Query Comment By Singer
        elif query_type == 'singer':
            comment_list = self.__get_by_singer(request)
        else:
            comment_list = []

        # Total Number Of Comments
        comment_num = len(comment_list)

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(comment_list, 10, request=request)
        comment_pages = p.page(page)

        return render(request, 'Comment_Information.html', {
            'comment_pages': comment_pages,
            'comment_num': comment_num,
        })

# Query Feedback Information
class Feedback_View(View):

    def post(self, request):

        # Get Feedback Information
        comment_id = request.POST.get('comment_id', '')
        comment = Comment_Information.objects.filter(comment_id=comment_id)
        comment_feedback_list = User_Feedback_Comment.objects.filter(comment=comment)
        comment_feedback_list = comment_feedback_list.order_by('-feedback_time')

        feedback_list = []
        for comment_feedback in comment_feedback_list:
            feedback = comment_feedback.feedback
            feedback_list.append(feedback)

        # Total Number Of Comments
        feedback_num = len(feedback_list)

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(feedback_list, 10, request=request)
        feedback_pages = p.page(page)

        return render(request, 'Feedback_Information.html', {
            'feedback_pages': feedback_pages,
            'feedback_num': feedback_num,
        })

# Part Four: Entity RelationShip Query After Login: Other User's Public Information

# Get Music By user_id From User_Music
class Get_Music_By_User(LoginRequiredMixin, View):

    def post(self, request):

        # Music Information
        user_id = request.POST.get('user_id', '')
        user = UserProfile.objects.get(user_id=user_id)
        user_music_list = User_Music.objects.filter(user=user)

        music_list = []
        for user_music in user_music_list:
            music = user_music.music
            music_list.append(music)

        # Total Number Of Music
        music_num = music_list.length()

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(music_list, 10, request=request)
        music_pages = p.page(page)

        return render(request, 'Get_Music_Information_By_User.html', {
            'music_pages': music_pages,
            'music_num': music_num,
        })

# Get Singer By user_id From User_Singer
class Get_Singer_By_User(LoginRequiredMixin, View):

    def post(self, request):

        # Get Singer Information
        user_id = request.POST.get('user_id', '')
        user = UserProfile.objects.get(user_id=user_id)
        user_singer_list = User_Singer.objects.filter(user=user)

        singer_list = []
        for user_singer in user_singer_list:
            singer = user_singer.singer
            singer_list.append(singer)

        # Total Number Of Music
        singer_num = singer_list.length()

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(singer_list, 10, request=request)
        singer_pages = p.page(page)

        return render(request, 'Get_Singer_Information_By_User.html', {
            'singer_pages': singer_pages,
            'singer_num': singer_num,
        })

# Get Songsheet By user_id From User_Songsheet
class Get_Songsheet_By_User(LoginRequiredMixin, View):

    def post(self, request):

        # Get Songsheet Information
        user_id = request.POST.get('user_id', '')
        user = UserProfile.objects.get(user_id=user_id)
        user_songsheet_list = User_Songsheet.objects.filter(user=user)

        songsheet_list = []
        for user_songsheet in user_songsheet_list:
            songsheet = user_songsheet.songsheet
            songsheet_list.append(songsheet)

        # Total Number Of Songsheet
        songsheet_num = songsheet_list.length()

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(songsheet_list, 10, request=request)
        songsheet_pages = p.page(page)

        return render(request, 'Get_Songsheet_Information_By_User.html', {
            'songsheet_pages': songsheet_pages,
            'songsheet_num': songsheet_num,
        })

# Part Five: User Operation, Without Association To Other User

# Update My Favorite Music List
class User_Music_View(View):

    def __add_fav(self, request):

        # Get Music Information
        music_id = request.POST.get('music_id', '')
        music = Music_Information.objects.get(music_id=music_id)

        # Check Duplication
        exist_record = User_Music.objects.get(user=request.user, music=music)
        if exist_record:
            return {
                'status': 'fail',
                'msg': '无法重复收藏'
            }

        # Add Information
        user_music = User_Music()
        user_music.user = request.user
        user_music.music = music
        user_music.save()

        return {
            'status': 'success',
            'msg': '收藏成功'
        }

    def __del_fav(self, request):

        # Get Music Information
        music_id = request.POST.get('music_id', '')
        music = Music_Information.objects.get(music_id=music_id)

        # Check Duplication
        exist_record = User_Music.objects.get(user=request.user, music=music)
        if not exist_record:
            return {
                'status': 'fail',
                'msg': '收藏信息不存在'
            }

        # Del Information
        exist_record.delete()

        return {
            'status': 'success',
            'msg': '删除成功'
        }

    def __run(self, request):

        # Get Music Information
        music_id = request.POST.get('music_id', '')
        music = Music_Information.objects.get(music_id=music_id)

        # Check Favorite List
        exist_record = User_Music.objects.get(user=request.user, music=music)
        if exist_record:
            exist_record.run_times += 1
            exist_record.save()

        return {
            'status': 'success',
            'msg': '播放成功'
        }

    def post(self, request):

        # Check User Authenticated
        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        # Three Op: add, delete, run
        op = request.POST.get('op', '')

        # Add Music To Fav List
        if op == 'add':
            ret_info = self.__add_fav(request)
        # Del Music From Fav List
        elif op == 'delete':
            ret_info = self.__del_fav(request)
        # Listen Music
        elif op == 'run':
            ret_info = self.__run(request)
        else:
            ret_info = {
                'status': 'fail',
                'msg': '未知操作'
            }

        return HttpResponse(json.dumps(ret_info), content_type='application/json')

# Update My Favorite Singer List
class User_Singer_View(View):

    def __add_fav(self, request):

        # Get Singer Information
        singer_id = request.POST.get('singer_id', '')
        singer = Singer_Information.objects.get(singer_id=singer_id)

        # Check Duplication
        exist_record = User_Singer.objects.get(user=request.user, singer=singer)
        if exist_record:
            return {
                'status': 'fail',
                'msg': '无法重复关注'
            }

        # Add Information
        user_singer = User_Singer()
        user_singer.user = request.user
        user_singer.singer = singer
        user_singer.save()

        return {
            'status': 'success',
            'msg': '关注成功'
        }

    def __del_fav(self, request):

        # Get Singer Information
        singer_id = request.POST.get('singer_id', '')
        singer = Singer_Information.objects.get(singer_id=singer_id)

        # Check Duplication
        exist_record = User_Singer.objects.get(user=request.user, singer=singer)
        if not exist_record:
            return {
                'status': 'fail',
                'msg': '关注信息不存在'
            }

        # Del Information
        exist_record.delete()

        return {
            'status': 'success',
            'msg': '删除成功'
        }

    def post(self, request):

        # Check User Authenticated
        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        # Two Op: add, delete
        op = request.POST.get('op', '')

        # Add Singer To Fav List
        if op == 'add':
            ret_info = self.__add_fav(request)
        # Del Singer From Fav List
        elif op == 'delete':
            ret_info = self.__del_fav(request)
        else:
            ret_info = {
                'status': 'fail',
                'msg': '未知操作'
            }

        return HttpResponse(json.dumps(ret_info), content_type='application/json')

# Make/Delete Comments On Music Or Singer
class User_Comment_View(View):

    def __make_comment_on_music(self, request):

        # Get Music Information
        music_id = request.POST.get('music_id')
        music = Music_Information.objects.get(music_id=music_id)

        # Insert Into Comment_Information Table
        comment = Comment_Information()
        comment.comment_theme = request.POST.get('comment_theme', '')
        comment.comment_grade = request.POST.get('comment_grade', '')
        comment.comment_content = request.POST.get('comment_content', '')
        comment.save()

        # Insert Into User_Comment_Music Table
        user_comment_music = User_Comment_Music()
        user_comment_music.user = request.user
        user_comment_music.comment = comment
        user_comment_music.target_music = music
        user_comment_music.save()

        return {
            'status': 'success',
            'msg': '发布成功'
        }

    def __make_comment_on_singer(self, request):

        # Get Singer Information
        singer_id = request.POST.get('singer_id')
        singer = Singer_Information.objects.get(singer_id=singer_id)

        # Insert Into Comment_Information Table
        comment = Comment_Information()
        comment.comment_theme = request.POST.get('comment_theme', '')
        comment.comment_grade = request.POST.get('comment_grade', '')
        comment.comment_content = request.POST.get('comment_content', '')
        comment.save()

        # Insert Into User_Comment_Singer Table
        user_comment_singer = User_Comment_Singer()
        user_comment_singer.user = request.user
        user_comment_singer.comment = comment
        user_comment_singer.target_singer = singer
        user_comment_singer.save()

        return {
            'status': 'success',
            'msg': '发布成功'
        }

    def __del_comment(self, request):

        # Get Comment Information
        comment_id = request.POST.get('comment_id')
        comment = Comment_Information.objects.get(comment_id=comment_id)

        comment.delete()
        return {
            'status': 'success',
            'msg': '删除成功'
        }

    def post(self, request):

        # Check User Authenticated
        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        # Three Op: add_comment_on_music, add_comment_on_singer, delete_comment
        op = request.POST.get('op', '')

        # Add Comment On Music
        if op == 'add_comment_on_music':
            ret_info = self.__make_comment_on_music(request)
        # Add Comment On Singer
        elif op == 'add_comment_on_singer':
            ret_info = self.__make_comment_on_singer(request)
        # Delete Comment
        elif op == 'delete_comment':
            ret_info = self.__del_comment(request)
        else:
            ret_info = {
                'status': 'fail',
                'msg': '未知操作'
            }

        return HttpResponse(json.dumps(ret_info), content_type='application/json')

# Make/Delete Feedback On Comment
class User_Feedback_View(View):

    def __add_feedback(self, request):

        # Get Comment Information
        comment_id = request.POST.get('comment_id', '')
        comment = Comment_Information.objects.get(comment_id=comment_id)

        # Insert Into Feedback_Information Table
        feedback = Feedback_Information()
        feedback.feedback_theme = request.POST.get('feedback_theme', '')
        feedback.feedback_content = request.POST.get('feedback_content', '')
        feedback.save()

        # Insert Into User_Feedback_Comment Table
        user_feedback_comment = User_Feedback_Comment()
        user_feedback_comment.user = request.user
        user_feedback_comment.feedback = feedback
        user_feedback_comment.comment = comment
        user_feedback_comment.save()

        return {
            'status': 'success',
            'msg': '回帖成功'
        }

    def __del_feedback(self, request):

        # Get Feedback Information
        feedback_id = request.POST.get('feedback_id', '')
        feedback = Feedback_Information.objects.get(feedback_id=feedback_id)

        feedback.delete()
        return {
            'status': 'success',
            'msg': '删除成功'
        }

    def post(self, request):

        # Check User Authenticated
        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        # Two Op: add_feedback, delete_feedback
        op = request.POST.get('op', '')

        # Add Feedback On Comment
        if op == 'add_feedback':
            ret_info = self.__add_feedback(request)
        # Delete Feedback
        elif op == 'delete_feedback':
            ret_info = self.__del_feedback(request)
        else:
            ret_info = {
                'status': 'fail',
                'msg': '未知操作'
            }

        return HttpResponse(json.dumps(ret_info), content_type='application/json')

# Update Songsheet
class User_Songsheet_Operation_View(View):

    def __create_songsheet(self, request):

        # Insert Into Songsheet_Information Table
        songsheet = Songsheet_Information()
        songsheet.songsheet_name = request.POST.get('songsheet_name', '')
        songsheet.songsheet_access = request.POST.get('songsheet_access', '')
        songsheet.save()

        # Insert Into User_Songsheet_Information Table
        user_songsheet = User_Songsheet()
        user_songsheet.user = request.user
        user_songsheet.songsheet = songsheet
        user_songsheet.save()

        return {
            'status': 'success',
            'msg': '创建成功'
        }

    def __delete_songsheet(self, request):

        # Get Songsheet Information
        songsheet_id = request.POST.get('songsheet_id', '')
        songsheet = Songsheet_Information.objects.get(songsheet_id=songsheet_id)

        songsheet.delete()
        return {
            'status': 'success',
            'msg': '删除成功'
        }

    def __add_music_to_songsheet(self, request):

        # Get Music Information
        music_id = request.POST.get('music_id', '')
        music = Music_Information.objects.get(music_id=music_id)

        # Get Songsheet Information
        songsheet_id = request.POST.get('songsheet_id', '')
        songsheet = Songsheet_Information.objects.get(songsheet_id=songsheet_id)

        # Check Duplication
        exists_record = Songsheet_Music.objects.get(songsheet=songsheet, music=music)
        if exists_record:
            return {
                'status': 'fail',
                'msg': '重复添加'
            }

        # Update Songsheet_Music Table
        songsheet_music = Songsheet_Music()
        songsheet_music.songsheet = songsheet
        songsheet_music.music = music
        songsheet.save()

        # Update User_Songsheet Table
        user_songsheet = User_Songsheet.objects.get(user=request.user, songsheet=songsheet)
        user_songsheet.update_time = datetime.date.today()
        user_songsheet.save()

        return {
            'statue': 'success',
            'msg': '添加成功'
        }

    def __del_music_from_songsheet(self, request):

        # Get Music Information
        music_id = request.POST.get('music_id', '')
        music = Music_Information.objects.get(music_id=music_id)

        # Get Songsheet Information
        songsheet_id = request.POST.get('songsheet_id', '')
        songsheet = Songsheet_Information.objects.get(songsheet_id=songsheet_id)

        # Check Duplication
        exists_record = Songsheet_Music.objects.get(songsheet=songsheet, music=music)
        if not exists_record:
            return {
                'status': 'fail',
                'msg': '不存在该歌曲'
            }

        # Update Songsheet_Music Table
        exists_record.delete()

        # Update User_Songsheet Table
        user_songsheet = User_Songsheet.objects.get(user=request.user, songsheet=songsheet)
        user_songsheet.update_time = datetime.date.today()
        user_songsheet.save()

        return {
            'statue': 'success',
            'msg': '移除成功'
        }

    def post(self, request):

        # Check User Authenticated
        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        # Four Op: create songsheet, delete songsheet, add music to songsheet, remove music from songsheet
        op = request.POST.get('op', '')

        # create songsheet
        if op == 'create_songsheet':
            ret_info = self.__create_songsheet(request)
        # delete songsheet
        elif op == 'delete_songsheet':
            ret_info = self.__delete_songsheet(request)
        # add music to songsheet
        elif op == 'add_music_to_songsheet':
            ret_info = self.__add_music_to_songsheet(request)
        # delete music from songsheet
        elif op == 'remove music from songsheet':
            ret_info = self.__del_music_from_songsheet(request)
        else:
            ret_info = {
                'status': 'fail',
                'msg': '未知操作'
            }

        return HttpResponse(json.dumps(ret_info), content_type='application/json')

# Display The Song sheets Created By The User
class User_Songsheet_View(View):

    def get(self, request):

        # Check User Authenticated
        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        # Get The Songsheet Information
        user_songsheet_list = User_Songsheet.objects.filter(user=request.user)
        songsheet_list = []
        for user_songsheet in user_songsheet_list:
            songsheet = user_songsheet.songsheet
            songsheet_list.append(songsheet)

        # Total Number Of Song sheets
        songsheet_num = len(songsheet_list)

        # Paging The Information
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(songsheet_list, 10, request=request)
        songsheet_pages = p.page(page)

        return render(request, 'Songsheet_Information.html', {
            'songsheet_pages': songsheet_pages,
            'songsheet_num': songsheet_num,
        })

# Part Six: User Operation, Associated With Other User

# Add Or Delete Other User From Contact List
class User_User(View):

    def __add(self, request):

        # User Information
        tar_user_id = request.POST.get('user_id', '')
        tar_user = UserProfile.objects.get(user_id=tar_user_id)

        # Check Duplication
        exist_record = User_Relationship.objects.get(user_1=request.user, user_2=tar_user)
        if exist_record:
            return {
                'status': 'fail',
                'msg': '重复关注'
            }

        # Insert Into User Relationship Table
        user_relationship = User_Relationship()
        user_relationship.user_1 = request.user
        user_relationship.user_2 = tar_user
        user_relationship.save()

        return {
            'status': 'success',
            'msg': '关注成功'
        }

    def __del(self, request):

        # User Information
        tar_user_id = request.POST.get('user_id', '')
        tar_user = UserProfile.objects.get(user_id=tar_user_id)

        # Check Duplication
        exist_record = User_Relationship.objects.get(user_1=request.user, user_2=tar_user)
        if not exist_record:
            return {
                'status': 'fail',
                'msg': '不存在该用户'
            }

        # Delete User Relationship
        exist_record.delete()

        return {
            'status': 'success',
            'msg': '关注成功'
        }

    def post(self, request):

        # Check User Authenticated
        res = dict()
        if not request.user.is_authenticated:
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        # Two Op: add or remove user from contact list
        op = request.POST.get('op', '')

        # create songsheet
        if op == 'add_user':
            ret_info = self.__add(request)
        # delete songsheet
        elif op == 'delete_user':
            ret_info = self.__del(request)
        else:
            ret_info = {
                'status': 'fail',
                'msg': '未知操作'
            }

        return HttpResponse(json.dumps(ret_info), content_type='application/json')

# Check Other's Songsheet
class Check_Songsheet(View):

    def post(self, request):

        # Get Songsheet Information
        songsheet_id = request.POST.get('songsheet_id', '')
        songsheet = Songsheet_Information.objects.get(songsheet_id=songsheet_id)

        # Get User Information
        user_songsheet = User_Songsheet.objects.get(songsheet=songsheet)
        owner = user_songsheet.user

        exist_relationship = User_Relationship.objects.get(user_1=request.user, user_2=owner)
        if exist_relationship:

            songsheet_music_list = Songsheet_Music.objects.get(songsheet=songsheet)
            music_list = []
            for songsheet_music in songsheet_music_list:
                music_list.append(songsheet_music.music)
            music_num = len(music_list)

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(music_list, 10, request=request)
            music_pages = p.page(page)

            return render(request, 'Songsheet_View.html', {
                'music_pages': music_pages,
                'music_num': music_num,
            })
        else:
            ret_info = {'status': 'fail', 'msg': '未关注该用户'}
            return HttpResponse(json.dumps(ret_info), content_type='application/json')

# Part Seven: About My Songsheet

# List My Songsheet
class My_Songsheet_List(View):

    def post(self, request):

        # Get Songsheet List
        user_songsheet_list = User_Songsheet.objects.filter(user=request.user)
        songsheet_list = []
        for user_songsheet in user_songsheet_list:
            songsheet_list.append(user_songsheet.songsheet)

        return render(request, 'My_Songsheet.html', {
            'songsheet_list': songsheet_list,
            'songsheet_num': len(songsheet_list),
        })
