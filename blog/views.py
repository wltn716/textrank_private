import json
import urllib
import urllib.request

from django.shortcuts import render
#모델
from .models import Post
#TextRank 관련 클래스
from .neededClasses import TextRank
from .forms import PostForm

from django.shortcuts import render

def index(request):
	return render(request, 'blog/index.html', {})

def content(request):
	# url = 'http://v.media.daum.net/v/20170611192209012?rcmd=r'
	return render(request, 'blog/content.html', {})

def result(request):
	content= request.POST['content']
	textrank = TextRank(content)
	texts = textrank.sent_tokenize.origin_text
	posts = textrank.summarize(3)
	keywords = textrank.keywords()
	return render(request, 'blog/result.html', {'texts': texts,'posts': posts, 'keywords': keywords})

def word_graph(request):
	return render(request, 'blog/word.html', {})

def graph_file(request):
	return render(request, 'blog/graphFile.json', {})

def search(request):

	if request.method == 'GET':

		client_id = "XkxUvnjBBEJZqh3oIlbK"
		client_secret = "dg_TgKomla"

		q = request.GET.get('q')
		encText = urllib.parse.quote("{}".format(q))
		url = "https://openapi.naver.com/v1/search/encyc?query=" + encText
		dic_api_request = urllib.request.Request(url)
		dic_api_request.add_header("X-Naver-Client-Id", client_id)
		dic_api_request.add_header("X-Naver-Client-Secret",client_secret)
		response = urllib.request.urlopen(dic_api_request)
		rescode = response.getcode()
		if (rescode == 200):
			response_body = response.read()
			result = json.loads(response_body.decode('utf-8'))
			items = result.get('items')
			print(result)  # request를 예쁘게 출력해볼 수 있다.

			context = {
				'items': items
			}
		return render(request, 'blog/search.html', context=context)
