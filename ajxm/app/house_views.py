import os
import re

from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session

from app.models import db, User, House, Facility, Area, HouseImage, Order
from utils import status_code
from utils.config import Config
from utils.funcitons import image_code, is_login


house_blue = Blueprint('house',__name__)

@house_blue.route('/myhouse/')
def myhouse():
	return render_template('myhouse.html')


#判断是否实名认证通过
@house_blue.route('/auth_myhouse/',methods=['GET'])
@is_login
def auth_house():
	if request.method == 'GET':
		user_id = session['user_id']
		user = User.query.get(user_id)
		# 判断是否已经完成过实名认证
		if user.id_name:
			house_list = House.query.filter(House.user_id == user_id).order_by(House.id.desc())
			house_list2 = []
			for house in house_list:
				house_list2.append(house.to_dict())
			return jsonify(code='200', hlist=house_list2)
		else:
			# 没有完成实名认证
			return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


# 进入添加新房源页面
@house_blue.route('/newhouse/')
@is_login
def new_house():
	return render_template('newhouse.html')


# 添加新的房源
@house_blue.route('/newhouse/',methods=['POST'])
@is_login
def set_newhouse():
	params = request.form.to_dict()
	facility_ids = request.form.getlist('facility')
	# 验证数据的有效性

	# 创建对象并保存
	house = House()
	house.user_id = session['user_id']
	house.area_id = params.get('area_id')
	house.title = params.get('title')
	house.price = params.get('price')
	house.address = params.get('address')
	house.room_count = params.get('room_count')
	house.acreage = params.get('acreage')
	house.beds = params.get('beds')
	house.unit = params.get('unit')
	house.capacity = params.get('capacity')
	house.deposit = params.get('deposit')
	house.min_days = params.get('min_days')
	house.max_days = params.get('max_days')
	# 根据设施的编号查询设施对象
	if facility_ids:
		facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
		house.facilities = facility_list
	house.add_update()
	# 返回结果
	return jsonify(code='200', house_id=house.id)


@house_blue.route('/area_facility/',methods=['GET'])
@is_login
def area_facility():
    #查询地址
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    #查询设施
    facility_list = Facility.query.all()
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    #构造结果并返回
    return jsonify(area=area_dict_list,facility=facility_dict_list)


@house_blue.route('/image/',methods=['POST'])
@is_login
def newhouse_image():
    #接收房屋编号
    house_id=request.form.get('house_id')
    #接收图片信息
    f1=request.files.get('house_image')
    #保存到图片
    con = Config()
    url = os.path.join(os.path.join(con.UPLOAD_FOLDER, 'house'), f1.filename)
    f1.save(url)

    #保存图片对象
    image=HouseImage()
    image.house_id=house_id
    image.url=os.path.join('/static/upload/house', f1.filename)
    image.add_update()
    #房屋的默认图片
    house=House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url=os.path.join('/static/upload/house', f1.filename)
        house.add_update()
    #返回图片信息
    return jsonify(code='200',url=os.path.join('/static/upload/house', f1.filename))


# 房源详情页面
@house_blue.route('/detail/')
def detail():
	return render_template('detail.html')


#房源页面详情<int:id>
@house_blue.route('/detail/<int:id>/',methods=['GET'])
def house_detail(id):
    #查询房屋信息
    house=House.query.get(id)
    #查询设施信息
    facility_list=house.facilities
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    #判断当前房屋信息是否为当前登录的用户发布，如果是则不显示预订按钮
    booking=1
    if 'user_id' in session:
        if house.user_id==session['user_id']:
            booking=0

    return jsonify(house=house.to_full_dict(),facility_list=facility_dict_list,booking=booking)


# 主页页面
@house_blue.route('/index/')
def index():
	return render_template('index.html')


#主页面详情
@house_blue.route('/hindex/', methods=['GET'])
def index_h():

    user_name = ''
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        user_name = user.name
        code = status_code.OK

    # 返回最新的5个房屋信息
    hlist = House.query.order_by(House.id.desc()).all()[:5]
    hlist2 = [house.to_dict() for house in hlist]
    # 查找地区信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]

    return jsonify(code=code, name=user_name, hlist=hlist2, alist=area_dict_list)


#搜索页面
@house_blue.route('/search/')
def search():
	return render_template('search.html')


#搜索页面详情
@house_blue.route('/searchall/',methods=['GET'])
def searchall():
	if request.method == 'GET':
		dict = request.args

		sort_key = dict.get('sk')  # 排序
		a_id = dict.get('aid')  # 区域
		begin_date = dict.get('sd')  # 入住时间
		end_date = dict.get('ed')  # 离店时间

		houses = House.query.filter_by(area_id=a_id)
		# 不能查询自己发布的房源，排除当前用户发布的房屋
		if 'user_id' in session:
			hlist = houses.filter(House.user_id != (session['user_id']))

		# 满足时间条件，查询入住时间和退房时间在首页选择时间内的房间，并排除掉这些房间
		order_list = Order.query.filter(Order.status != 'REJECTED')
		# 情况一：
		order_list1 = Order.query.filter(Order.begin_date >= begin_date, Order.end_date <= end_date)
		# 情况二：
		order_list2 = order_list.filter(Order.begin_date < begin_date, Order.end_date > end_date)
		# 情况三：
		order_list3 = order_list.filter(Order.end_date >= begin_date, Order.end_date <= end_date)
		# 情况四：
		order_list4 = order_list.filter(Order.begin_date >= begin_date, Order.begin_date <= end_date)
		# 获取订单中的房屋编号
		house_ids = [order.house_id for order in order_list2]
		for order in order_list3:
			house_ids.append(order.house_id)
		for order in order_list4:
			if order.house_id not in house_ids:
				house_ids.append(order.house_id)
		# 查询排除入住时间和离店时间在预约订单内的房屋信息
		hlist = hlist.filter(House.id.notin_(house_ids))

		# 排序规则,默认根据最新排列
		sort = House.id.desc()
		if sort_key == 'booking':
			sort = House.order_count.desc()
		elif sort_key == 'price-inc':
			sort = House.price.asc()
		elif sort_key == 'price-des':
			sort = House.price.desc()
		hlist = hlist.order_by(sort)
		hlist = [house.to_dict() for house in hlist]

		# 获取区域信息
		area_list = Area.query.all()
		area_dict_list = [area.to_dict() for area in area_list]

		return jsonify(code=status_code.OK, houses=hlist, areas=area_dict_list)


@house_blue.route('/booking/')
def booking():
	return render_template('booking.html')


@house_blue.route('/getbookingbyid/<int:id>/')
def get_booking_by_id(id):
    house = House.query.get(id)
    return jsonify(house=house.to_dict())