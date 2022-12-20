# python file
# author: 梁绪宁

from django.urls import path
from .views import (
    Music_Information_View,
    Music_View,
    Singer_Information_View,
    Singer_View,
    Album_Information_View,
    Album_View,
    Comment_View,
    User_View,
    Personal_View,
    Songsheet_View,
    Singer_Registration_View,
    # Singer_Operation,
)

urlpatterns = [
    path('Music_Information_View/', Music_Information_View.as_view(), name='Music_Information_View'),
    path('Music_View/', Music_View.as_view(), name='Music_View'),
    path('Singer_Information_View/', Singer_Information_View.as_view(), name='Singer_Information_View'),
    path('Singer_View/', Singer_View.as_view(), name='Singer_View'),
    path('Album_Information_View/', Album_Information_View.as_view(), name='Album_Information_View'),
    path('Album_View/', Album_View.as_view(), name='Album_View'),
    path('Comment_View/', Comment_View.as_view(), name='Comment_View'),
    path('User_View/', User_View.as_view(), name='User_View'),
    path('Personal_View/', Personal_View.as_view(), name='Personal_View'),
    path('Songsheet_View/', Songsheet_View.as_view(), name='Songsheet_View'),
    path('Singer_Registration_View/', Singer_Registration_View.as_view(), name='Singer_Registration_View'),
    # path('Singer_Operation/', Singer_Operation.as_view(), name='Singer_Operation'),
]
