from django.db import models

class FavoriteCity(models.Model):
    city_name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.city_name
