from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product

class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            # save an empty cart in the session
            cart = self.session["cart"] = {}
        self.cart = cart
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            yield product
        
    def add(self, product, quantity=1, action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id = product.id
        newItem = True
        if str(product.id) not in self.cart.keys():

            self.cart[product.id] = {
                    'id': product.id,
                    'name' : product.name,
                    'quantity': 1,
                    'slug': product.slug,
                    'price': str(product.price),
                    'image' : product.image.url,
            }
        else:
            newItem = True

            for key, value in self.cart.items():
                if key == str(product.id):

                    # value['quantity'] = value['quantity'] + 1
                    newItem = False
                    self.save()
                    break
            if newItem == True:

                self.cart[product.id] = {
                    'id': product.id,
                    'name' : product.name,
                    'quantity': 1,
                    'slug': product.slug,
                    'price': str(product.price),
                    'image' : product.image.url,
                }

        self.save()

    @property
    def get_total_price(self):
        return str(sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()))
    
    def is_empty(self):
        return True if len(self.cart) == 0 else False

    def save(self):
        # update the session cart
        self.session["cart"] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):

                value['quantity'] = value['quantity'] - 1
                if(value['quantity'] < 1):
                    return redirect('store:cart_detail')
                self.save()
                break
            else:
                print("Something Wrong")

    def clear(self):
        # empty cart
        self.session["cart"] = {}
        self.session.modified = True