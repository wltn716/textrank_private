# 01/25 SEOHYUN 20:58 edited
from django.conf.urls import url
from . import views
app_name='dic'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^content$', views.content, name='content'),
    url(r'^search$', views.search, name='api_search'),
    url(r'^result$', views.result, name='result'),
    url(r'^word$', views.word_graph, name='word_graph'),
    url(r'^graphFile$', views.graph_file, name='graph_file'),
]
