from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=300)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    
class Product(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=250)
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, related_name="product_id", blank=True)

