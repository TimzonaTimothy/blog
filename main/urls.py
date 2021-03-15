from django.conf.urls import re_path
from django.urls import path
from main import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^$',views.PostListView.as_view(),name='post_list'),
    re_path(r'^home/$',views.PostListView.as_view(),name='home'),
    re_path(r'^about/$',views.AdvertView.as_view(),name='advert'),
    re_path(r'^post/(?P<pk>\d+)$',views.PostDetailView.as_view(),name='post_detail'),
    re_path(r'^add_post/$',views.CreatePostView.as_view(), name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$',views.UpdatePostView.as_view(), name='post_edit'),
    re_path(r'^post/(?P<pk>\d+)/remove/$',views.PostDeleteView.as_view(),name='post_remove'),
    # re_path(r'^drafts/$',views.DraftListView.as_view(), name='post_drafts_list'),
    re_path(r'^post/(?P<pk>\d+)/comment/$',views.add_comment_to_post,name="add_comment_to_post"),
    re_path(r'^add_category/$',views.AddCategoryView.as_view(),name='add_category'),
    re_path(r'^post/(?P<pk>\d+)/publish/$',views.post_publish,name="post_publish"),
    re_path(r'unsubscribe/$',views.news_unsub,name='unsub'),
    re_path(r'subscribe/$',views.newsletter_subscribe,name='subscribe'),
    path('category/<str:cats>/',views.CategoryView,name='category'),
    path('category-list/',views.CategoryListView,name='category-list'),
    path('contact',views.contact, name="contact"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
