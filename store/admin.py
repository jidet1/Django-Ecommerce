from django.contrib import admin
from . models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)



#Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

#Extend User model
class UserAdmin(admin.ModelAdmin):
   model = User
   fields = ['password', 'last_login', 'username', 'first_name', 'last_name', 'email']
   inlines = [ProfileInline]

#Unregister the default User model
admin.site.unregister(User)
#Register the new User model
admin.site.register(User, UserAdmin)
