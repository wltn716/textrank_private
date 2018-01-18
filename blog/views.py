from django.shortcuts import render
#모델
from .models import Post 
#TextRank 관련 클래스
from .neededClasses import TextRank
from .forms import PostForm

def post_list(request):
	# url = 'http://v.media.daum.net/v/20170611192209012?rcmd=r'
	return render(request, 'blog/post_list.html', {})

def receive(request):
	url = request.POST['url']
	textrank = TextRank(url)
	posts = textrank.summarize(3)
	keywords = textrank.keywords()
	return render(request, 'blog/receive.html', {'posts': posts, 'keywords': keywords,})
