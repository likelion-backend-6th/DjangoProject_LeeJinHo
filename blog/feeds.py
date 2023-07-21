import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list') #reverse의 지연평가버전 URL구성 로드전에 URL반전 가능
    description = 'New posts of my blog.'

    def items(self): #피드에 포함될 객체 검색, 마지막5개 글
        return Post.published.all()[:5]

    # 각 객체의 제목, 설명, 발행일 반환 3개 메서드
    def item_title(self, item):
        return item.title

    def item_description(self, item): #markdown함수로 마크다운을 html로 변환하고 30단어로 자름
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
