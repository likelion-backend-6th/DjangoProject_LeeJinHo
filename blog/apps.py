#카탈로그 애플리케이션의 주요 설정을 포함합니다
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
