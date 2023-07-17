# 모델을 등록하여 장고 관리 사이트에 포함시킬 수 있습니다.관리사이트 사용은 선택 사항
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
