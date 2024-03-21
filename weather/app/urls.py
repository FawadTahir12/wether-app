from django.urls import path, include
from .views import search, favoriteCities
urlpatterns = [
    path("search/", search),
    path('favorites/', favoriteCities, name='favorite-cities'),
    
]