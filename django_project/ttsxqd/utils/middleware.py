import re

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

from users.models import User
from cart.models import ShoppingCart


class UserAuthMiddleware(MiddlewareMixin):

	def process_request(self,request):
		not_need_check=['/home/index/','/users/login/','/users/register/',
						'/cart/cart/','/cart/f_price/','/cart/add_cart/',
						'/media/(.*)','/static/(.*)','/goods/goods_detail/(\d+)/']
		path = request.path
		for not_path in not_need_check:
			# 匹配当前地址是不是不需要登录验证
			if re.match(not_path,path):
				return None

		# 登录验证开始
		user_id= request.session.get('user_id')
		# 没有登录获取不到user_id参数
		if not user_id:
			return HttpResponseRedirect(reverse('users:login'))
		# 给request.user赋值，赋值为当前登录系统的用户
		user=User.objects.get(pk=user_id)
		request.user = user

		return None


class UserSessionMiddleware(MiddlewareMixin):
	# 同步session数据到shopping_cart表中

	def process_request(self,request):
		# 判断用户是否登录
		user_id = request.session.get('user_id')
		if user_id:
			# 同步,获取session中的数据
			session_goods = request.session.get('goods')
			if session_goods:
				#1.如果购物车中没有session中没有商品数据则创建
				# 2.如果购物车中有session中商品数据则更新
				# session中结构[[id,num,is_select]]
				# goods_ids = [goods[0]for goods in session_goods]
				for goods in session_goods:
					cart = ShoppingCart.objects.filter(goods_id=goods[0],
												user_id=user_id).first()
					if cart:
						# 如果购物车中存在session数据，则修改数据
						if cart.nums != goods[1]:
							# 如果商品数量不相同时，则同步商品数量
							cart.nums = goods[1]
						# 同步商品选择状态
						cart.is_select = int(goods[2])
						cart.save()
					else:
						# session中商品数据不存在于购物车中，则保存
						ShoppingCart.objects.create(user_id=user_id,
													goods_id=goods[0],
													nums=goods[1],
													is_select=goods[2])
				return None