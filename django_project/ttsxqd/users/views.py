from django.contrib.auth.hashers import check_password,make_password
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import UserForm, UserLoginForm
from users.models import User
from django.contrib import auth

def login(request):
	if request.method=='GET':
		return render(request,'login.html')

	if request.method=='POST':
		# 使用cookie+session形式实现登录
		username= request.POST.get('username')
		password = request.POST.get('password')
		# all()校验参数，如果为空则返回false
		if not all([username,password]):
			msg='请填写完整信息'
			return render(request,'login.html',{'msg':msg})
		# 校验是否能通过username和password找到user对象
		user = User.objects.filter(username=username).first()
		if user:
			if not check_password(password,user.password):
				msg='密码错误'
				return render(request,'login.html',{'msg':msg})
			else:
				# 向cookie中设值，向user_ticket表中设值
				request.session['user_id']=user.id

				# 设置session过期时间
				# request.session.set_expiry(timedelta(days=1))
				request.session.set_expiry(60000)
				return HttpResponseRedirect(reverse('home:index'))
		else:
			msg='用户名错误'
			return render(request,'login.html',{'msg':msg})


def register(request):
	if request.method=='GET':
		return render(request,'register.html')

	if request.method=='POST':
		# 校验页面中传递的参数是否完整
		form=UserForm(request.POST)
		# is_valid():判断表单是否验证通过
		if form.is_valid():
			username=form.cleaned_data.get('username')
			password=make_password(form.cleaned_data.get('password'))
			password2=form.cleaned_data.get('password2')
			email=form.cleaned_data.get('email')
			# 直接跳转
			User.objects.create(username=username,password=password,email=email)
			return HttpResponseRedirect(reverse('users:login'))
		else:
			return render(request,'register.html',{'form':form})


def user_center_info(request):
	if request.method=='GET':
		return render(request,'user_center_info.html')
