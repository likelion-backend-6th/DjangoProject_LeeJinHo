from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('list/', views.post_list, name='post_list'),
    path('', views.post_list, name='post_list'), #함수형 뷰로 만드니까 페이지네이션 작동
    #path('', views.PostListView.as_view(), name='post_list'), #PostListView 클래스 사용
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<post>[-\w]+)/$', views.post_detail,
            name='post_detail'),
#5. URL패턴 생성
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('tag/<tag_slug>/', views.post_list, name='post_list_by_tag'),
]
