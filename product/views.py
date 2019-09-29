from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.views import View
from django.views.generic.base import TemplateView
from django.http import HttpResponse, Http404
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import json

class IndexView(View):
	def get(self, request):
		if request.user.is_authenticated:
			return redirect('product/product_list')

		return render(request,'registration/login.html')


@method_decorator(login_required, name='dispatch')
class ItemCountView(View):
	def get(self, request):
		item_count = Cart.objects.all().count()
		result = {"data": {'item_count':item_count}}
		return HttpResponse(json.dumps(result))


class ProductListView(View):
	template_name = 'product/product_listing.html'
	def get(self, request):
		products = ProductPage.objects.all()
		result = {'products':products}
		return render(request, self.template_name,result)


@method_decorator(login_required, name='dispatch')
class CheckoutCartView(View):
	template_name = 'product/checkout.html'
	def get(self, request):
		carts = Cart.objects.all()
		total = sum([cart.product_id.price*cart.quantity for cart in carts ])
		result = {"total":total}
		return render(request, self.template_name,result)


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
	def post(self, request):
		product_id = request.POST['product_id']
		user = request.user
		user_id = user.id

		product = ProductPage.objects.filter(product_id=product_id)
		product = product[0]
		if not product:	
			response = {'success':False,'message':"product_id not present"}
			return HttpResponse(json.dumps({"data":response}),status=404)

		cart = Cart.objects.filter(user_id=user_id, product_id=product_id)
		if cart:
			cart = cart[0]
			cart.quantity+=1
		else:
			cart = Cart(
				user_id= user,
				product_id=product,
			)

		try:
			cart.save()
		except Exception as e:
			response = {"success":False, "message": str(e)}
			result = {"data":response}
			return HttpResponse(json.dumps(result))

		item_count = Cart.objects.all().count()

		response = {"success": True, "message": "successfully added to cart","item_count":item_count}
		result = {"data":response}
		return HttpResponse(json.dumps(result))


@method_decorator(login_required, name='dispatch')
class CartDetailsView(View):
	template_name = 'product/shopping_cart.html'
	def get(self, request):
		carts = Cart.objects.all()
		total = sum([cart.product_id.price*cart.quantity for cart in carts ])
		result = {'carts' : carts, 'total':total}
		return render(request, self.template_name,result)


@method_decorator(login_required, name='dispatch')
class RemoveFromCart(View):
	def post(self, request):
		cart_id = request.POST['cart_id']
		user = request.user
		user_id = user.id
		try:
			cart = get_object_or_404(Cart, cart_id = cart_id)
		except Http404:
			response = {'success':False,'message':"Cart_id not present"}
			return HttpResponse(response,status=404)

		cart.delete()
		response = {"success": True, "message": "successfully added to cart"}
		result = {"data":response}
		return HttpResponse(json.dumps(result))

@method_decorator(login_required, name='dispatch')
class UpdateCartView(View):
	def post(self, request):
		cart_id = request.POST['cart_id']
		quantity = request.POST['quantity']
		try:
			quantity = int(quantity)

		except:
			response = {'success':False,'message':"Quantity should be Integer"}
			return HttpResponse(response,status=400)


		cart = Cart.objects.filter(cart_id=cart_id)
		if not cart:			
			response = {'success':False,'message':"Cart_id not present"}
			return HttpResponse(response,status=404)

		cart.update(quantity=quantity)

		response = {"success": True, "message": "successfully added to cart"}
		result = {"data":response}
		return HttpResponse(json.dumps(result))
