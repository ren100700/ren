
OK = 200
SUCCESS = {'code':200,'msg':'请求成功'}
PARAMS_ERROR = {'code':400,'msg':'参数错误'}
DATABASE_ERROR = {'code':500,'msg':'数据库崩溃'}

# 用户模块
USER_REGISTER_CODE_ERROR = {'code':1000,'msg':'验证码错误'}
USER_REGISTER_PARAMS_VALID = {'code':1001,'msg':'请填写完整的注册参数'}
USER_REGISTER_MOBILE_INVALID = {'code':1002,'msg':'手机格式不正确'}
USER_REGISTER_PASSWARD_ERROR = {'code':1003,'msg':'两次密码不正确'}
USER_REGISTER_MOBILE_EXSIST = {'code':1004,'msg':'手机号已存在'}
USER_REGISTER_USER_ERROR = {'code':1008,'msg':'手机号注册更新数据库失败'}

USER_LOGIN_PARAMS_VALID = {'code':1005,'msg':'请填写完整的登录信息'}
USER_LOGIN_USER_NOT = {'code':1009,'msg':'没有该用户信息'}
USER_LOGIN_PASSWORD_INVALID = {'code':1006,'msg':'登录密码不正确'}
USER_LOGIN_PHONE_INVALID = {'code':1007,'msg':'请填写正确的手机号'}

USER_PROFILE_IMAGE_UPDATE_ERROR = {'code':1010,'msg':'用户上传图片的格式错误'}
USER_REGISTER_USER_IS_EXSITS = {'code':1011,'msg':'用户名已存在'}

USER_AUTH_CRAD_INVALID = {'code':1012,'msg':'请填写正确的身份证号码'}


MYHOUSE_USER_IS_NOT_AUTH = {'code':1013,'msg':'请先通过实名认证'}
ORDER_START_END_TIME_ERROR = {'code': 1014, 'msg': '时间选择错误'}
