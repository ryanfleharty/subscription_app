from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[0-9]+)$', views.show, name='show'),
    url(r'^manage$', views.manage, name='manage'),
    url(r'^sub_form_expansion$', views.sub_form_expansion, name='sub_form_expansion'),
    url(r'^subscribe/(?P<id>[0-9]+)$', views.subscribe, name='subscribe'),
    url(r'^unsubscribe/(?P<id>[0-9]+)$', views.unsubscribe, name='unsubscribe'),
    url(r'^subscribe_bulk$', views.subscribe_bulk, name='subscribe_bulk'),
    url(r'^unsubscribe_bulk$', views.unsubscribe_bulk, name='unsubscribe_bulk'),
    url(r'^search_comics$', views.search, name='search'),
    url(r'^browse_comics$', views.browse, name='browse'),
    url(r'^import_comics$', views.import_comics, name='import_comics'),
    url(r'^add_review/(?P<id>[0-9]+)$', views.add_review, name='add_review'),
    url(r'^add_comment/(?P<id>[0-9]+)$', views.add_comment, name='add_comment'),
    url(r'^jump_to_issue$', views.jump_to_issue, name='jump_to_issue'),
    url(r'^(?P<title>[\w]+( \w+)*)$', views.show_by_title, name='show_by_title'),
    url(r'^(?P<title>[\w]+( \w+)*)/(?P<issue_num>[0-9]+)$', views.show_issue, name='show_issue'),
    url(r'^(?P<title>[\w]+( \w+)*)/(?P<issue_num>[0-9]+)/add_review$', views.add_issue_review, name='add_issue_review'),
]
