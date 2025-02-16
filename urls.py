from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("main", views.homepage, name="main"),
    path("store", views.store, name="store"),
    path("product/<int:id>", views.product, name="product"),
    path("cart", views.cart, name="cart"),
    path("aboutus", views.aboutus, name='aboutus'),
    path("contactus", views.contactus, name='contactus'),
    path('checkout', views.checkout, name='checkout'),
    path('success', views.transaction_successful, name='success'),
    path('update-item/', views.updateItem, name='update_item'),
    ]