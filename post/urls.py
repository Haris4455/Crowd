from django.urls import path
from post.views import index, NewPost, PostDetails, tags, like, favorite, post_del, post_edit


urlpatterns = [
   	path('', index, name='index'),
   	path('newpost/', NewPost, name='newpost'),
   	path('<uuid:post_id>', PostDetails, name='postdetails'),
   	path('<uuid:post_id>/like', like, name='postlike'),
   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
   	path('tag/<slug:tag_slug>', tags, name='tags'),
	path('<uuid:post_id>/delete', post_del, name='postdel'),
	path('updatepost/<uuid:post_id>/', post_edit, name='postedit'),
]