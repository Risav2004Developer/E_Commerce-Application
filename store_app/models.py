
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Categories(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Brand(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Color(models.Model):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION=(('New','New'), ('Old','Old'))
    STOCK=(('In Stock','In Stock'),('Out of Stock','Out Of Stock'))
    STATUS=(('Publish','Publish'),('Draft','Draft'))
    unique_id=models.CharField(unique=True,blank=True,null=False,max_length=200)
    image=models.ImageField(upload_to='Product_images/img')
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    condition=models.CharField(choices=CONDITION,max_length=100)
    information=models.TextField()
    description=models.TextField()
    stock=models.CharField(choices=STOCK,max_length=100)
    status=models.CharField(choices=STATUS,max_length=100)
    created_date=models.DateTimeField(default=timezone.now)
    Categories=models.ForeignKey(Categories,on_delete=models.CASCADE)
    Brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    Color=models.ForeignKey(Color,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id=self.created_date.strftime('75%Y%m%d23') + str(self.id)
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class Images(models.Model):
    image=models.ImageField(upload_to='Product_images/img')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class Tag(models.Model):
    name=models.CharField(max_length=200)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    postcode=models.IntegerField()
    phone=models.IntegerField()
    email=models.EmailField(max_length=100)
    additional_info=models.TextField()
    amount=models.CharField(max_length=100)
    paid=models.BooleanField(default=False,null=True)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
      return self.user.username

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.CharField(max_length=100)
    image=models.ImageField(upload_to="Product_Images/Order_Img")
    quantity=models.CharField(max_length=20)
    price=models.CharField(max_length=50)
    total=models.CharField(max_length=1000)

    def __str__(self):
        return self.order.user.username

class Banner(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to='Product_images/img')

    def __str__(self):
        return self.name