from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
	brand_id = models.AutoField(primary_key=True)
	brand_name = models.CharField(max_length=60)

	def __str__(self):
		return self.brand_name

class Category(models.Model):
	category_id = models.AutoField(primary_key=True)
	category_name = models.CharField(max_length=60)

	def __str__(self):
		return self.category_name

class Subcategory(models.Model):
	category_id = models.ForeignKey(Category,on_delete=models.PROTECT)
	subcategory_id = models.AutoField(primary_key=True)
	subcategory_name = models.CharField(max_length=60)

	def __str__(self):
		return self.subcategory_name

class ProductPage(models.Model):
	product_id = models.AutoField(primary_key=True)
	product_name = models.CharField(max_length= 60)
	short_desc = models.CharField(max_length=100)
	description = models.CharField(max_length = 500)
	brand = models.ForeignKey(Brand,on_delete=models.PROTECT)
	pub_date = models.DateField()
	category = models.ForeignKey(Category,on_delete=models.PROTECT)
	subcategory = models.ForeignKey(Subcategory,on_delete=models.PROTECT)
	mrp = models.IntegerField()
	price = models.IntegerField()
	image_url = models.CharField(max_length=400)
	product_url = models.CharField(max_length =400)
	color = models.CharField(max_length=20)
	Status = models.CharField(max_length=20)

	def __str__(self):
		return self.product_name


class Cart(models.Model):
	cart_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User,  on_delete=models.PROTECT)
	product_id = models.ForeignKey(ProductPage, on_delete=models.PROTECT)
	quantity = models.IntegerField(default=1)


	def remove(self, product, cart):
		print (product)
		product_id = str(product.product_id)
		print (product_id, cart)
		if product_id in cart:
			# Subtract 1 from the quantity
			cart[product_id]['quantity'] -= 1
			# If the quantity is now 0, then delete the item
			if cart[product_id]['quantity'] == 0:
				del cart[product_id]
			self.save()

