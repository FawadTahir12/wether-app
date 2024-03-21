from django.urls import path
from app import consumer
websocket_urlpatterns = [
    path('ws/search/', consumer.WeatherConsumer.as_asgi()),
    path('ws/favorite/', consumer.FavoriteCityConsumer.as_asgi()),
]