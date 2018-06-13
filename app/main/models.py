from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

from .. import loginManager, mysql

# Howard 2017/11/26，Joshua 2018/2/6修改
@loginManager.user_loader
def load_user(user_id): # 讀取使用者
    return User.getUserID(user_id)

# Joshua 2018/2/6修改
class User(UserMixin,mysql.Model):
    __tablename__ = 'users'
    id = mysql.Column(mysql.Integer, primary_key=True)
    user_name = mysql.Column(mysql.String(16), unique = True)
    email = mysql.Column(mysql.String(80), unique=True)
    password_hash = mysql.Column(mysql.String(128))
    role_id = mysql.Column(mysql.Integer, mysql.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.user_name

    # Joshua 2018/2/5新增，等於定義password的getter方法，但直接取password這個屬性，會跳AttributeError
    @property
    def password(self):
        raise AttributeError('you can not get password')

    # Joshua 2018/2/5新增，直接對password屬性定義setter方法，但可以直接更改password屬性
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Joshua 2018/2/5新增，登入時會進這個方法，確認該密碼跟存在db的hash值是相同的
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Joshua 2018/2/7，判斷使用者是否有某權限
    def can(self, permission):
        return self.role is not None and self.role.name == permission
    
    # Joshua 2018/2/7，判斷使用者是否具備admin權限
    def is_admin(self):
        return self.can('admin')

    # Joshua 2018/2/9，判斷使用者是否具備user權限
    def is_user(self):
        return self.can('user')


    def insertAdmin():
        admin = Role.query.filter_by(name='admin').first()
        if admin is None:
            admin = Role(name='admin')
        u = User(user_name='admin',password='0000',role=admin)
        mysql.session.add_all([admin,u])
        mysql.session.commit()
        
    # Joshua 2018/2/6修改
    def getAuthRecord(user_name):
        return User.query.filter_by(user_name = user_name).first()

    # Joshua 2018/2/7修改
    def getUserID(user_id):
        return User.query.get(user_id)

    # Joshua 2018/2/8修改
    def getAllRecord(user_name):
        return User.query.filter_by(user_name = user_name).first()

    def getLikeRecord(user_name=None, user_type=None):
        if user_name and user_type:
            filters = {
                User.user_name.like('%' + user_name + '%'),
                User.role_id == Role.query.filter_by(name=user_type).first().id
            }
            user = User.query.filter(*filters).all()
        elif user_name and not user_type:
            user = User.query.filter(User.user_name.like('%' + user_name + '%')).all()
        elif not user_name and user_type:
            user = User.query.filter(User.role_id == Role.query.filter_by(name=user_type).first().id).all()
        else:
            user = User.query.all()
        return user

    # Joshua 2018/2/8修改，把User和Role拆成兩個表後，新增方式改變
    def insertRecord(user_name, password, userType, fullName, phoneNumber, email):
        role = Role.query.filter_by(name=userType).first()
        user = User(user_name=user_name, password=password, fullName=fullName, phoneNumber=phoneNumber, email=email, role=role)
        mysql.session.add_all([role,user])
        mysql.session.commit()

    # Joshua 2018/4/3修改，把User和Role拆成兩個表後，更新方式改變，處理 password 為 None 的狀況
    def updateRecord(user_name, userType, fullName, phoneNumber, email, password=None):
        role = Role.query.filter_by(name=userType).first()
        user = User.query.filter_by(user_name = user_name).first()
        if password:
            user.password = password
        user.fullName = fullName
        user.phoneNumber = phoneNumber
        user.email = email
        user.role = role
        mysql.session.add(user)
        mysql.session.commit()
    
    def deleteRecord(user_name):
        user = User.query.filter_by(user_name = user_name).first()
        mysql.session.delete(user)
        mysql.session.commit()

    # 因為已經繼承UserMixin類別，所以除非要修改不然不用再實作以下方法
    # # is_authenticated()方法：使用者是否登入
    # def is_authenticated(self):
    #     return True
    # # is_active()方法：是否允許此使用者登入
    # def is_active(self):
    #     return True
    # # is_anonymous()方法：是否為匿名使用者，也就是未登入使用者
    # def is_anonymous(self):
    #     return False
    # # get_id()方法：傳回唯一的使用者，可定義要回傳的欄位，這邊為id，Joshua，2018/2/6修改
    # def get_id(self):
    #     return self.id

# Joshua 2018/2/8，建立一個匿名使用者類別
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.user_name = 'Guest'

    # Joshua 2018/2/8，判斷匿名使用者是否有某權限，這邊直接回None，
    # 不然發生 403 error時，會判斷權限，但沒有設定匿名使用者的狀況會報錯
    def can(self, permission):
        return None

# Joshua 2018/2/6，定義權限欄位
class Role(mysql.Model):
    __tablename__ = 'roles'
    id = mysql.Column(mysql.Integer, primary_key = True)
    name = mysql.Column(mysql.String(64), unique = True)
    users = mysql.relationship('User', backref = 'role', lazy = 'dynamic')

    # Joshua 2018/2/7，啟動mysql後，可以直接用shell直接插入所有權限
    def insertRoles():
        roles = ['admin','user']
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            mysql.session.add(role)
        mysql.session.commit()

# 設定匿名使用者類別
# loginManager.anonymous_user = Anonymous