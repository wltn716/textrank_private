from django.conf.urls import url
from . import views
app_name='dic'

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^content$', views.content, name='content'),
    url(r'^result$', views.result, name='result'),
    url(r'^word$', views.word_graph, name='word_graph'),
    
    #회원관리 관련
    url(r'^sign_up/$', views.signup, name='sign_up'),
    url(r'^sign_in/$', views.signin, name='sign_in'),
]
