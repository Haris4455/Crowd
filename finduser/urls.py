from django.urls import path
from finduser.views import UserSearchu
urlpatterns = [
	path('', UserSearchu, name='usersearch1'),
]