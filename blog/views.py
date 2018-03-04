import json
# import urllib
# import urllib.request
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.views.generic import View


#모델 및 폼
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import PostForm, UserForm, LoginForm

#TextRank 관련 클래스
from .neededClasses import TextRank


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


	k4g = {"nodes":[],"links":[]}
	for i in range(len(keywords)):
		k4g["nodes"].append({"name": keywords[i], "group":1})
		if i!=0:
			k4g["links"].append({"source": 0, "target": i, "weight":1})

	return render(request, 'blog/result.html', {'texts': texts,'posts': posts, 'keywords': json.dumps(k4g, ensure_ascii=False)})

def signup(request):
    if request.method == "POST":
    	form = UserForm(request.POST)
    	print(form)
    	if form.is_valid():
    		new_user = User.objects.create_user(**form.cleaned_data)
    		login(request, new_user)
    		return redirect('/content')
    	else:
    		return render(request, 'blog/sign_up.html', {'form': form})
    else:
        form = UserForm()
        return render(request, 'blog/sign_up.html', {'form': form})

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/content')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'blog/sign_in.html', {'form': form})

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
