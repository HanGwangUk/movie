from django.urls import path
from . import views

app_name = "movies"

urlpatterns=[
    path('', views.first_page, name='first_page'),
    path('chajja/', views.index, name="index"),
    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:movie_pk>/delete', views.movie_delete, name='movie_delete'),
    path('<int:movie_pk>/update', views.movie_update, name='movie_update'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/rank/', views.rank, name='rank'),
    path('<int:movie_pk>/rank_cancle/', views.rank_cancle, name='rank_cancle'),
    path('<int:movie_pk>/review_create/', views.review_create, name='review_create'),
    path('<int:movie_pk>/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/<int:review_pk>/update', views.review_update, name='review_update'),
    path('<int:movie_pk>/<int:review_pk>/delete', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/<int:review_pk>/comments', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/comment_update', views.comment_update, name='comment_update'),
    path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/comment_delete', views.comment_delete, name='comment_delete'),
    # path('<int:movie_pk>/rank', views.rank, name='rank')



]