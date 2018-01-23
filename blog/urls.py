from django.conf.urls import url
from . import views
app_name='dic'

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^content$', views.content, name='content'),
    url(r'^result$', views.result, name='result'),
    url(r'^word$', views.word_graph, name='word_graph'),
]
