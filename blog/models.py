# 카탈로그 데이터 모델 model.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):  # TextChoices를 상속받는 열거형 클래스
        DRAFT = 'DF', 'Draft'  # 게시물 상태 : 임시
        PUBLISHED = 'PB', 'Published'  # 게시물 상태 : 게시됨

    # id = 자동생성(BigAutoField)
    title = models.CharField(max_length=250)  # 글의 제목을 위한 필드, SQL에서 VARCHAR열로 변환
    slug = models.SlugField(max_length=250, unique_for_date='publish', allow_unicode=True)# SlugField필드, 문자,숫자,밑줄,하이픈만 포함하는 짧은 레이블, SEO친화적인 URL구성
    tags = TaggableManager()
    author = models.ForeignKey(  # 장고가 관련모델의 기본키를 사용하여 데이터베이스에서 외래키를 생성함
        User,  # import한 User모델, M:1 관계, 사용자는 여러글을 작성한다
        on_delete=models.CASCADE,  # 객체가 삭제될 시 동작, 사용자가 삭제되면 글도 삭제된다
        related_name='blog_posts',  # user.blog_posts로 객체접근 가능
    )
    body = models.TextField()  # 글의 본문을 저장하는 필드, SQL에서 TEXT열로 변환
    publish = models.DateTimeField(default=timezone.now)  # datatime.now의 시간대를 고려한 버전
    created = models.DateTimeField(auto_now_add=True)  # 게시물 create 날짜 시간 저장, auto_now_add 객체를 생성할 때 날짜 저장
    updated = models.DateTimeField(auto_now=True)  # 게시물의 last update 날짜 저장, auto_now를 사용하여 객체 저장시 update

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    objects = models.Manager()  # 기본 매니저
    published = PublishedManager()  # 사용자 정의 매니저

    class Meta:  # 메타 내부클래스
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):  # 장고 admin사이트를 포함하여 여러곳에서 해당 객체 이름을 표시
        return self.title

    def get_absolute_url(self):
        #정규 URL의 매개변수도 수정.
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


#1. 댓글 모델 생성, 이후 마이그레이션
class Comment(models.Model):
    post = models.ForeignKey(Post, #게시물과 댓글을 연결하기 위한 외래키
                             on_delete=models.CASCADE,
                             related_name='comments') #related_name으로 연결된 객체로부터 이 객체로의 관계에 대한 속성 이름을 지정
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True) #생성시 날짜 add
    updated = models.DateTimeField(auto_now=True) #auto_now를 사용하여 객체 저장시 update
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'