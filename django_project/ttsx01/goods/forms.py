from django import forms

from goods.models import GoodsCategory


class GoodsForm(forms.Form):
	name=forms.CharField(required=True,error_messages={'required':'商品名称必填'})
	goods_sn=forms.CharField(required=True,error_messages={'goods_sn':'商品货号必填'})
	category=forms.CharField(required=True,error_messages={'category':'商品分类必填'})
	goods_nums=forms.CharField(required=True,error_messages={'goods_nums':'商品库存必填'})
	market_price=forms.CharField(required=True,error_messages={'market_price':'市场价必填'})
	shop_price=forms.CharField(required=True,error_messages={'shop_price':'超市价必填'})
	goods_brief=forms.CharField(required=True,error_messages={'goods_brief':'超市价必填'})
	goods_front_image=forms.ImageField(required=False)

	def clean_category(self):
		category_id=self.cleaned_data['category']
		category=GoodsCategory.objects.filter(id=category_id).first()
		if category:
			return category
		else:
			raise forms.ValidationError({'category':'商品分类选择错误'})