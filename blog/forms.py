from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)  # 글을 보내는 사람의 이름
    email = forms.EmailField()  # 글 추천하는 사람의 이메일
    to = forms.EmailField()  # 글 추천 이메일을 수신할 사람의 이메일
    comments = forms.CharField(required=False, widget=forms.Textarea)  # 글 추천 이메일 코멘트


#3. 폼 생성
class CommentForm(forms.ModelForm):
    class Meta: #모델로부터 폼을 생성하기 위해, 폼의 Meta클래스에서 어떤 모델을 사용할지 지정
        model = Comment
        fields = ['name', 'email', 'body'] #폼에 포함되는 필드 3개
