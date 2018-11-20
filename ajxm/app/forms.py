from flask_wtf import FlaskForm

from wtforms import SubmitField,StringField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.models import User


class UserRegisterForm(FlaskForm):
	username = StringField('账号',validators=[DataRequired()])
	password = StringField('密码',validators=[DataRequired()])
	password2 = StringField('确认密码',validators=[DataRequired(),
											   EqualTo('password','两次密码不一致')])
	submit = SubmitField('提交')

	def validate_username(self,field):
		if len(field.data)<3:
			raise ValidationError('用户名不能少于3个字符')
		user = User.query.filter(User.username == field.data).first()
		if user:
			raise ValidationError('该账号已注册')