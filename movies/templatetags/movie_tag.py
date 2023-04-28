from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count=5):
    movies = Movie.objects.order_by("id")[:count]
    return {'last_movies': movies}


@register.filter
def age(value):
    if str(value)[-1] == '1':
        age_end = "год"
    elif int(str(value)[-1]) in (2, 3, 4):
        age_end = "года"
    else:
        age_end = "лет"
    return "{} {}".format(value, age_end)
    
