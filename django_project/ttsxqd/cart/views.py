from django.http import JsonResponse
from django.shortcuts import render

from goods.models import Goods
from cart.models import ShoppingCart

def add_cart(request):
	if request.method=='POST':
		# 添加到session中的数据格式为：
		# key==>goods,
		# value==>[[id1,num],[id2,num],]
		# 1.1添加到购物车的数据就是添加到session中
		# 1.2如果商品已经添加到session中，则为修改session中的数据
		# 1.3如果商品没有添加到session中，则添加
		# 获取从ajax中传递的数据
		goods_id=request.POST.get('goods_id')
		goods_num=request.POST.get('goods_num')
		goods_list=[goods_id,goods_num,1]
		if request.session.get('goods'):
			flag=0
			# 购物车中已经有商品信息
			session_goods=request.session['goods']
			for goods in session_goods:
				if goods_id == goods[0]:
					goods[1] = int(goods[1]) + int(goods_num)
					flag=1
			if not flag:
				session_goods.append(goods_list)
			request.session['goods']=session_goods
			cart_count = len(session_goods)
		else:
			data=[]
			data.append(goods_list)
			request.session['goods']=data
			cart_count=1

		return JsonResponse({'code':200,'cart_count':cart_count})


def cart(request):
    if request.method == 'GET':
        # 需要判断用户是否登录， session['user_id']
        # 1. 如果登录，则购物车中展示当前登录用户的购物车表中的数据
        # 2. 如果没有登录，则购物车页面中展示session中的数据
        user_id = request.session.get('user_id')
        if user_id:
            # 登录系统用户, 获取购物车中的商品信息
            shop_cart = ShoppingCart.objects.filter(user_id=user_id)
            goods_all = [(cart.goods, cart.is_select, cart.nums) for cart in shop_cart]

            return render(request, 'cart.html', {'goods_all': goods_all})
        else:
            # 没有登录
            session_goods = request.session.get('goods')
            # 拿到session中所有的商品id值
            if session_goods:
                goods_all = [(Goods.objects.get(pk=good[0]), good[2], good[1])
                             for good in session_goods]
            else:
                goods_all = ''
            return render(request, 'cart.html', {'goods_all': goods_all})


def f_price(request):
	"""
	返回购物车或session中商品的价格，和总价
	{key:[[id1, price1],[id2, price2]], key2: total_price}
	"""
	user_id = request.session.get('user_id')
	if user_id:
		carts=ShoppingCart.objects.filter(user_id=user_id)
		cart_data={}
		cart_data['goods_price']=[(cart.goods_id,cart.nums*cart.goods.shop_price)
								  for cart in carts]
		all_price=0
		for cart in carts:
			if cart.is_select:
				all_price+=cart.nums*cart.goods.shop_price
		cart_data['all_price']=all_price
	else:
		# 拿到session中所有的商品信息
		session_goods = request.session.get('goods')
		cart_data = {}
		data_all = []
		all_price = 0
		for goods in session_goods:
			data = []
			data.append(goods[0])
			g = Goods.objects.get(pk=goods[0])
			data.append(int(goods[1]) * g.shop_price)
			data_all.append(data)
			if goods[2]:
				all_price += int(goods[1]) * g.shop_price
		cart_data['goods_price'] = data_all
		cart_data['all_price'] = all_price
	return JsonResponse({'code': 200, 'cart_data': cart_data})