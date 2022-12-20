from django.db import models
from users.models import UserProfile
import datetime

# Create your models here.

class Music_Information(models.Model):

    singing_type = [
        (1, "solo"),
        (2, "antiphon"),
        (3, "chorus")
    ]

    theme = [
        (1, "History"),
        (2, "Anecdote"),
        (3, "Emotion"),
        (4, "Game"),
        (5, "Encouragement"),
        (6, "Nation"),
        (7, "Other")
    ]

    music_id = models.AutoField(primary_key=True, verbose_name="歌曲id")
    music_name = models.CharField(max_length=32, verbose_name="歌曲名称", null=False)
    music_singing_type = models.CharField(choices=singing_type, max_length=10, verbose_name="歌曲演唱形式", null=False)
    music_theme = models.CharField(choices=theme, max_length=20, verbose_name="歌曲主题", null=False)
    music_duration = models.IntegerField(verbose_name="歌曲时长", null=False, default=3)
    music_popularity = models.IntegerField(verbose_name="歌曲流行度", null=False, default=0)
    music_link = models.CharField(max_length=1000, verbose_name="播放链接", default="http://ws.stream.qqmusic.qq.com/C400003UkWuI0E8U0l.m4a?guid=472740677&vkey=E3E33D1B7EEEC9C30F9D1F0E42E27F00CB92E8515BC8442E617ACEF1F646C6F9DD9397DD7DBED4300B1A044D27237FFD76D00883AB7FE62B&uin=&fromtag=120032")
    music_public_time = models.DateField(verbose_name="歌曲创作时间", default=datetime.date.today())

class Singer_Information(models.Model):

    nationality = [
        (1, "China"),
        (2, "USA"),
        (3, "UK"),
        (4, "Japan"),
        (5, "France"),
        (6, "Germany"),
        (7, "Koera"),
        (8, "Russia"),
        (9, "Italy"),
        (10, "Spain"),
        (11, "Australia"),
        (12, "Canada")
    ]

    sex = [
        (1, "Male"),
        (2, "Female")
    ]

    singer_id = models.AutoField(primary_key=True, verbose_name="歌手id")
    singer_name = models.CharField(max_length=10, verbose_name="歌手姓名", null=False)
    singer_nationality = models.CharField(max_length=10, choices=nationality, verbose_name="歌手国籍", null=False)
    singer_age = models.IntegerField(verbose_name="歌手年龄", null=False)
    singer_sex = models.CharField(max_length=10, choices=sex, verbose_name="歌手性别", null=False)
    singer_popularity = models.IntegerField(verbose_name="歌手热度", null=False, default=0)
    singer_debut_time = models.DateField(verbose_name="歌手出道时间", null=False, default=datetime.date.today())

    class Meta:
        managed = True
        db_table = "singer_information"

class Album_Information(models.Model):

    coverpage_pattern = [
        (1, "Simple"),
        (2, "Bright"),
        (3, "Dim"),
    ]

    album_id = models.AutoField(primary_key=True, verbose_name="专辑id")
    album_name = models.CharField(max_length=30, verbose_name="专辑名称", null=False)
    album_coverpage_pattern = models.CharField(max_length=10, choices=coverpage_pattern,
                                               verbose_name="专辑封面设计方式", null=False)
    album_music_num = models.IntegerField(verbose_name="专辑包含歌曲数量", null=False, default=0)
    album_created_time = models.DateField(verbose_name="专辑创建时间", null=False,default=datetime.date.today())
    album_popularity = models.IntegerField(verbose_name="专辑热度", null=False,default=0)

    class Meta:
        managed = True
        db_table = "album_information"

class Songsheet_Information(models.Model):

    songsheet_id = models.AutoField(primary_key=True, verbose_name="Songsheet Id")
    songsheet_name = models.CharField(max_length=32, verbose_name="Songsheet Name", null=False)

    class Meta:
        managed = True
        db_table = "Songsheet_Information"

class Comment_Information(models.Model):

    grade = [
        (1, "Positive"),
        (2, "Normal"),
        (3, "Negative")
    ]

    comment_id = models.AutoField(primary_key=True, verbose_name="评论id")
    comment_theme = models.CharField(max_length=100, verbose_name="评论主题", null=False)
    comment_grade = models.CharField(choices=grade, max_length=10, verbose_name="评论基调", null=False)
    comment_content = models.CharField(max_length=10000, verbose_name="评论内容", null=False)
    comment_time = models.DateTimeField(verbose_name='评论时间', default=datetime.datetime.now())

    class Meta:
        managed = True
        db_table = "comment_information"

