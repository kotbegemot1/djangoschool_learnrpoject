from typing import ClassVar
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Category, Movie, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm

# Create your views here.

class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").distinct()


class MoviesView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 2


class MovieDetailViews(GenreYear, DetailView):
    model = Movie
    slug_field = 'url'
    
    def get_object(self):
        self.obj = super().get_object()
        return self.obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        try:
            context["obj"] = str(self.obj.ratings.first().star_id)
        except AttributeError:
            context["obj"] = "0"

 
        # context["form"] = ReviewForm()
        return context


class AddRewiew(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST, request.FILES)
        movie = Movie.objects.get(id=pk)
        print()
        print(form.errors)
        print()
        if form.is_valid():

            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie 
            form.save()
        return redirect(movie)

class ActorView(DetailView):
    model = Actor
    template_name = "movies/actor.html"
    slug_field = "name"

class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 2

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        # print()
        # print(queryset)
        # print()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        # print(context["year"])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context

class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 2

    def get_queryset(self):
        # print(Movie.objects.filter(title__contains=self.request.GET.get("q")))
        return Movie.objects.filter(title__contains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context