from django.urls import path

from .views import ActorView, AddRewiew, MovieDetailViews, MoviesView, FilterMoviesView, AddStarRating, \
                Search

urlpatterns = [
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path('search/', Search.as_view(), name='search'),
    path('add_rating/', AddStarRating.as_view(), name='add_rating'),
    path('review/<int:pk>/', AddRewiew.as_view(), name='add_review'),
    path('<slug:slug>/', MovieDetailViews.as_view(), name='movie_detail'),
    path('', MoviesView.as_view(), name='index'),
    path('actor/<str:slug>', ActorView.as_view(), name="actor_detail"),
    
]