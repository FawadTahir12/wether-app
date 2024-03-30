import json
from channels.generic.websocket import AsyncWebsocketConsumer
import requests
import asyncio
import os
from .models import FavoriteCity
from channels.db import database_sync_to_async

from dotenv import load_dotenv
load_dotenv()
class WeatherConsumer(AsyncWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weather_update_tasks = {}
        
    async def connect(self):
        await self.accept()
        default_city = 'Islamabad'
        await self.send_weather_updates(default_city)
        self.weather_update_task = asyncio.create_task(self.periodic_weather_updates(default_city))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        if hasattr(self, 'weather_update_task'):
            self.weather_update_task.cancel()
        
        city = json.loads(text_data).get('city').capitalize()
        
        await self.send_weather_updates(city)
 
        self.weather_update_task = asyncio.create_task(self.periodic_weather_updates(city))

    async def send_weather_updates(self, city):
        weather_data = await self.get_weather_data(city)
        await self.send(text_data=json.dumps(weather_data))

    async def get_weather_data(self, city):
        api_key = os.environ['API_KEY']
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                'city': city,
                'temperature': data['current']['temp_c'],
                'condition': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'humidity': data['current']['humidity'],
                'localtime': data['location']['localtime']
            }
            return weather_info
        else:
            return {'error': 'Unable to fetch weather data'}

    async def periodic_weather_updates(self, city):
        while True:
            await asyncio.sleep(60)  # Wait for 60 seconds
            await self.send_weather_updates(city)
            
            


class FavoriteCityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'add_favorite':
            city_name = data.get('city')
            await self.add_favorite(city_name)
            await self.send(text_data=json.dumps({'status': 'success', 'message': f'{city_name} added to favorites.'}))
        elif action == 'delete_favorite':
            city_name = data.get('city')
            response  = await self.delete_favorite(city_name)
            await self.send(text_data=json.dumps({'status': response.get('status'), 'message': response.get('message')}))
        elif action == 'get_favorite_cities':
            favorite_cities = await self.send_favorite_cities()
            await self.send(text_data=json.dumps({'action': 'Favorite Cities', 'favorite_cities': list(favorite_cities)}))
    
    # @database_sync_to_async
    # def add_favorite(self, city_name):
    #     try:
    #         favorite_city = FavoriteCity.objects.create(city_name=city_name)
    #     except Exception as e:
    #         self.send(text_data=json.dumps({'status': 'error', 'message': str(e)}))
    
    
    async def add_favorite(self, city_name):
        try:          
            await FavoriteCity.objects.acreate(city_name=city_name)
        except Exception as e:
            self.send(text_data=json.dumps({'status': 'error', 'message': str(e)}))
    
    # @database_sync_to_async
    # def delete_favorite(self, city_name):
    #     try:
    #         FavoriteCity.objects.filter(city_name=city_name).delete()
    #         return {'status': 'success', 'message': f'{city_name} removed from favorites.'}
    #     except Exception as e:
    #         return {'status': 'error', 'message': str(e)}
        

    async def delete_favorite(self, city_name):
        try:
            print('in delee')
            await FavoriteCity.objects.filter(city_name=city_name).adelete()
            return {'status': 'success', 'message': f'{city_name} removed from favorites.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    
    @database_sync_to_async      
    def send_favorite_cities(self):
        return list(FavoriteCity.objects.all().values_list('city_name', flat=True))
        
   