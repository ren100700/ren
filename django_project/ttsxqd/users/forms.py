from django import forms

from users.models import User


class UserForm(forms.Form):
	username=forms.CharField(required=True,error_messages={'requird':'用户名必填','max_length':'用户名不能多于20个字符','min_length':'用户名不能少于5个字符'},max_length=20,min_length=5)
	password = forms.CharField(required=True, error_messages={'requird': '密码必填', 'min_length': '密码不能少于8个字符'},min_length=8)
	password2 = forms.CharField(required=True, error_messages={'requird': '密码必填', 'min_length': '密码不能少于8个字符'},min_length=8)
	email = forms.CharField(required=True)

	def clean(self):
		# 校验用户名是否已经注册过
		user=User.objects.filter(username=self.cleaned_data.get('username'))
		if user:
			# 如果已经注册过
			raise forms.ValidationError({'username':'用户名已经存在'})
		# 校验密码和确认密码是否相同
		if self.cleaned_data.get('password')!=self.cleaned_data.get('password2'):
			raise forms.ValidationError({'password':'两次输入的密码不相同'})
		return  self.cleaned_data


class UserLoginForm(forms.Form):
	username=forms.CharField(required=True,error_messages={'requird':'用户名必填','max_length':'用户名不能多于8个字符','min_length':'用户名不能少于3个字符'},max_length=8,min_length=3)
	password=forms.CharField(required=True,error_messages={'requird':'密码必填','min_length':'密码不能少于6个字符'},min_length=6)

	def clean(self):
		# 校验用户名是否已经注册过
		user=User.objects.filter(username=self.cleaned_data['username'],password=self.cleaned_data['password'])
		if not user:
			# 如果已经注册过
			raise forms.ValidationError({'username': '用户名不存在'})
		return  self.cleaned_data