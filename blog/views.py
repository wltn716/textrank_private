from django.shortcuts import render
#모델
from .models import Post
#TextRank 관련 클래스
from .neededClasses import TextRank
from .forms import PostForm


def index(request):
	return render(request, 'blog/index.html', {})

def content(request):
	# url = 'http://v.media.daum.net/v/20170611192209012?rcmd=r'
	return render(request, 'blog/content.html', {})

def result(request):
	url = request.POST['url']
	textrank = TextRank(url)
	texts = textrank.sent_tokenize.origin_text
	posts = textrank.summarize(3)
	keywords = textrank.keywords()
	return render(request, 'blog/result.html', {'texts': texts,'posts': posts, 'keywords': keywords})
