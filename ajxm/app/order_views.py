from datetime import datetime
import os
import re

from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session

from app.models import db, User, House, Facility, Area, HouseImage, Order
from utils import status_code
from utils.config import Config
from utils.funcitons import image_code, is_login


order_blue = Blueprint('order',__name__)


@order_blue.route('/', methods=['POST'])
@is_login
def order():
    # 接收参数
    dict = request.form
    house_id = int(dict.get('house_id'))
    start_date = datetime.strptime(dict.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(dict.get('end_date'), '%Y-%m-%d')
    # 验证有效性
    if not all([house_id, start_date, end_date]):
        return jsonify(status_code.PARAMS_ERROR)
    if start_date > end_date:
        return jsonify(status_code.ORDER_START_END_TIME_ERROR)
    # 查询房屋对象
    try:
        house = House.query.get(house_id)
    except:
        return jsonify(status_code.DATABASE_ERROR)
    # 创建订单对象
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = (end_date - start_date).days + 1
    order.house_price = house.price
    order.amount = order.days * order.house_price

    try:
        order.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    # 返回信息
    return jsonify(code=status_code.OK)


@order_blue.route('/orders/')
@is_login
def orders():
	return render_template('orders.html')


# 获取所有订单
@order_blue.route('/allorders/', methods=['GET'])
@is_login
def all_orders():

    uid = session['user_id']
    order_list = Order.query.filter(Order.user_id == uid).order_by(Order.id.desc())
    order_list2 = [order.to_dict() for order in order_list]
    return jsonify(olist=order_list2)


@order_blue.route('/lorders/')
@is_login
def lorders():
	return render_template('lorders.html')


@order_blue.route('/fd/',methods=['GET'])
@is_login
def my_lorders():
    uid=session['user_id']
    #查询当前用户的所有房屋编号
    hlist=House.query.filter(House.user_id==uid)
    hid_list=[house.id for house in hlist]
    #根据房屋编号查找订单
    order_list=Order.query.filter(Order.house_id.in_(hid_list)).order_by(Order.id.desc())
    #构造结果
    olist=[order.to_dict() for order in order_list]
    return jsonify(olist=olist)


@order_blue.route('/order/<int:id>/',methods=['PUT'])
@is_login
def status(id):
    #接收参数：状态
    status=request.form.get('status')
    #查找订单对象
    order=Order.query.get(id)
    #修改
    order.status=status
    #如果是拒单，需要添加原因
    if status=='REJECTED':
        order.comment=request.form.get('comment')
    #保存
    try:
        order.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    return jsonify(code=status_code.OK)