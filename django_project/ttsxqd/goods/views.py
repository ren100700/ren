from django.shortcuts import render

# Create your views here.
from goods.models import Goods, GoodsCategory


def goods_detail(request,id):
	if request.method=='GET':
		goods=Goods.objects.filter(pk=id).first()
		return render(request,'detail.html',{'goods':goods})


def goods_list(request):
	if request.method=='GET':
		category_types=GoodsCategory.CATEGORY_TYPE
		goods=Goods.objects.all().order_by('-id')
		data_all={}
		for type in category_types:
			data = []
			for good in goods:
				if type[0] == good.category.category_type:
					data.append(good)
			data_all['goods_'+str(type[0])]=data

		return render(request,'index.html',{'category_types':category_types,'data_all':data_all})