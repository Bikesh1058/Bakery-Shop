from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, null=True)
    price = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    image = models.ImageField(null=True, upload_to="images/")
    short_description = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", null=True
    )
    
    def __str__(self):
        return self.name

class images(models.Model):
    image=models.ImageField(null=True,upload_to="images/")
    

class Carousel(models.Model):
    id=models.IntegerField(primary_key=True, null=False)
    title=models.CharField(max_length=250, null=True)
    description=models.CharField(null=True, max_length=5000)
    image=models.ImageField(null=True,upload_to="images/")
    
    def __str__(self):
        return self.title
    
    


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
        
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.price for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

    def __str__(self):
        return str(self.id)
     
    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to="orderitem_images/")  # Added image field

    def save(self, *args, **kwargs):
        # Automatically assign the product's image to the OrderItem image field
        if self.product and not self.image:
            self.image = self.product.image
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=255,null=True)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name} ({self.email})'
