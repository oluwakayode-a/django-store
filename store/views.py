from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponseRedirect, JsonResponse

from .models import Order, Product
from .cart import Cart

# Create your views here.
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = "product_list.html"


class ProductDetailView(DetailView):
    model = Product
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'
    template_name = "product_detail.html"


class CartDetail(View):
    def get(self, request, *args, **kwargs):
        self.cart = Cart(request)
        return render(request, "cart.html", {"cart" : self.cart})


class Checkout(View):
    def get(self, request, *args, **kwargs):
        self.cart = Cart(request)
        return render(request, "checkout.html", {"price" : self.cart.get_total_price})
    
    def post(self, request, *args, **kwargs):
        if request.method.is_ajax:
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')

            order = Order.objects.create(
                name=name,
                email=email
            )
            
            if request.user.is_authenticated():
                order.user = request.user
            order.save()
        
        return JsonResponse({"message" : "successful"})


        
