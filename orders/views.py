from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . cart import Cart
from home.models import Product
from . forms import CartAddForm,CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Order,OrderItem,Coupon
from django.contrib import messages
import requests
from django.http import HttpResponse
import requests
import json
import datetime
from django.contrib import messages
from django.core.exceptions import PermissionDenied

class CartView(View):
    def get(self,request):
        cart=Cart(request)
        return render(request, 'orders/cart.html', {'cart':cart})


class CartAddView(View):
    def post(self,request,product_id):
        cart=Cart(request)
        product=get_object_or_404(Product,id=product_id)
        form=CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product,form.cleaned_data['quantity'])
        return redirect('orders:cart')
    
    
class CartDeleteView(View):
    def get(self,request,product_id):
        cart=Cart(request)
        product=get_object_or_404(Product,id=product_id)
        cart.delete(product)
        return redirect('orders:cart')
    
    
    
    
class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')
    
class CartIncreaseView(View):
    def get(self,request,product_id):
        cart=Cart(request)
        product=get_object_or_404(Product,id=product_id)
        cart.increase(product)
        return redirect('orders:cart')
    

class OrderDetailView(LoginRequiredMixin, View):
	form_class = CouponApplyForm

	def get(self, request, order_id):
		order = get_object_or_404(Order, id=order_id)
		return render(request, 'orders/payment.html', {'order':order,'form':self.form_class})




class OrderCreateView(LoginRequiredMixin, View):
	def get(self, request):
		cart = Cart(request)
		order = Order.objects.create(user=request.user)
		for item in cart:
			OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
		cart.get_total_price()
		return redirect('orders:order_detail', order.id)


MERCHANT = '****'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'




class OrderPayView(LoginRequiredMixin, View):
	def get(self, request, order_id):
		cart=Cart(request)
		order = get_object_or_404(Order, id=order_id, user=request.user)
		cart.clear()
		cart.save()
		return render(request,'orders/order.html', {"order": order})


		# order = Order.objects.get(id=order_id)
		# request.session[''] = {
		# 	'order_id': order.id,
		# }
		# req_data = {
		# 	"merchant_id": MERCHANT,
		# 	"amount": order.get_total_price(),
		# 	"callback_url": CallbackURL,
		# 	"description": description,
		# 	"metadata": {"mobile": request.user.phone_number, "email": request.user.email}
		# }
		# req_header = {"accept": "application/json",
		# 			  "content-type": "application/json'"}
		# req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
		# 	req_data), headers=req_header)
		# authority = req.json()['data']['authority']
		# if len(req.json()['errors']) == 0:
		# 	return redirect(ZP_API_STARTPAY.format(authority=authority))
		# else:
		# 	e_code = req.json()['errors']['code']
		# 	e_message = req.json()['errors']['message']
		# 	return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class OrderVerifyView(LoginRequiredMixin, View):
    pass
# 	def get(self, request):
# 		order_id = request.session['order_pay']['order_id']
# 		order = Order.objects.get(id=int(order_id))
# 		t_status = request.GET.get('Status')
# 		t_authority = request.GET['Authority']
# 		if request.GET.get('Status') == 'OK':
# 			req_header = {"accept": "application/json",
# 						  "content-type": "application/json'"}
# 			req_data = {
# 				"merchant_id": MERCHANT,
# 				"amount": order.get_total_price(),
# 				"authority": t_authority
# 			}
# 			req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
# 			if len(req.json()['errors']) == 0:
# 				t_status = req.json()['data']['code']
# 				if t_status == 100:
# 					order.paid = True
# 					order.save()
# 					return HttpResponse('Transaction success.\nRefID: ' + str(
# 						req.json()['data']['ref_id']
# 					))
# 				elif t_status == 101:
# 					return HttpResponse('Transaction submitted : ' + str(
# 						req.json()['data']['message']
# 					))
# 				else:
# 					return HttpResponse('Transaction failed.\nStatus: ' + str(
# 						req.json()['data']['message']
# 					))
# 			else:
# 				e_code = req.json()['errors']['code']
# 				e_message = req.json()['errors']['message']
# 				return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
# 		else:
# 			return HttpResponse('Transaction failed or canceled by user')





class CouponApplyView(View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)

        if not form.is_valid():
            messages.error(request, "لطفاً کد تخفیف را درست وارد کنید.", "danger")
            return redirect('orders:order_detail', order_id)

        code = form.cleaned_data['code']
        
        try:
            coupon = Coupon.objects.get(code=code, valid_from__lte=now, valid_to__gte=now, active=True)
            order = get_object_or_404(Order, id=order_id, user=request.user)

            order.discount = coupon.discount if coupon.discount else 0
            order.save()

            messages.success(request, f'کد تخفیف {coupon.discount}% با موفقیت اعمال شد!', 'success')
        except Coupon.DoesNotExist:
            messages.error(request, "این کد تخفیف معتبر نیست!", "danger")

        return redirect('orders:order_detail', order_id)




