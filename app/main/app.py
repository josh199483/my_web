"""
建立時間: 2017/11/26
作者: Howard
說明:
    首頁、讀取使用者、登入頁面、登出、身份管理頁面、身份管理AJAX
修改時間: 2018/2/2
作者: Joshua
說明: 
    修改一些管理功能，和增加權限管理讓使用者依照不同權限使用不同頁面功能
"""

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_uploads import UploadSet, IMAGES

from . import main
from .models import User
from .form import LoginForm, ImageForm
from ..decorators import admin_required
from .. import imagesUpload

@main.route('/',methods=['GET'])
def index():
    return render_template('index.html')

# Joshua 2018/2/6
@main.route('/login',methods=['GET','POST'])
def login():
    # 當使用者已經登入時，除非藉著登出不然不讓使用者直接回到login頁面
    if current_user.is_authenticated:
        return redirect(url_for('main.identity_management'))
    form = LoginForm()
    # post request
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.identity_management'))
    return render_template('login.html',form=form)    
 
# Joshua 2018/2/6
@main.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout(): # 登出，把session全部pop掉
    logout_user()
    return redirect(url_for('main.login'))

# Howard 2017/11/26，Joshua 2018/2/8修改
@main.route('/identity_management', methods = ['GET', 'POST'])
@admin_required
@login_required
def identity_management(): # 身分管理頁面
    user_name = request.args.get('user_name')
    user_type = request.args.get('user_type')
    result = User.getLikeRecord(user_name, user_type)
    if user_name == None:
        user_name = ''
    if user_type == None:
        user_type = 'all'
    return render_template('identity_management.html', result=result, user_name=user_name, user_type=user_type)

# 上傳圖片
@main.route('/image/', methods=['GET','POST'])
def upload_image():
    form = ImageForm()
    if form.validate_on_submit():
        file_name = imagesUpload.save(form.uploads.data)
        file_url = imagesUpload.url(file_name)
        print(file_name, file_url)
        return render_template('image.html', form=form, file_url=file_url)
    else:
        file_url=None
    return render_template('image.html', form=form, file_url=file_url)


# # Joshua 2018/2/8，身分管理新增
# class identityListApi(Resource):
#     def post(self):
#         """傳入參數
#             {"userName":'joshua',
#             "password":'000000',
#             "confirmPassword":'000000',
#             "userType":'admin',
#             "fullName":'chen',
#             "phoneNumber":'0987654321',
#             "email":'pome@pomerobotservice.com'}
#         """
#         userName = request.form.get('userName')
#         password = request.form.get('password')
#         confirmPassword = request.form.get('confirmPassword')
#         userType = request.form.get('userType')
#         fullName = request.form.get('fullName')
#         phoneNumber = request.form.get('phoneNumber')
#         email = request.form.get('email')
#         if User.getAllRecord(userName):
#             return jsonify(result='使用者名稱重複')# 使用者名稱重複
#         elif len(userName) < 6 or len(userName) > 12:
#             return jsonify(result='使用者名稱長度需介於6~12')# 使用者名稱長度不符
#         elif len(password) < 6 or len(password) > 12:
#             return jsonify(result='密碼長度需介於6~12')# 密碼長度不符
#         elif confirmPassword != password:
#             return jsonify(result='確認密碼與密碼不一致')# 確認密碼與密碼不一致
#         elif userType == '':
#             return jsonify(result='使用者等級未選擇')# 使用者等級未選擇
#         elif fullName == '':
#             return jsonify(result='全名未填寫')# 全名未填寫
#         elif phoneNumber == '':
#             return jsonify(result='手機未填寫')# 手機未填寫
#         elif email == '':
#             return jsonify(result='mail未填寫')# E-mail未填寫
#         else:
#             User.insertRecord(userName, password, userType, fullName, phoneNumber, email)
#             return jsonify(result='新增成功')# 新增成功


# # Joshua 2018/2/8，身分管理修改、刪除
# class identityApi(Resource):
#     def put(self,userName):
#         """傳入參數
#             {"password":'000000',
#             "confirmPassword":'000000',
#             "userType":'admin',
#             "fullName":'chen',
#             "phoneNumber":'0987654321',
#             "email":'pome@pomerobotservice.com'}
#         """
#         password = request.form.get('password')
#         confirmPassword = request.form.get('confirmPassword')
#         userType = request.form.get('userType')
#         fullName = request.form.get('fullName')
#         phoneNumber = request.form.get('phoneNumber')
#         email = request.form.get('email')
#         if password == '' and confirmPassword == '':
#             if userType == '':
#                 return jsonify(result='使用者等級未選擇')# 使用者等級未選擇
#             elif fullName == '':
#                 return jsonify(result='全名未填寫')# 全名未填寫
#             elif phoneNumber == '':
#                 return jsonify(result='手機未填寫')# 手機未填寫
#             elif email == '':
#                 return jsonify(result='mail未填寫')# E-mail未填寫
#             else:
#                 User.updateRecord(userName, userType, fullName, phoneNumber, email, password=password)
#                 return jsonify(result='更新成功')# 修改成功
#         else:
#             if len(password) < 6 or len(password) > 12:
#                 return jsonify(result='密碼長度需介於6~12')# 密碼長度不符
#             elif confirmPassword != password:
#                 return jsonify(result='確認密碼與密碼不一致')# 確認密碼與密碼不一致
#             elif userType == '':
#                 return jsonify(result='使用者等級未選擇')# 使用者等級未選擇
#             elif fullName == '':
#                 return jsonify(result='全名未填寫')# 全名未填寫
#             elif phoneNumber == '':
#                 return jsonify(result='手機未填寫')# 手機未填寫
#             elif email == '':
#                 return jsonify(result='mail未填寫')# E-mail未填寫
#             else:
#                 User.updateRecord(userName, userType, fullName, phoneNumber, email, password=password)
#                 return jsonify(result='更新成功')# 修改成功
    
#     def delete(self,userName):
#         User.deleteRecord(userName)
#         return jsonify(result='刪除成功')# 刪除成功