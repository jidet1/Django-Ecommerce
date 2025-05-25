from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save #to create a user profile

#Create customer profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField( max_length=20, default='', blank=True)
    address1 = models.CharField(max_length=100, default='', blank=True)
    address2 = models.CharField(max_length=100, default='', blank=True)
    city = models.CharField(max_length=50, default='', blank=True)
    state = models.CharField(max_length=50, default='', blank=True)
    country = models.CharField(max_length=50, default='', blank=True)
    zip_code = models.CharField(max_length=20, default='', blank=True)
    old_cart = models.CharField(default='', blank=True, null=True)

    def __str__(self):
        return self.user.username #to put the username in the admin panel

#Create a user profile when a new user is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance) 
        user_profile.save()

#Automatically create a user profile when a new user is created
post_save.connect(create_user_profile, sender=User)

#Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"

#Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    password = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
#All of our Products
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0.0, max_digits=6, decimal_places=2)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='uploads/products')

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0.0, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

#Customer Order
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