class Feedback_Information(models.Model):

    feedback_id = models.AutoField(primary_key=True, verbose_name="回帖id")
    feedback_theme = models.CharField(max_length=100, verbose_name="回帖主题", null=False)
    feedback_content = models.CharField(max_length=10000, verbose_name="回帖内容", null=False)

    class Meta:
        managed = True
        db_table = "feedback_information"

class Singer_Music(models.Model):

    singer = models.ForeignKey(Singer_Information, on_delete=models.CASCADE, default="")
    music = models.ForeignKey(Music_Information, on_delete=models.CASCADE, default="")
    sing_time = models.DateField(verbose_name='演唱时间', default=datetime.date.today())

    class Meta:
        managed = True
        db_table = "singer_music"

class Singer_Album(models.Model):

    singer = models.ForeignKey(Singer_Information, on_delete=models.CASCADE, default="")
    album = models.ForeignKey(Album_Information, on_delete=models.CASCADE, default="")

    class Meta:
        managed = True
        db_table = "singer_album"

class Album_Music(models.Model):

    album = models.ForeignKey(Album_Information, on_delete=models.CASCADE, default="")
    music = models.ForeignKey(Music_Information, on_delete=models.CASCADE, default="")
    join_time = models.DateField(verbose_name="歌曲加入专辑的时间", default=datetime.date.today())

    class Meta:
        managed = True
        db_table = "album_music"

class User_Music(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    music = models.ForeignKey(Music_Information, on_delete=models.CASCADE, default="")
    store_times = models.DateField(verbose_name="用户收藏歌曲的时间", default=datetime.date.today())
    run_times = models.IntegerField(verbose_name='用户播放歌曲的次数', default=0)

    class Meta:
        managed = True
        db_table = "user_music"

class User_Songsheet(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='User', default="")
    songsheet = models.ForeignKey(Songsheet_Information, on_delete=models.CASCADE, verbose_name='Songsheet', default="")
    create_time = models.DateField(verbose_name='创建时间', default=datetime.date.today())
    update_time = models.DateField(verbose_name='更新时间', default=datetime.date.today())

    class Meta:
        managed = True
        db_table = "User_Songsheet"

class Songsheet_Music(models.Model):

    songsheet = models.ForeignKey(Songsheet_Information, on_delete=models.CASCADE, default="")
    music = models.ForeignKey(Music_Information, on_delete=models.CASCADE, default="")
    join_time = models.DateField(verbose_name="歌曲加入歌单的时间", default=datetime.date.today())

    class Meta:
        managed = True
        db_table = "songsheet_music"

class User_Singer(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    singer = models.ForeignKey(Singer_Information, on_delete=models.CASCADE, default="")
    attention_time = models.DateField(verbose_name="用户关注该歌手的时间", default=datetime.date.today())

    class Meta:
        managed = True
        db_table = "user_singer"

class User_Comment_Music(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    comment = models.ForeignKey(Comment_Information, on_delete=models.CASCADE, default="")
    target_music = models.ForeignKey(Music_Information, on_delete=models.CASCADE, default="")

    class Meta:
        managed = True
        db_table = "user_comment_music"

class User_Comment_Singer(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    comment = models.ForeignKey(Comment_Information, on_delete=models.CASCADE, default="")
    target_singer = models.ForeignKey(Singer_Information, on_delete=models.CASCADE, default="")

    class Meta:
        managed = True
        db_table = "user_comment_singer"

class User_Feedback_Comment(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    feedback = models.ForeignKey(Feedback_Information, on_delete=models.CASCADE, default="")
    comment = models.ForeignKey(Comment_Information, on_delete=models.CASCADE, default="")
    feedback_time = models.DateField(verbose_name='回帖时间', default=datetime.date.today())

    class Meta:
        managed = True
        db_table = "user_feedback_comment"

class User_Become_Singer(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户账号')
    singer = models.ForeignKey(Singer_Information, on_delete=models.CASCADE, verbose_name='歌手账号')

class Singer_Write_Music(models.Model):

    singer = models.ForeignKey(Singer_Information, on_delete=models.CASCADE, verbose_name="创作者")
    music = models.ForeignKey(Music_Information, on_delete=models.CASCADE, verbose_name="歌曲")
    public_time = models.DateField(verbose_name="出版时间", default=datetime.date.today())

