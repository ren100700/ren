from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from goods.forms import GoodsForm
from goods.models import GoodsCategory,Goods
from ttsx01.settings import PAGE_NUMBER


def goods_category_list(request):
	if request.method=='GET':
		# 获取分类信息
		categorys = GoodsCategory.objects.all()
		# 返回类型
		category_types = GoodsCategory.CATEGORY_TYPE
		return render(request,'goods_category_list.html',{'categorys':categorys,'category_types':category_types})


def goods_category_edit(request,id):
	if request.method=='GET':
		# 获取当前选择的商品分类
		category = GoodsCategory.objects.get(pk=id)
		# 返回商品类型
		categorys_types = GoodsCategory.CATEGORY_TYPE
		return render(request,'goods_category_detail.html',{'category':category,'categorys_types':categorys_types})
	if request.method=='POST':
		category_front_image=request.FILES.get('category_front_image')
		if category_front_image:
			category=GoodsCategory.objects.get(pk=id)
			category.category_front_image=category_front_image
			category.save()
		return HttpResponseRedirect(reverse('goods:goods_category_list'))


def goods_list(request):
	if request.method=='GET':
		try:
			page_number=int(request.GET.get('page',1))
		except:
			page_number=1
		goods=Goods.objects.all()
		category_types=GoodsCategory.CATEGORY_TYPE
		paginator=Paginator(goods,PAGE_NUMBER)
		page=paginator.page(page_number)
		return render(request,'goods_list.html',{'page':page,'category_types':category_types})


def goods_add(request):
	if request.method=='GET':
		category_types = GoodsCategory.CATEGORY_TYPE
		return render(request,'goods_detail.html',{'category_types': category_types})
	if request.method=='POST':
		# 保存数据
		# 1.获取页面中传递的参数，并校验是否填写完整
		form = GoodsForm(request.POST,request.FILES)
		if form.is_valid():
			# 保存*args,**kwargs
			data=form.cleaned_data
			Goods.objects.create(**data)
			return HttpResponseRedirect(reverse('goods:goods_list'))
		else:
			return render(request,'goods_detail.html',{'form':form})

		# 2.保存
		# 3.跳转到页面


def goods_delete(request):
	if request.method=='POST':
		Goods.objects.filter(pk=id).delete()
		return JsonResponse({'code':200,'msg':'请求成功'})


def goods_edit(request,id):
	if request.method=='GET':
		goods=Goods.objects.get(pk=id)
		category_types=GoodsCategory.CATEGORY_TYPE
		return render(request,'goods_detail.html',{'goods':goods,'category_types':category_types})
	if request.method=='POST':
		form=GoodsForm(request.POST,request.FILES)
		if form.is_valid():
			data=form.cleaned_data
			goods_front_image=data.pop('goods_front_image')
			if goods_front_image:
				goods=Goods.objects.filter(pk=id).first()
				goods.goods_front_image=goods_front_image
				goods.save()
			Goods.objects.filter(pk=id).update(**data)
			return HttpResponseRedirect(reverse('goods:goods_list'))
		else:
			# 验证失败
			goods=Goods.objects.get(pk=id)
			category_types = GoodsCategory.CATEGORY_TYPE
			return render(request,'goods_detail.html',{'goods':goods,'category_types':category_types,'form':form})


def goods_desc(request,id):
	if request.method=='GET':
		goods=Goods.objects.filter(pk=id).first()
		return render(request,'goods_desc.html',{'goods':goods})
	if request.method=='POST':
		# 保存商品描述信息
		content=request.POST.get('content')
		Goods.objects.filter(pk=id).update(goods_desc=content)
		return HttpResponseRedirect(reverse('goods:goods_list'))


# def goods_delete1(request,):
# 	if request.method=='GET':
# 		goods=Goods.objects.filter(pk=id).first()
# 		goods.delete()
# 		return HttpResponseRedirect(reverse('goods:goods_list'))