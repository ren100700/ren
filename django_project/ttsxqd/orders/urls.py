from django.conf.urls import url

from orders import views

urlpatterns=[
	url(r'^order/',views.order,name='order'),
	url(r'^user_center_site/',views.user_center_site,name='user_center_site'),
]