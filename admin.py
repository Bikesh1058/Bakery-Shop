from django.contrib import admin
from .models import Product,images, Carousel, OrderItem, Order, Customer,Category,ContactMessage

admin.site.register(Product)
admin.site.register(images)
admin.site.register(Carousel)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(ContactMessage)