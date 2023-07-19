from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) #글을 보내는 사람의 이름
    email = forms.EmailField() #글 추천하는 사람의 이메일
    to = forms.EmailField() #글 추천 이메일을 수신할 사람의 이메일
    comments = forms.CharField(required=False, widget=forms.Textarea) #글 추천 이메일 코멘트
