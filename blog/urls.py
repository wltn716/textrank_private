from django.conf.urls import url
from . import views
app_name='dic'

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^search$', views.search, name='api_search'),
    url(r'^word$', views.word_graph, name='word_graph'),
    url(r'^graphFile$', views.graph_file, name='graph_file'),
]
