#coding=utf-8

#coding:utf-8

#-*- coding:utf-8 -*-

import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
# mysql数据库游标设置
conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='first_flask', charset='utf8')
cursor = conn.cursor()
cursor.execute('set names utf8')
cursor.execute('set autocommit = 1')
app.secret_key = 'iii'

# MongoDb配置
app.config['MONGO_DBNAME'] = 'DATA'
app.config['MONGO_URI'] = 'mongodb://172.16.31.171:27017/DATA'
mongo = PyMongo(app)



# 查询数据库中用户名
def username1():
    sql  = "select * from users"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0][1]


# 查询数据库中的密码
def password1():
    sql  = "select * from admin"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0][2]

# 接收前端表单参数
def get_data():
    username = request.form['username']
    password = request.form['password']
    sn = request.fomr['SN']
    list = []
    list.append[username]


# 根据SN查询结束的天数
def find_end_day(sn):
    sql = "select * from end_day where SN = %s" %(sn)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# 查询出全部数据
def find_data():
    sql = "select * from end_day"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
# 删除end_day的数据
@app.route('/delete_end_day/<id>')
def delete_end_day(id):
    sql = "DELETE FROM end_day WHERE id = %s" % (id)
    cursor.execute(sql)
    return redirect(url_for('adminview'))


# 登录页面
@app.route('/userlogin',methods=['POST','GET'])
def userlogin():
    if request.method == 'POST':
        if (request.form['username']==username1() and request.form['password']==password1()):
            return redirect(url_for('view'))
        else:
            return redirect(url_for('mistake'))
    return render_template('user_login.html')

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if request.method == 'POST':
        if (request.form['username'] == username1() and request.form['password']==password1()):
            return redirect(url_for('getdata'))
        else:
            return redirect(url_for('mistake'))
    return render_template('admin_login.html')

@app.route('/getdada',methods=['POST','GET'])
def getdata():
    return render_template('getdata.html')
# 显示页面
@app.route('/userview',methods=['POST','GET'])
def userview():
    if int(find_end_day(request.form['SN'])[0][1])<3000:
        error = '该物联卡使用天数已不足3000天请注意'
    return render_template('userview.html', end_day=find_end_day(request.form['SN']),error=error)

@app.route('/adminview',methods=['POST','GET'])
def adminview():
    if int(find_end_day(request.form['SN'])[0][1])<3000:
        error = '该物联卡使用天数已不足3000天请注意'
    return render_template('adminview.html', data=find_data(),error=error)
# 错误页面
@app.route('/404',methods=['POST','GET'])
def mistake():
    return render_template('404.html')
# 索引页面
@app.route('/index',methods=['POST','GET'])
def index():
    return render_template('index.html')

# 注册页面
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    error = None
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            error = '两次密码不相同'
        elif len(request.form['username'])<6 or len(request.form['username'])>20:
            error = '用户名格式输入错误，必须6-20位，请重新输入'
        elif request.form['username'][0] not in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
            error = '用户名开头必须是字母，请重新输入'
        elif len(request.form['password1']) < 6:
            error = '密码长度至少6位,不能为纯数字,不能有空格'
        else:
            username=request.form['username']
            password=request.form['password1']
            sql = "insert into admin(username,password) values ('%s','%s')" %(username,password)
            cursor.execute(sql)
            return redirect(url_for('index'))
    return render_template('registerpage.html', error=error)

@app.route('/addcard',methods=['POST','GET'])
def addcard():
    error = None
    if request.method == 'POST':
        try:
            a2=request.form['end_day']
            a3 = request.form['sn']
            a4 = request.form['result']
            a5 = request.form['card_flow']
            a6 = request.form['total_flow']
            a7 = request.form['left_flow']
            a8 = request.form['package_name']
            a9 = request.form['sms_count']
            sql = "insert into end_day (end_day, sn,result,card_flow,total_flow,left_flow,package_name,sms_count) values('%s','%s','%s','%s','%s','%s','%s','%s')" %(a2,a3,a4,a5,a6,a7,a8,a9)
            cursor.execute(sql)
            return redirect(url_for('adminview'))
        except Exception as e:
            return redirect(url_for('mistake'))
    else:
        flash('添加错误')
    return render_template('addcard.html')
# 管理员页面
# @app.route('admin)

if __name__ == '__main__':
    app.run()
