from django.db import models
from django.conf import settings
import os  , datetime
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits = 10 , decimal_places = 2)
    category = models.ForeignKey(Category , on_delete = models.CASCADE)
    
    
    @property 
    def is_active(self):
        return self.quantity > 0
    

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_image/')
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    
    def delete(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
        if os.path.isfile(file_path):
            os.remove(file_path)
        super(ProductImage, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Product picture"
        verbose_name_plural = "Product pictures"
        
    def __str__(self):
        return self.product.title
        

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(blank = True , null = True)
    is_active = models.BooleanField(default = True)
    
    @property
    def quantity(self):
        quantity = 0 
        products = CartProduct.objects.filter(product_id = self.id)
        for i in products:
            quantity += i.quantity
        return quantity
    
        
    @property
    def total_price(self):
        result = 0
        for i in CartProduct.objects.filter(card_id=self.id):
            result +=(i.product.price)*i.quantity
        return result
    
    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now()
        super(Cart, self).save(*args, **kwargs)
    

class CartProduct(models.Model):
    card = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    @property
    def total_price(self):
        result = self.product.price * self.quantity
        return result


class Order(models.Model):
    product = models.ForeignKey(Product , on_delete = models.SET_NULL , null = True)
    date = models.DateTimeField(blank = True , null = True)
    status = models.SmallIntegerField(
        choices=(
            (1,'being delivered'), 
            (2, 'delivered'),
            (3, 'cancallation')
            )
    )     

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now()
        super(Order, self).save(*args, **kwargs)
        