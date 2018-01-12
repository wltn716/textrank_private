from django.shortcuts import render
#모델
from .models import Post 
#TextRank 관련 클래스
from .neededClasses import TextRank

def post_list(request):
	url = 'http://v.media.daum.net/v/20170611192209012?rcmd=r'
	textrank = TextRank(url)
	posts = textrank.summarize(3)
	keywords = textrank.keywords()
	return render(request, 'blog/post_list.html', {'posts': posts, 'keywords': keywords})