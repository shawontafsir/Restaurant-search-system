from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=20)
    costperfood = models.CharField(max_length=15)
    time = models.CharField(max_length=20)

    def __str__(self):
        return self.name+' - '+self.address

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    review = models.CharField(max_length=200)
    rating = models.CharField(max_length=2)

    def __str__(self):
        return self.username+' - '+self.review+' - '+self.rating

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    foodname = models.CharField(max_length=20)
    price = models.CharField(max_length=4)
    review = models.CharField(max_length=200)
    rating = models.CharField(max_length=2)

    def __str__(self):
        return self.foodname+' - '+self.price+' - '+self.rating

class Deal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    deal = models.CharField(max_length=300)

    def __str__(self):
        return self.deal