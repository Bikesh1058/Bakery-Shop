from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.core.files.storage import FileSystemStorage
from .models import Product,images, Carousel,Category,Order,OrderItem,ContactMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from .form import ContactForm

from .models import *

def checkout(request):
    if request.method == 'POST':
        # Retrieve the current user's active order
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()

        if order:
            # Mark the order as complete
            order.complete = True
            order.save()

            # Clear the cart by deleting all order items related to this order
            OrderItem.objects.filter(order=order).delete()

            # Display a success message
            messages.success(request, f"Checkout successful! Total paid: Rs. {order.get_cart_total}")

            # Redirect to the success page after completing the checkout
            return redirect('success')  # Redirect to the success page
        else:
            messages.error(request, "No active cart found!")
            return redirect('cart')  # Redirect back to the cart if no order exists
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        
        total = order.get_cart_total
        tax = 0.13 * total
        total_price = total + tax

    else:
        total = 0
        items = []
        tax = 0
        total_price = 0
    context = {
        'total': total,
    }
    print(total_price)
    return render(request, 'checkout.html', context)

    return render(request, 'checkout.html')

def transaction_successful(request):
    # Render the success page template where animation and redirection happens
    return render(request, 'success.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the contact message to the database
            return redirect('thank_you')  # Redirect to a thank you page after submission
    else:
        form = ContactForm()

    return render(request, 'contactus.html', {'form': form})

def product_list(request):
    # Fetch all categories along with their related products
    categories = Category.objects.prefetch_related('products').all()
    
    return render(request, 'your_template.html', {'categories': categories})


def homepage(request):
    result=images.objects.all()
    print((result.values()))
    return render(request, 'homepage.html',{'image':result})

def home(request):
    result=Product.objects.all()[:6]
    carousels = Carousel.objects.all()
    order_items = OrderItem.objects.count()
    
    context = {'Products':result, 'carousels': carousels, 'count': order_items}
    return render(request, 'home.html', context=context)

def store(request):
    order_items = OrderItem.objects.count()
    context = {'count': order_items, 'products':{}}

    categories=Category.objects.all()

    for cat in categories:
        context['products'][cat.name] = Product.objects.filter(category=cat.id)

    print(context)
    return render(request, 'store.html', context=context)

def product(request, id):
    # pdt = Product.objects.filter(id=id)
    pdt = get_object_or_404(Product, id=id)
    order_items = OrderItem.objects.count()
    
    return render(request, 'productdetails.html', {"product": pdt, 'count': order_items})


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        
        total = order.get_cart_total
        tax = 0.13 * total
        total_price = total + tax

    else:
        total = 0
        items = []
        tax = 0
        total_price = 0
    request.session['total_price'] = total_price
    context = {'items':items, 'total': total, 'tax': tax, 'total_price': total_price, 'count': len(items)}
    return render(request, 'cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    print(orderItem.quantity)
        

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def cart_view(request):
    # Get cart data from session
    cart = request.session.get('cart', {})  # Retrieve cart from session, default to empty dict

    # Calculate total price and prepare cart items
    order_items = []
    total_price = 0
    for product_id, details in cart.items():
        product = Product.objects.get(id=product_id)  # Get the product by ID
        quantity = details.get('quantity', 1)  # Default to 1 if quantity is not set
        item_total = quantity * product.price
        order_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total,
        })
        total_price += item_total

    # Save total price to session for use in checkout
    request.session['total_price'] = total_price

    context = {
        'order_items': order_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

 