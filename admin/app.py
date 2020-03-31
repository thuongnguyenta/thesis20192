from flask import Flask,render_template, flash, redirect , url_for , session ,request, logging
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import datetime
import json
# from flask_dropzone import Dropzone
# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

# import pymysql
# from app import app
# from db_config import mysql
from flask import jsonify
# from wtforms import Form, StringField , TextAreaField ,PasswordField , validators
# from passlib.hash import sha256_crypt
# from functools import wraps


app = Flask(__name__)
app.debug = True

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = '20192'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

@app.route('/')
def form(): 
    return render_template('login.html')

@app.route('/login',methods=["POST","GET"])
def login(): 
    if request.method=='POST':
        email = request.form['user_name']
        password = request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE email=%s AND password =%s AND role=1",[email,password])
        rows=cur.fetchall()
        if len(rows) ==0:
            error="Incorrect email or password"
            return render_template('login.html',error=error)
        else:
            session['id'] = rows[0]['id_account']
            session['name'] = rows[0]['username']
            session["email"] =rows[0]['email']
            # session['role'] =rows[0]['role']
            session['address']=rows[0]['address']
            session['phone_number']=rows[0]['phone_number']
            session['cover_image']=rows[0]['cover_image']
            return redirect(url_for('product'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    # session.pop('id',None)
    # session.pop('role',None)
    return render_template('login.html')

@app.route('/product')
def product():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes")
    rows=cur.fetchall()

    cur.execute("SELECT * FROM shoes,shoes_surface WHERE shoes.id_shoes=shoes_surface.id_shoes")
    surfaces=cur.fetchall()


    cur.execute("SELECT * FROM shoes,shoes_color WHERE shoes_color.id_shoes=shoes.id_shoes")
    colors=cur.fetchall()

    cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes_color.id_shoes=shoes.id_shoes AND shoes_color_image.id_shoes_color=shoes_color.id_shoes_color")
    color_images=cur.fetchall()
    
    return render_template('basic-table.html',shoes=rows,surfaces=surfaces,colors=colors,color_images=color_images,a=[],b=[])

@app.route('/order')
def order(): 
    # if 'id' in session:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM user_order,account,ship WHERE user_order.id_user=account.id_account AND ship.id_order=user_order.id_order")
        user_order=cur.fetchall()
        cur.execute("SELECT * FROM user_order,order_detail,shoes,shoes_color_image WHERE user_order.id_order= order_detail.id_order AND shoes.id_shoes=order_detail.id_shoes AND shoes_color_image.id_shoes_color=order_detail.id_shoes_color GROUP BY order_detail.id_order_detail")
        order_detail=cur.fetchall()
        return render_template('order.html',user_order=user_order,order_detail=order_detail)


@app.route('/profile')
def profile():
    if 'id' in session:
        id_admin= session['id']
        cur= mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE id_account=%s",[id_admin])
        rows=cur.fetchall()
        return render_template('profile.html',account=rows)

@app.route('/profile/update',methods=['POST','GET'])
def update_profile():
    if 'id' in session:
        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']
            phone_number =request.form['phone_number']
            address =request.form['address']
            cur=mysql.connection.cursor()
            cur.execute("UPDATE account SET username=%s,phone_number=%s,address=%s WHERE id_account =%s ",[username,phone_number,address,session['id']])
            mysql.connection.commit()
            return redirect(url_for('profile'))
        return redirect(url_for('profile'))
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    cur=mysql.connection.cursor()
    cur.execute("SELECT count(*) as number FROM shoes")
    number=cur.fetchall()
    number_product=number[0]['number']

    today = datetime.datetime.today()
# datem = datetime.datetime(today.year, today.month, 1)
    cur.execute("SELECT SUM(total_price) as income FROM user_order,ship WHERE user_order.id_order=ship.id_order AND MONTH(time_order)=%s AND YEAR(time_order)=%s AND ship.status=%s",[today.month,today.year,"Hoàn Thành"])
    income=cur.fetchall()
    # now_income=income[0]['income']
    # print(now_income)
    if income :
        now_income=int(income[0]['income'])
    else:
        now_income=int(0)
    # print(now_income)

    cur.execute("SELECT count(*) as number_user FROM account ")
    user=cur.fetchall()
    number_user=user[0]['number_user']

    cur.execute("SELECT total_price,order_quantity,SUM(total_price) as income,MONTH(time_order) as month,YEAR(time_order) as year FROM `user_order` GROUP BY MONTH(time_order),YEAR(time_order)")
    combo_chart=cur.fetchall()
    combo_chart=json.dumps(combo_chart)

    cur.execute("SELECT *,count(*) as number_pur FROM shoes,user_order,order_detail WHERE shoes.id_shoes=order_detail.id_shoes AND order_detail.id_order=user_order.id_order AND YEAR(time_order)=%s AND MONTH(time_order)=%s GROUP BY shoes.id_shoes ORDER BY number_pur DESC limit 10",[today.year,today.month])
    sp=cur.fetchall()

    # print(sp)
    if sp:
        sp=sp
    else:
        if today.month==1:
            year=today.year-1
            month=12
            cur.execute("SELECT *,count(*) as number_pur FROM shoes,user_order,order_detail WHERE shoes.id_shoes=order_detail.id_shoes AND order_detail.id_order=user_order.id_order AND YEAR(time_order)=%s AND MONTH(time_order)=%s GROUP BY shoes.id_shoes ORDER BY number_pur DESC limit 10",[year,month])
        else:
            cur.execute("SELECT *,count(*) as number_pur FROM shoes,user_order,order_detail WHERE shoes.id_shoes=order_detail.id_shoes AND order_detail.id_order=user_order.id_order AND YEAR(time_order)=%s AND MONTH(time_order)=%s GROUP BY shoes.id_shoes ORDER BY number_pur DESC limit 10",[today.year,today.month-1])
        sp=cur.fetchall()



    return render_template('dashboard.html',number_product=number_product,income=now_income,number_user=number_user,sp=enumerate(sp),combo_chart=combo_chart,today=today)

@app.route('/getdata')
def getdata():
    cur.execute("SELECT total_price,order_quantity,SUM(total_price) as income,MONTH(time_order) as month,YEAR(time_order) as year FROM `user_order` GROUP BY MONTH(time_order),YEAR(time_order)")
    combo_chart=cur.fetchall()
    combo_chart=json.dumps(combo_chart)
    return combo_chart

@app.route('/dashboard/product_purchase', methods=['POST'])
def product_purchase():
    if request.method=='POST':
        cur=mysql.connection.cursor()
        month=request.form['month']
        year=request.form['year']
        print(month,year)
        cur.execute("SELECT *,count(*) as number_pur FROM shoes,user_order,order_detail WHERE shoes.id_shoes=order_detail.id_shoes AND order_detail.id_order=user_order.id_order AND YEAR(time_order)=%s AND MONTH(time_order)=%s GROUP BY shoes.id_shoes ORDER BY number_pur DESC limit 10",[year,month])
        sp=cur.fetchall()
        # print(sp)
        resp=""
        status=""
        for idx,pr in enumerate(sp):
            if pr['sale'] == 0:
                status="Avaiable"
            else:
                status="Sale: "+str(pr['sale'])+"%"
            resp+="<tr><td>"+str(idx+1)+"</td><td class='txt-oflo'>"+pr['shoes_name']+"</td><td>"+status+"</td><td class='txt-oflo'>"+ str(pr['number_pur'])+"</td><td><span class='text-success'>"+str(pr['price'])+"<ins>đ</ins></span></td></tr>"
                
        print(resp)
        return resp
@app.route('/product/color_image', methods=["POST"])
def color_image():
    if request.method=='POST':
        cur=mysql.connection.cursor()
        color=request.form['color']
        name=request.form['name']
        print(color,name)
        cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.shoes_name=%s AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes_color.color=%s",[name, color])
        sp=cur.fetchall()
        reps=""
        for idx,pr in enumerate(sp):
            reps+="<img src='/static/image/shoes_image/"+pr['image']+"' width='50px' height='50px'>"
        return reps

@app.route('/add_product',methods=['GET','POST'])
def add_product():
    if request.method =="POST":
        cur =mysql.connection.cursor()
        shoes_name= request.form['shoes_name']
        gender_shoes =request.form['gender']
        shoes_type =request.form['shoes_type']
        feature =request.form['feature']
        price =request.form['price']
        athleter= request.form['athleter']
        if athleter :
            athleter
        else:
            athleter=None
        sale= request.form['sale']
        describe= request.form['describe']
        catalogy =request.form['catalogy']
        surface= request.form.getlist("surface")
        colors =request.form.getlist('color')
        # print(shoes_name,gender_shoes,shoes_type,feature,price,athleter,sale,describe,catalogy,surface,colors)
        cur.execute("INSERT INTO shoes(id_shoes,shoes_name,gender_shoes,shoes_type,feature,price,athleter,sale,catalogy,`describe`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",["NULL",shoes_name,gender_shoes,shoes_type,feature,price,athleter,sale,catalogy,describe])
        mysql.connection.commit()

        cur.execute("SELECT * FROM shoes WHERE shoes_name=%s ORDER BY id_shoes DESC limit 1",[shoes_name])
        rows= cur.fetchall()
        id_shoes = rows[0]['id_shoes']
        for sf in surface:
            cur.execute("INSERT INTO shoes_surface(id_shoes_surface,id_shoes,surface) VALUES(%s,%s,%s)",["NULL",id_shoes,sf])
            mysql.connection.commit()
        for color in colors:
            cur.execute("INSERT INTO shoes_color(id_shoes_color,id_shoes,color) VALUES(%s,%s,%s)",["NULL",id_shoes,color])
            mysql.connection.commit()
        return redirect(url_for('product'))
    return redirect(url_for('product'))

@app.route('/update_product/<id_shoes>',methods=['GET','POST'])
def update_product(id_shoes):
    # print("b")
    if request.method =="POST":
        # print("a")
        cur =mysql.connection.cursor()
        shoes_name= request.form['shoes_name']
        gender_shoes =request.form['gender']
        shoes_type =request.form['shoes_type']
        feature =request.form['feature']
        price =request.form['price']
        athleter= request.form['athleter']
        if athleter :
            athleter
        else:
            athleter=None
        sale= request.form['sale']
        describe= request.form['describe']
        catalogy =request.form['catalogy']
        new_surface= request.form.getlist("surface")
        new_colors =request.form.getlist('color')
        cur.execute("UPDATE shoes SET shoes_name=%s,gender_shoes=%s,shoes_type=%s,feature=%s,price=%s,athleter=%s,sale=%s,catalogy=%s,`describe`=%s WHERE id_shoes=%s",[shoes_name,gender_shoes,shoes_type,feature,price,athleter,sale,catalogy,describe,id_shoes])
        mysql.connection.commit()

        # Update surface
        cur.execute("SELECT * FROM shoes_surface WHERE id_shoes=%s",[id_shoes])
        old_surface=[]
        temps= cur.fetchall()
        for temp in temps:
            old_surface.append(temp['surface'])
        for sf in new_surface:
            if sf not in old_surface:
                cur.execute("INSERT INTO shoes_surface(id_shoes_surface,id_shoes,surface) VALUES(%s,%s,%s)",["NULL",id_shoes,sf]) 
                mysql.connection.commit()
        for old_sf in old_surface:
            if old_sf not in new_surface:
                cur.execute("DELETE FROM shoes_surface WHERE id_shoes =%s AND surface =%s",[id_shoes,old_sf])

        # ADD color
        cur.execute("SELECT * FROM shoes_color WHERE id_shoes=%s",[id_shoes])
        old_color=[]
        set_image_color=[]
        temps_color=cur.fetchall()
        for temp in temps_color:
            old_color.append(temp['color'])
        for cl in new_colors:
            if cl not in old_color:
                cur.execute("INSERT INTO shoes_color(id_shoes_color,id_shoes,color) VALUES(%s,%s,%s)",["NULL",id_shoes,cl]) 
                mysql.connection.commit()

        # select color set image
        cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes_color.id_shoes=shoes.id_shoes AND shoes_color_image.id_shoes_color=shoes_color.id_shoes_color AND shoes.id_shoes=%s GROUP BY shoes_color.id_shoes_color",[id_shoes])
        set_cl_image = cur.fetchall()
        for i in set_cl_image:
            set_image_color.append(i['color'])
        
        for old_cl in old_color:
            
            if old_cl not in new_colors:
                
                if old_cl not in set_image_color:
                    cur.execute("DELETE FROM shoes_color WHERE id_shoes =%s AND color =%s",[id_shoes,old_cl])
                    mysql.connection.commit()

        return redirect(url_for('product'))
    return redirect(url_for('product'))
@app.route('/complete/<id_order>')
def complete(id_order):
    # if 'id' in session:
        cur=mysql.connection.cursor()
        cur.execute("UPDATE ship SET status=%s WHERE id_order= %s",["Hoàn Thành",id_order])
        mysql.connection.commit()
        return redirect(url_for('order'))
    # return redirect(url_for('form'))


@app.route('/product_color/<id_shoes>', methods=['POST'])
def username_check():
	# conn = None
	# cursor = None
    cur =mysql.connection.cursor()
    email = request.form['email']
    
    # validate the received values
    if email and request.method == 'POST':		
        # conn = mysql.connect()
        # cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cur.execute("SELECT * FROM account WHERE email=%s", [email])
        row = cur.fetchall()
        
        if row:
            resp = jsonify('<span style=\'color:red;\'>Email unavailable</span>')
            resp.status_code = 200
            return resp
        else:
            resp = jsonify('OK')
            resp.status_code = 200
            return resp
    else:
        resp = jsonify('<span style=\'color:red;\'>Email is required field.</span>')
        resp.status_code = 200
        return resp
