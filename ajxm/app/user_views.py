import os
import re

from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session

from app.models import db, User
from utils import status_code
from utils.config import Config
from utils.funcitons import image_code, is_login

blue = Blueprint('user',__name__)


@blue.route('/')
def hello_world():
	return 'Hello World'


@blue.route('/register/',methods=['GET'])
def register():
	if request.method == 'GET':
		return render_template('register.html')


@blue.route('/image_code/',methods=['GET'])
def register_image_code():
	if request.method == 'GET':
		i_code = image_code()
		return jsonify({'code':200,'image_code':i_code})


@blue.route('/create_db/')
def create_db():
	db.create_all()
	return '创建成功'


@blue.route('/register/',methods=['POST'])
def my_register():
	if request.method == 'POST':
		mobile = request.form.get('mobile')
		imagecode = request.form.get('imagecode')
		passwd = request.form.get('password')
		passwd2 = request.form.get('password2')

		if not all([mobile,passwd,passwd2]):
			return jsonify(status_code.USER_REGISTER_PARAMS_VALID)
		# 验证图片验证码是否正确
		# if session.get('code')!=imagecode:
		# 	return jsonify(status_code.USER_REGISTER_CODE_ERROR)
		if not re.match(r'^1[3456789]\d{9}$',mobile):
			return jsonify(status_code.USER_REGISTER_MOBILE_INVALID)
		if passwd != passwd2:
			return jsonify(status_code.USER_REGISTER_PASSWARD_ERROR)
		if User.query.filter(User.phone==mobile).count():
			return jsonify(status_code.USER_REGISTER_MOBILE_EXSIST)
		user = User()
		user.phone = mobile
		user.password = passwd
		user.name = mobile
		try:
			user.add_update()
			return jsonify(status_code.SUCCESS)
		except:
			return jsonify(status_code.USER_REGISTER_USER_ERROR)


@blue.route('/login/',methods = ['GET'])
def login():
	if request.method == 'GET':
		return render_template('login.html')


@blue.route('/login/',methods =['POST'])
def user_login():
	if request.method == 'POST':
		mobile = request.form.get('mobile')
		password = request.form.get('password')
		if not all([mobile,password]):
			return jsonify(status_code.USER_REGISTER_PARAMS_VALID)
		if not re.match(r'^1[3456789]\d{9}$',mobile):
			return jsonify(status_code.USER_REGISTER_MOBILE_INVALID)

		user = User.query.filter_by(phone=mobile).first()
		if user:
			if not user.check_pwd(password):
				return jsonify(status_code.USER_LOGIN_PASSWORD_INVALID)
			else:
				session['user_id'] = user.id
				return jsonify(status_code.SUCCESS)
		else:
			return jsonify(status_code.USER_LOGIN_USER_NOT)


@blue.route('/my/',methods=['GET'])
@is_login
def my():
	if request.method == 'GET':
		return render_template('my.html')


@blue.route('/profile/',methods=['GET'])
@is_login
def profile():
	if request.method == 'GET':
		return render_template('profile.html')


@blue.route('/logout/',methods=['DELETE'])
@is_login
def logout():
	session.clear()
	return jsonify(status_code.SUCCESS)


@blue.route('/user/',methods=['PUT'])
@is_login
def user_profile():
	dict = request.form
	dict_file = request.files
	if 'avatar' in dict_file:
		try:
			# 获取头像文件
			f1 = request.files['avatar']
			# mime-type:国际规范，表示文件的类型，如text/html,text/xml,image/png,image/jpeg..
			if not re.match('image/.*', f1.mimetype):
				return jsonify(status_code.USER_PROFILE_IMAGE_UPDATE_ERROR)
		except:
			return jsonify(code=status_code.PARAMS_ERROR)
		# 保存到upload中
		con = Config()
		url = os.path.join(con.UPLOAD_FOLDER, f1.filename)
		f1.save(url)

		# 如果未出错
		# 保存用户的头像信息
		try:
			user = User.query.get(session['user_id'])
			user.avatar = os.path.join('/static/upload', f1.filename)
			user.add_update()
		except:
			return jsonify(status_code.DATABASE_ERROR)
		# 则返回图片信息
		return jsonify(code='200', url=os.path.join('/static/upload', f1.filename))

	elif 'name' in dict:
		# 修改用户名
		name = dict.get('name')
		# 判断用户名是否存在
		if User.query.filter_by(name=name).count():
			return jsonify(status_code.USER_REGISTER_USER_IS_EXSITS)
		else:
			user = User.query.get(session['user_id'])
			user.name = name
			user.add_update()
			return jsonify(status_code.SUCCESS)
	else:
		return jsonify(status_code.PARAMS_ERROR)


@blue.route('/user/', methods=['GET'])
@is_login
def get_user_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify(user=user.to_basic_dict())


@blue.route('/auth/',methods=['GET'])
@is_login
def auth():
	if request.method == 'GET':
		return render_template('auth.html')


@blue.route('/auth1/', methods=['GET'])
@is_login
def get_user_auth():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify(user=user.to_basic_dict())


@blue.route('/auth1/',methods=['PUT'])
@is_login
def set_user_auth():
	# 获取数据
	id_name = request.form.get('id_name')
	id_card = request.form.get('id_card')
	# 验证是否完整
	if not all([id_name,id_card]):
		return jsonify(status_code.PARAMS_ERROR)
	if not re.match(r'^[123456789]\d{17}$',id_card):
		return jsonify(status_code.USER_AUTH_CRAD_INVALID)
	# 修改数据对象
	try:
		user = User.query.get(session['user_id'])
	except:
		return jsonify(status_code.DATABASE_ERROR)
	try:
		user.id_name = id_name
		user.id_card = id_card
		user.add_update()
	except:
		return jsonify(status_code.DATABASE_ERROR)
	# 返回数据
	return jsonify(status_code.SUCCESS)
