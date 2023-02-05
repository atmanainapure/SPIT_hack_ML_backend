from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload_s', views.upload_s, name='upload_s'),
    path('upload_a', views.upload_a, name='upload_a'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('syllabus_home', views.syllabus_home, name='syllabus_home'),
    path('syllabus', views.syllabus, name='syllabus'),
    path('index_tensor', views.index_tensor, name='index_tensor')
]