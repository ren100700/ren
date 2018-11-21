from django.conf.urls import url

from goods import views

urlpatterns=[
	url(r'^goods_detail/(\d+)/',views.goods_detail,name='goods_detail'),
	url(r'^goods_list/',views.goods_list,name='goods_list'),

]