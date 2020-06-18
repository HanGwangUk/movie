from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# 슈퍼유저인지 알아보기 위한 데코레이터
from django.contrib.auth.decorators import user_passes_test

import random

from .models import *
from .forms import *

from django.db.models import Q
# 슈퍼유저인지 알아보기 위한 데코레이터

def first_page(request):
    pass
    return render(request, 'movies/first_page.html')

def index(request):
    movies = Movie.objects.all()
    # fr_movies = Movie.objects.all().exclude(poster_path__isnull=True).exclude(backdrop_path__isnull=True).order_by('-popularity')[:21]
    # en_movies = Movie.objects.all().exclude(poster_path__isnull=True).exclude(backdrop_path__isnull=True).order_by('-vote_average')[:21]
    fr_movies = Movie.objects.all().exclude(poster_path__isnull=True).exclude(backdrop_path__isnull=True).filter(popularity__gte=20).order_by('?')[:21]
    en_movies = Movie.objects.all().exclude(poster_path__isnull=True).exclude(backdrop_path__isnull=True).filter(vote_average__gte=8).order_by('?')[:21]
    lists = {fr_movies:'인기 많은 영화',  en_movies:'평점 높은 영화'}
    ### 유저가 투표한 장르의 영화들을 가져옴###
    user_movie = Movie.objects.all().filter(vote_user=request.user.id)
    # 영화들이 쿼리셋형태라 mv로 각각의 요소를 가져올 것임
    gen_list = {} # 나의 장르 리스트 // 평점을 표현한 영화의 장르들의 목록. 어떤 장르를 몇개 투표했는지 알기 위해
    for mv in user_movie:
        ge = mv.id # 해당 영화의 id를 ge라고 선언
        gen = Genre.objects.all().filter(movie_genre=ge) # 역참조로 해당 영화에 대한 장르정보를 장르 테이블에서 가져옴 (이름 알기 위해)
        for genr in gen: # 장르 요소가 쿼리셋이어서 genr로 선언
            genre = genr.id # 해당 장르의 id를 가져옴
            if genre in gen_list: # 평점을 남긴 영화의 장르가 나의 장르 리스트에 있는지 보고
                gen_list[genre] += 1 # 있으면 1 증가
            else:
                gen_list[genre] = 1 # 없으면 만들어 줌
           
    sorted(gen_list.items(), key=lambda x: x[1], reverse=True) # 갯수 상위 순으로 출력 위해서 정렬
    
    x = 0
    recommend_list = {}
    for key, value in gen_list.items(): # 딕셔너리 형태여서 
        if x == 3: # 상위 3개만 출력하기 위해
            break
        gen_rec_m = Movie.objects.all().exclude(poster_path__isnull=True, backdrop_path__isnull=True).filter(genres = key).order_by('?')[:21] # 장르기반 추천 영화 목록// 장르기준으로 랜덤 4개 출력
        keyname = Genre.objects.all().filter(id=key) # 장르 이름을 출력해야해서, 장르id를 key로 하고
        recommend_list[keyname] = gen_rec_m # 선별한 쿼리셋을 value로 한 딕셔너리 만듬
        x += 1
       
    context = {
        'movies' : movies,
        'fr_movies': fr_movies,
        'en_movies': en_movies,
        'user_movie' : user_movie,
        'gen_list': gen_list,
        'recommend_list' : recommend_list,
        'lists':lists
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = Rate.objects.all().filter(user_id=request.user.id, movie_id = movie.pk)
    form = RatingForm(request.POST)
    genres = Genre.objects.all().filter(movie_genre=movie_pk)
    user = request.user
    movie_names = Movie.objects.all().filter(vote_user=request.user.id)
    point = 0
    for score in rate:
        if request.user.id == score.user_id and movie_pk == score.movie_id:
            point = int(score.rank)

    total = (movie.vote_average) * (movie.vote_count)

    context = {
    'movie':movie,
    'genres':genres,
    'total':total,
    'rate' : rate,
    'form': form,
    'user' : user,
    'point' : point,
    'movie_names':movie_names,
    }
    return render(request, 'movies/detail.html', context)

### 영화 평점넣기 ###

def rank(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    rate = Rate.objects.all()
    User = get_user_model()
    total = (movie.vote_average) * (movie.vote_count)
    if request.user.is_authenticated:
        if request.user not in movie.vote_user.all():
            form = RatingForm(request.POST)
            if form.is_valid():
                rate = form.save(commit=False)
                rate.user = request.user
                rate.movie = movie
                rate.save()
                movie.vote_user.add(request.user)
        else:
            pass
    return redirect('movies:detail', movie.pk)

def rank_cancle(request, movie_pk):
    global point
    movie = get_object_or_404(Movie, pk = movie_pk)
    rate =  Rate.objects.all().filter(movie_id = movie_pk, user_id = request.user.id)
    rate.delete()
    movie.vote_user.remove(request.user)
    return redirect('movies:detail', movie.pk)


### 리뷰 관련 ###
@login_required
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:review_detail', review.movie.id, review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'movie':movie
    }
    return render(request, 'movies/review_form.html', context)


def review_detail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm()

    context = {
        'movie':movie,
        'review' : review,
        'form':form
    }
    return render(request, 'movies/review_detail.html', context)

@login_required
def review_update(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    # 글작성 유저랑 로그인 한 유저가 같을 때
    if request.user == review.user:
        # POST방식일 때
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.movie = movie
                review.save()
                # 글수정을 완료하고 review_detail페이지로 돌려줌
                return redirect('movies:review_detail', review.movie.id, review.pk)
        # GET방식일때
        else:
            form = ReviewForm(instance=review)
        context = {
            'form':form,
        }
        return render(request, 'movies/review_form.html', context)
    else:
        return redirect('movies:review_detail', review_pk, movie_pk)

@login_required
@require_POST
def review_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk )
    if request.user == review.user:
        review.delete()
    return redirect('movies:detail', movie.pk)

### Comment 관련 ###

@require_POST
def comment_create(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        review = get_object_or_404(Review, pk=review_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
    return redirect('movies:review_detail', movie.pk, review.pk)

@login_required
def comment_update(request, movie_pk, review_pk, comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    # 글작성 유저랑 로그인 한 유저가 같을 때
    if request.user == comment.user:
        # POST방식일 때
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.movie = movie
                comment.save()
                # 글수정을 완료하고 review_detail페이지로 돌려줌
                return redirect('movies:review_detail', review.movie.id, review.pk)
        # GET방식일때
        else:
            form = CommentForm(instance=comment)
        context = {
            'form':form,
        }
        return render(request, 'movies/review_form.html', context)
    else:
        return redirect('movies:review_detail', review_pk, movie_pk)

@login_required
@require_POST
def comment_delete(request, movie_pk, review_pk, comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()  
    return redirect('movies:review_detail', movie.pk, review.pk)

### 관리자 관련 (슈퍼유저인지 아닌지에 따른 영화 쓰기) ###
@user_passes_test(lambda u: u.is_superuser)
def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')

    else:
        form = MovieForm()

    context = {
        'form' : form
    }
    return render(request, 'movies/m_cre_upd.html', context)

@user_passes_test(lambda u : u.is_superuser)
@login_required
def movie_delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()

    return redirect('movies:index')

@user_passes_test(lambda u: u.is_superuser)
@login_required
def movie_update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:index', movie_pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'form': form
    }
    return render(request, 'movies/m_cre_upd.html', context)

