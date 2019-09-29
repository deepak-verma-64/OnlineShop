from django.contrib import admin
from django.urls import path, include
from product import views
urlpatterns = [
    path('add_to_cart', views.AddToCartView.as_view(), name = 'add_to_cart'),
    path('product_list/', views.ProductListView.as_view(), name="product_list"),
    path('cart/', views.CartDetailsView.as_view(), name="shopping_cart"),
    path('remove_from_cart', views.RemoveFromCart.as_view(), name = 'remove_from_cart'),
    path('update_cart', views.UpdateCartView.as_view(), name = 'update_cart'),
    path('item_count', views.ItemCountView.as_view(), name = 'item_count'),
    path('checkout', views.CheckoutCartView.as_view(), name = 'checkout_cart'),

]
