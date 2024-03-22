# Real Time Weather App Using Websockets


## Project Overview

This project is related to weather app in which I use Django channels for websocket to unable real time updation of weather. User can search fro weather of different cities and add favorite cities weather information.

## Steps
1. First I start  Django project and create an app name 'app'
2. As django channels is asynchronus so I have to install Daphne
3. Configure My django application with Daphne
4. Then I create Consumer for websocket which takes city from request and pass to the third party api weatherapi.com and send the response back to the client.
5. Configure routing for websockets.
6. I use Asyncio module to create asynchronous task. After getting data from API the server hit the api after I minute and the send the response to client which enable that the data will be updated after every minute
7. There are two pages one is for search where user search for particular city and one is for favorite cities so the user see direct weather data without search.
8. Favorite cities module is not completed yet because of the time but backend logic is completed.
9. I use postgresql to save the favorite cities. That is why I create Favorite cities model in models.py
10. Dockerize the whole application by writing dockerfile and docker-compose.yml in which I handle django applicaton, database as well as redis.



## Technologies

1. Django
2. Django Channels
3. https://www.weatherapi.com/ Api for getting Data
4. JavaScript
5. Html, Css
6. Postgrsql




