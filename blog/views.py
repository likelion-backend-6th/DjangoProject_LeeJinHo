# 어플리케이션의 로직이 들어갑니다.각 뷰는 HTTP요청을 받아 처리하고 응답을 반환
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count


class PostListView(ListView):
    # 대체글 목록뷰
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# Create your views here.
def post_list(request, tag_slug=None):
    per_page = request.GET.get('per_page', 3)  # per_page가 없으면 3을 가져옴(동적으로 우선은 3개를 가져오게함)
    page_number = request.GET.get('page', 1)  # page_number가 없으면 1을 가져옴
    post_list = Post.published.all()  # published인 글들만 모두 가져옴
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)  # slug가 없으면 404
        post_list = post_list.filter(tags__in=[tag])

    # 페이지네이터 클래스로 객체 생성
    paginator = Paginator(post_list, per_page, orphans=1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    # 날짜 및 post인수를 받아와 주어진 슬러그와 출판일을 가진 게시글 검색
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)  # 쿼리셋 추가, 해당포스트의 활성 댓글을 가져오기 위해
    # Comment 모델에 직접 구축하는 대신 post객체를 활용해 관련 Comment 객체를 가져옴
    form = CommentForm()  # 댓글 폼 인스턴스 생성

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


def post_share(request, post_id):
    # id로 게시글 조회
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        # 폼이 제출되었을 때
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 폼 필드가 유효성 검사를 통과
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}님이 {post.title}을(를) 추천합니다."
            message = f"{post.title}을(를) 다음에서 읽어보세요.\n\n" \
                      f"{cd['name']}의 의견: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
        sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


# 4. 뷰에서 ModelForm 처리
@require_POST  # 데코레이터를 사용해 POST요청만 허용하도록 설정함
def post_comment(request, post_id):  # requet객체와 post_id를 매개변수로 받음 이 뷰를 사용하여 댓글 제출 관리
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)  # PUBLISHED인 게시물을 가져옴
    comment = None  # 이 변수는 댓글 객체를 저장
    form = CommentForm(data=request.POST)
    if form.is_valid():  # 유효성검사
        comment = form.save(commit=False)  # 댓글 객체 생성(데이터 베이스 저장X, 저장전 수정가능)
        comment.post = post  # 댓글을 게시물에 할당
        comment.save()  # 댓글을 데이터베이스에 저장
    return render(request, 'blog/post/comment.html',  # 탬플릿 랜더링
                  {'post': post, 'form': form, 'comment': comment})  # 객체를 템플릿 컨텍스트로 전달
