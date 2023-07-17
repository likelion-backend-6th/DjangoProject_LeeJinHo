# 카탈로그 데이터 모델 model.py
from django.db import models
from django.utils import timezone


class Post(models.Model):
    #id = 자동생성(BigAutoField)
    title = models.CharField(max_length=250)  # 글의 제목을 위한 필드, SQL에서 VARCHAR열로 변환
    slug = models.SlugField(max_length=250)  # SlugField필드, 문자,숫자,밑줄,하이픈만 포함하는 짧은 레이블, SEO친화적인 URL구성
    body = models.TextField()  # 글의 본문을 저장하는 필드, SQL에서 TEXT열로 변환
    publish = models.DateTimeField(default=timezone.now) #datatime.now의 시간대를 고려한 버전
    created = models.DateTimeField(auto_now_add=True) #게시물 create 날짜 시간 저장, auto_now_add 객체를 생성할 때 날짜 저장
    updated = models.DateTimeField(auto_now=True) #게시물의 last update 날짜 저장, auto_now를 사용하여 객체 저장시 update

    def __str__(self):  # 장고 admin사이트를 포함하여 여러곳에서 해당 객체 이름을 표시
        return self.title
