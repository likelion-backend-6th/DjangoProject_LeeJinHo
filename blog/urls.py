from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'), 이전 URL 패턴
    path('', views.PostListView.as_view(), name='post_list'),  # PostListView 클래스 사용
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<post>[-\w]+)/$', views.post_detail,
            name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),

#5. URL패턴 생성
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
