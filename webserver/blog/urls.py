from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^user_login$', views.user_login, name='user_login'),
    url(r'^user_logout$', views.user_logout, name='user_logout'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    #url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),

    # blog/create_new_post
    url(r'^create_new_post/$', views.create_new_post, name='create_new_post'),

    # blog/post_update
    url(r'^post_update/(?P<slug>[-\w]+)/$', views.post_update, name='post_update'),

    # blog/markdown_edit
    url(r'^markdown_edit/$', views.markdown_edit, name='markdown_edit'),

    # blog/ajax/preview
    url(r'^ajax/preview$', views.ajax_preview, name='ajax_preview'),

]
