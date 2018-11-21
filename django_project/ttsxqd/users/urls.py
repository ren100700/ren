from django.conf.urls import url

from users import views

urlpatterns=[
	url(r'^login/',views.login,name='login'),
	# url(r'^logout/',views.logout,name='logout'),
	url(r'^register/',views.register,name='register'),
	url(r'^user_center_info/',views.user_center_info,name='user_center_info'),
]