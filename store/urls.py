from django.urls import path
from .views import CartDetail, Checkout, ProductListView, ProductDetailView

app_name = "store"

urlpatterns = [
    path("products", ProductListView.as_view(), name="product_list"),
    path("products/<slug:slug>", ProductDetailView.as_view(), name="product_detail"),
    path("cart", CartDetail.as_view(), name="cart_detail"),
    path("checkout", Checkout.as_view(), name="checkout"),
]