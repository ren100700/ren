from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart



# Create your views here.
from orders.models import OrderInfo, OrderGoods
from utils.functions import get_order_sn


def order(request):
	if request.method=='GET':
		# 获取当前登录系统的user_id
		user_id = request.session['user_id']
		# 获取当前勾选的商品用于下单
		cart_goods = ShoppingCart.objects.filter(user_id=user_id,is_select=True)
		# 在购物车对象上绑定一个total_price字段，用于计算价格
		for cart in cart_goods:
			cart.total_price = cart.nums*cart.goods.shop_price
		return render(request,'place_order.html',{'cart_goods':cart_goods})

	if request.method == 'POST':
		"""
		接收ajax请求，创建订单
		"""
		# 1. 选择购物车中is_select为True的商品
		# 2. 创建订单
		# 3. 创建订单和商品之间的关联关系表，order_goods表
		# 4. 删除购物车中已下单的商品
		user_id = request.session['user_id']
		# 获取购物车中当前登录用户勾选的商品
		carts = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
		# 订单货号
		order_sn = get_order_sn()
		# 订单金额
		order_mount = 0
		for cart in carts:
			order_mount += cart.nums * cart.goods.shop_price
		# 创建订单
		order = OrderInfo.objects.create(user_id=user_id,
										 order_sn=order_sn,
										 order_mount=order_mount)
		for cart in carts:
			# 创建订单和商品的详情表
			OrderGoods.objects.create(order_id=order.id,
									  goods_id=cart.goods_id,
									  goods_nums=cart.nums)
		carts.delete()
		# 删除session中的商品信息
		request.session.pop('goods')
		return JsonResponse({'code': 200, 'msg': '请求成功'})


def user_center_site(request):
	if request.method=='GET':
		return render(request,'user_center_site.html')