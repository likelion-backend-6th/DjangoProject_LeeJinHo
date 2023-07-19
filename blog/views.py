# 어플리케이션의 로직이 들어갑니다.각 뷰는 HTTP요청을 받아 처리하고 응답을 반환
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator


# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3) # 페이지당 3개의 게시물로 페이지네이션
    page_number = request.GET.get('page', 1)

    posts = paginator.page(page_number)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    # 날짜 및 post인수를 받아와 주어진 슬러그와 출판일을 가진 게시글 검색
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})
