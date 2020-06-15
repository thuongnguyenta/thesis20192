from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *


from flask import Flask,render_template, flash, redirect , url_for , session ,request, logging
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import datetime
import json
# from flask_dropzone import Dropzone
# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
import base64



from form import EmailForm,PasswordForm
from itsdangerous import URLSafeSerializer

# import com.snowplowanalytics.snowplow.tracker.*;
# import com.snowplowanalytics.snowplow.tracker.emitter.*;
# import com.snowplowanalytics.snowplow.tracker.payload.*;


from flask_mail import Mail, Message
# from . import app
# from .forms import EmailForm
# from .models import User
# from .util import send_email, ts


# import pymysql
# from app import app
# from db_config import mysql
from flask import jsonify
# from wtforms import Form, StringField , TextAreaField ,PasswordField , validators
# from passlib.hash import sha256_crypt
# from functools import wraps


client = RecombeeClient('hanoi-university-of-science-and-technology-dev', 'Q1NZZQ9do57L9rFjJtN293YZzInHoVGWjFogWIYiAQR8cHAyKw32eB2zAYSPurnH')


app = Flask(__name__)
app.debug = True


app.config['SECRET_KEY']="secret key"
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = '20192'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'seeyouagain791142@gmail.com'
app.config['MAIL_PASSWORD'] = '24111997'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

uploads_dir = './static/image/shoes_image/'


uploads_dir_account = './static/image/people'

mysql = MySQL(app)

@app.route('/')
def form(): 
    return render_template('user_login.html')

# @app.route('/login',methods=["POST","GET"])
# def login(): 
    # if request.method=='POST':
    #     email = request.form['user_name']
    #     password = request.form['password']
    #     cur=mysql.connection.cursor()
    #     cur.execute("SELECT * FROM account WHERE email=%s AND password =%s AND role=1",[email,password])
    #     rows=cur.fetchall()
    #     if len(rows) ==0:
    #         error="Incorrect email or password"
    #         return render_template('login.html',error=error)
    #     else:
    #         session['id'] = rows[0]['id_account']
    #         session['name'] = rows[0]['username']
    #         session["email"] =rows[0]['email']
    #         # session['role'] =rows[0]['role']
    #         session['address']=rows[0]['address']
    #         session['phone_number']=rows[0]['phone_number']
    #         session['cover_image']=rows[0]['cover_image']
    #         return redirect(url_for('dashboard'))
    # return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    # session.pop('id',None)
    # session.pop('role',None)
    return render_template('user_login.html')

@app.route('/product')
def product():
    if 'id' in session:
        if session['role']==1:
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
        return redirect(url_for('user_product'))
    return redirect(url_for('user_login'))

@app.route('/order')
def order(): 
    # if 'id' in session:
    if 'id' in session:
        if session['role']==1:
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM user_order,account,ship WHERE user_order.id_user=account.id_account AND ship.id_order=user_order.id_order")
            user_order=cur.fetchall()
            cur.execute("SELECT * FROM user_order,order_detail,shoes,shoes_color_image WHERE user_order.id_order= order_detail.id_order AND shoes.id_shoes=order_detail.id_shoes AND shoes_color_image.id_shoes_color=order_detail.id_shoes_color GROUP BY order_detail.id_order_detail")
            order_detail=cur.fetchall()
            return render_template('order.html',user_order=user_order,order_detail=order_detail)
        return redirect(url_for('user_product'))
    return redirect(url_for('user_login'))
    
@app.route('/customer')
def customer(): 
    # if 'id' in session:
    if 'id' in session:
        if session['role']==1:
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM account WHERE role=2 ")
            user=cur.fetchall()
            # cur.execute("SELECT * FROM user_order,order_detail,shoes,shoes_color_image WHERE user_order.id_order= order_detail.id_order AND shoes.id_shoes=order_detail.id_shoes AND shoes_color_image.id_shoes_color=order_detail.id_shoes_color GROUP BY order_detail.id_order_detail")
            # order_detail=cur.fetchall()
            return render_template('customer.html',user=user)
        return redirect(url_for('user_product'))
    return redirect(url_for('user_login'))


@app.route('/profile')
def profile():
    if 'id' in session:
        if session['role']==1:
            id_admin= session['id']
            cur= mysql.connection.cursor()
            cur.execute("SELECT * FROM account WHERE id_account=%s",[id_admin])
            rows=cur.fetchall()
            return render_template('profile.html',account=rows)
        return redirect(url_for('user_product'))
    return redirect(url_for('user_login'))

@app.route('/profile/update',methods=['POST','GET'])
def update_profile():
    if 'id' in session:
        if session['role']==1:
            if request.method=='POST':
                # print("1")
                username=request.form['username']
                # print("2")
                # password=request.form['password']
                # print("3")
                phone_number =request.form['phone_number']
                address =request.form['address']
                cur=mysql.connection.cursor()
                cur.execute("UPDATE account SET username=%s,phone_number=%s,address=%s WHERE id_account =%s ",[username,phone_number,address,session['id']])
                mysql.connection.commit()
                return redirect(url_for('profile'))
            return redirect(url_for('profile'))
        return redirect(url_for('user_product'))
    return render_template("user_login.html")

@app.route('/profile/change_password',methods=['POST','GET'])
def change_password():
    if 'id' in session:
        if request.method=='POST':
            cur= mysql.connection.cursor()
            old_password=request.form['old_password']
            new_password=request.form['new_password']
            cf_new_password =request.form['cf_new_password']
            if new_password!=cf_new_password:
                return "Confirm password not match !"
            else:
                cur.execute("SELECT * FROM account WHERE id_account=%s",[session['id']])
                password =cur.fetchall()
                if old_password==password[0]['password']:
                    cur.execute("UPDATE account SET password =%s WHERE id_account = %s",[new_password,session['id']])
                    mysql.connection.commit()
                    return "Done"
                else :
                    return "Password isn't correct !"
        return redirect(url_for('profile'))
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'id' in session:
        if session['role']==1:
            cur=mysql.connection.cursor()
            cur.execute("SELECT count(*) as number FROM shoes")
            number=cur.fetchall()
            number_product=number[0]['number']

            today = datetime.datetime.today()
            # datem = datetime.datetime(today.year, today.month, 1)
            cur.execute("SELECT SUM(total_price) as income FROM user_order,ship WHERE user_order.id_order=ship.id_order AND MONTH(time_order)=%s AND YEAR(time_order)=%s AND ship.status=%s",[today.month,today.year,"Hoàn Thành"])
            income=cur.fetchall()
            print (income)
            # now_income=income[0]['income']
            # print(now_income)
            if income[0]['income'] != None:
                now_income=int(income[0]['income'])
                # print(now_income)
            else:
                now_income=int(0)
            # print(now_income)

            cur.execute("SELECT SUM(total_price) as income FROM user_order,ship WHERE user_order.id_order=ship.id_order AND ship.status='Giao Hàng'")
            user=cur.fetchall()
            if user[0]['income'] != None:
                user_income=int(user[0]['income'])
                # print(now_income)
            else:
                user_income=int(0)
            # number_user=user[0]['income']

            cur.execute("SELECT total_price,order_quantity,SUM(total_price) as income,MONTH(time_order) as month,YEAR(time_order) as year FROM `user_order` GROUP BY MONTH(time_order),YEAR(time_order)")
            combo_chart=cur.fetchall()
            combo_chart=json.dumps(combo_chart)


            cur.execute("SELECT * FROM shoes WHERE shoes.id_shoes NOT IN(select s.id_shoes FROM shoes as s,order_detail,user_order WHERE user_order.id_order=order_detail.id_order AND s.id_shoes=order_detail.id_shoes AND MONTH(user_order.time_order)=MONTH(CURRENT_DATE) GROUP BY s.id_shoes)")
            shoes_remain=cur.fetchall()

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

            cur.execute("SELECT * FROM comment,shoes,account WHERE comment.id_shoes=shoes.id_shoes AND comment.id_user=account.id_account AND status=0 limit 10")
            comment=cur.fetchall()


            cur.execute("SELECT * FROM account WHERE account.role=2 limit 10")
            account=cur.fetchall()

            return render_template('dashboard.html',number_product=number_product,income=now_income,user_income=user_income,sp=enumerate(sp),combo_chart=combo_chart,today=today,comment=comment,account=account,shoes_remain=shoes_remain)
        return redirect(url_for('user_product'))
    return redirect(url_for('user_login'))

@app.route('/dashboard/comment',methods=['POST'])
def comment_ap():
    # print("1")
    if request.method=='POST':
        # print("2")
        id_comment=request.form['id_comment']
        print(id_comment)
        cur=mysql.connection.cursor()
        cur.execute("UPDATE comment SET status=%s WHERE id_comment=%s",[1,id_comment])
        mysql.connection.commit()

        cur.execute("SELECT * FROM comment,shoes,account WHERE comment.id_shoes=shoes.id_shoes AND comment.id_user=account.id_account AND status=0 limit 10")
        comment=cur.fetchall()
        print (comment)
        resp=""
        for cm in comment :
            # div1 = "<div class='comment-body' id='comment-body-"+str(cm['id_comment'])+"'>"
            # div2 = "<div class='user-img'> <img src='.."+cm['cover_image']+"'  alt='user' class='img-circle' style='border: 1px solid;width:50px; height:50px;'></div>"
            # div3 = "<div class='mail-contnet'><h5>"+cm['username']+"</h5><span class='time'>"+cm['time_review'].strftime("%H:%M %D,%B %Y")+"</span><br/><span class='mail-desc' >"+cm['comments']+"</span> <div id='comment_"+str(cm['id_comment'])+"' class='btn btn btn-rounded btn-default btn-outline m-r-5 approve'><i class='ti-check text-success m-r-5'></i>Approve</div><div href='javacript:void(0)' class='btn-rounded btn btn-default btn-outline'><i class='ti-close text-danger m-r-5'></i> Reject</div></div>"
            # div4 = "<div class='name_product'>"+str(cm['shoes_name'])+"</div>"
            # div5 = "<div class='star' id='"+str(cm['star'])+"'>"
            # for i in range(0,cm['star']):
            #     div5+="<span class='fa fa-star checked_star'></span>"
            # for i in range(cm['star'],5):
            #     div5+="<span class='fa fa-star uncheck_star'></span>"
            # div5+="</div></div>"
            # resp+=div1+div2+div3+div4+div5
            div1="<div class='comment-body' id='comment-body-"+str(cm['id_comment'])+"'>"
            div2="<div class='user-img'> <img src='.."+cm['cover_image']+"' alt='user' class='img-circle' style='border: 1px solid;width:50px; height:50px;'></div>"
            div3="<div class='mail-contnet'><h5>"+cm['username']+"</h5><span class='time'>"+(cm['time_review'].strftime("%H:%M %d,%B %Y"))+"</span><br/><span class='mail-desc' >"+cm['comments']+"</span> <div id='comment_"+str(cm['id_comment'])+"' class='btn btn btn-rounded btn-default btn-outline m-r-5 approve_div'><i class='ti-check text-success m-r-5'></i>Approve</div><div href='javacript:void(0)' id='reject_"+str(cm['id_comment'])+"' class='btn-rounded btn btn-default btn-outline reject_div'><i class='ti-close text-danger m-r-5'></i> Reject</div></div>"
            div4="<div class='name_product'>"+cm['shoes_name']+"</div>"
            div5="<div class='star' id='star_"+str(cm['star'])+"'>"
            for i in range(0,cm['star']):
                div5+="<span class='fa fa-star checked_star'></span>"
            for i in range(cm['star'],5):
                div5+="<span class='fa fa-star uncheck_star'></span>"
            div5+="</div></div>"                     
                                
            resp+=div1+div2+div3+div4+div5
        print(resp)
        return resp

@app.route('/getdata', methods=['POST'])
def getdata():
    cur=mysql.connection.cursor()
    cur.execute("SELECT CAST(SUM(order_quantity) AS INT)as quantity ,SUM(total_price) as total,SUM(if(ship.status = 'Giao Hàng',user_order.total_price,0)) as income,MONTH(time_order) as month,YEAR(time_order) as year FROM user_order,ship WHERE user_order.id_order=ship.id_order GROUP BY MONTH(time_order),YEAR(time_order)")
    combo_chart=cur.fetchall()
    print(combo_chart)
    combo_chart=json.dumps(combo_chart)
    return combo_chart

@app.route('/getdata_shoes', methods=['POST'])
def getdata_shoes():
    # print("xxx")
    cur=mysql.connection.cursor()
    # if request.form['month'] and request.form['year']:
    #     month=request.form['month']
    #     year=request.form['year']
    #     cur.execute("SELECT shoes_name,count(*)as number FROM user_order,order_detail,shoes WHERE user_order.id_order=order_detail.id_order AND MONTH(user_order.time_order)= %s AND YEAR(user_order.time_order)=%s AND shoes.id_shoes=order_detail.id_shoes GROUP BY order_detail.id_shoes",[month,year])
    # else:
    print("12")
    cur.execute("SELECT shoes_name,count(*)as number FROM user_order,order_detail,shoes WHERE user_order.id_order=order_detail.id_order AND MONTH(user_order.time_order)= MONTH(CURRENT_DATE) AND YEAR(user_order.time_order)=2020 AND shoes.id_shoes=order_detail.id_shoes GROUP BY order_detail.id_shoes")
    chart=cur.fetchall()
    chart=json.dumps(chart)
    return chart
@app.route('/updatedata_shoes', methods=['POST'])
def updatedata_shoes():
    if request.method=='POST':
        print("xxx")
        cur=mysql.connection.cursor()
        # year=request.form
        # print(year)
        month=request.form['month']
        year=request.form['year']
        print(month,year)
        cur.execute("SELECT shoes_name,count(*)as number FROM user_order,order_detail,shoes WHERE user_order.id_order=order_detail.id_order AND MONTH(user_order.time_order)= %s AND YEAR(user_order.time_order)=%s AND shoes.id_shoes=order_detail.id_shoes GROUP BY order_detail.id_shoes",[month,year])
        chart=cur.fetchall()
        chart=json.dumps(chart)
        print(chart)
        return chart

@app.route('/dashboard/product_purchase', methods=['POST'])
def product_purchase():
    if request.method=='POST':
        cur=mysql.connection.cursor()
        month=request.form['month']
        year=request.form['year']
        print(request.form)
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
# 
# PRODUCT NOT PURCHAR IN MOTNH
# 
@app.route('/dashboard/product_not_purchase', methods=['POST'])
def product_not_purchase():
    if request.method=='POST':
        cur=mysql.connection.cursor()
        month=request.form['month']
        year=request.form['year']
        print("thuong")
        print(request.form)
        cur.execute("SELECT * FROM shoes WHERE shoes.id_shoes NOT IN(select s.id_shoes FROM shoes as s,order_detail,user_order WHERE user_order.id_order=order_detail.id_order AND s.id_shoes=order_detail.id_shoes AND MONTH(user_order.time_order)=%s AND YEAR(user_order.time_order)=%s GROUP BY s.id_shoes)",[month,year])
        sp=cur.fetchall()
        # print(sp)
        status=""
        resp=""
        for temp in sp:
            if temp['sale'] == 0:
                status="Avaiable"
            else:
                status="Sale: "+str(temp['sale'])+"%"
            resp+="<tr><td>"+str(temp['id_shoes'])+"</td><td class='txt-oflo'>"+temp['shoes_name']+"</td><td>"+status+"</td><td class='txt-oflo'>"+temp['shoes_type']+"</td><td>"+temp['feature']+"</td><td><span class='text-success'>"+str(temp['price'])+"<ins>đ</ins></span></td></tr>"

        print(resp)
        return resp

@app.route('/product/color_image', methods=["POST"])
def color_image():
    if request.method=='POST':
        cur=mysql.connection.cursor()
        shoes_name=request.form['shoes_name']
        id_shoes=request.form['id_shoes']
        color=request.form['color']
        # id_shoes=request.form['id_shoes']
        # print(color,name)
        cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.shoes_name=%s AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes_color.color=%s",[shoes_name, color])
        sp=cur.fetchall()
        reps=""
        for idx,pr in enumerate(sp):
            reps+="<input type='checkbox' name='color_image' value='"+str(pr['id_shoes_color_image'])+"' id='id_color_image_"+str(pr['id_shoes_color_image'])+"'><label class='' for='id_color_image_"+str(pr['id_shoes_color_image'])+"'><img src='./static/image/shoes_image/"+pr['image']+"' width='120px' height='120px'></label>"
        print (reps)
        return reps
# @app.route('/product/color_image/delete',methods=['POST'])
# def delete_color_image
@app.route('/delete/color_image',methods=['GET','POST'])
def delete_color_image():
    if request.method=='POST':
        cur =mysql.connection.cursor()
        id_shoes=request.form['id_shoes']
        # print("2")
        shoes_color =request.form['color']
        shoes_delete = request.form.getlist("color_image")
        # shoes_delete = request.form.getlist("color_image")
        # print(shoes_delete)
        if shoes_delete :
            for id_shoes_color_image in shoes_delete:
                cur.execute("DELETE FROM shoes_color_image WHERE id_shoes_color_image=%s",[id_shoes_color_image])
                mysql.connection.commit()
        cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.id_shoes=%s AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes_color.color=%s",[id_shoes, shoes_color])
        sp=cur.fetchall()
        resp=""
        for idx,pr in enumerate(sp):
            resp+="<input type='checkbox' name='color_image' value='"+str(pr['id_shoes_color_image'])+"' id='id_color_image_"+str(pr['id_shoes_color_image'])+"'><label for='id_color_image_"+str(pr['id_shoes_color_image'])+"'><img src='./static/image/shoes_image/"+pr['image']+"' width='150px' height='150px'></label>"
        print (resp)
        return resp


@app.route('/add_product',methods=['GET','POST'])
def add_product():
    if 'id' in session:
        if session['role']==1:
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

                ### send infor to recombee

                # update_item_id(id_shoes)

                ###
                return redirect(url_for('product'))
            return redirect(url_for('product'))
        return redirect(url_for('user_product'))
    return redirect(url_for('user_login'))

@app.route('/update_product/<id_shoes>',methods=['GET','POST'])
def update_product(id_shoes):
    if 'id' in session:
        if session['role']==1:
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

                ### send infor to recombee
                # update_item_id(id_shoes)

                ###
                return redirect(url_for('product'))
            return redirect(url_for('product'))
        return redirect(url_for('user_product'))
    return redirect(url_for('user_login'))

@app.route('/update_product/color/<id_shoes>',methods=['POST','GET'])
def update_color_image(id_shoes):
    if request.method == 'POST':
        # print("1")
        cur =mysql.connection.cursor()
        id_shoes=request.form['id_shoes']
        # print("2")
        shoes_color =request.form['color']
        shoes_delete = request.form.getlist("color_image")
        # print("5")
        print('file_image_'+str(id_shoes))
        print(shoes_delete)
        # print(request)

        shoes_image = request.files.getlist('file')
        print(shoes_image)
        path_save=uploads_dir+str(id_shoes)+"/"+str(shoes_color)+"/"
        if not os.path.exists(path_save): 
            os.makedirs(path_save)
        # shoes_image.save(os.path.join(path_save, secure_filename(shoes_image.filename)))

         # save each "charts" file
        for file in shoes_image:
            file.save(os.path.join(path_save, secure_filename(file.filename)))
            # file.save(os.path.join(uploads_dir, secure_filename(file.name)))
        
            link=str(id_shoes)+"/"+str(shoes_color)+"/"+file.filename
        # print("4")
            print(link)
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM shoes,shoes_color WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes.id_shoes=%s AND shoes_color.color=%s",[id_shoes,shoes_color])
            temp=cur.fetchall()
            id_shoes_color = temp[0]['id_shoes_color']
            cur.execute("INSERT INTO shoes_color_image(id_shoes_color_image,id_shoes_color,image) VALUES(%s,%s,%s)",["NULL",id_shoes_color,link])
            mysql.connection.commit()
        # print(shoes_delete,shoes_image)
        ### send infor to recombee
        update_item_id(id_shoes)

        ###
        return redirect(url_for('product'))






@app.route('/complete/<id_order>')
def complete(id_order):
    # if 'id' in session:
    if 'id' in session:
        if session['role']==1:
            cur=mysql.connection.cursor()
            cur.execute("UPDATE ship SET status=%s WHERE id_order= %s",["Hoàn Thành",id_order])
            mysql.connection.commit()
            return redirect(url_for('order'))
    
        return redirect(url_for('user_product'))
    return redirect(url_for('user_login'))


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





# 
# 
# USER APP ROUTE
# 
# 




@app.route('/user_index')
def user_index():

    recommended={'recommId': '77c149bd875d2fb73b60574990507e6f', 'recomms': [{'id': '3', 'values': {'id_shoes': 3, 'shoes_type': 'Football', 'catalogy': 'Boot', 'color': ['Blue'], 'describe': 'Has alot of Surface and has durable with time\r\n', 'athleter': 'Cristiano Ronaldo', 'sale': 10, 'image': '/static/image/shoes_image/2/Lemon Venom/i1-e43bc0a3-290d-4620-983e-4d3d0a4688aa.webp', 'gender_shoes': 'Man', 'shoes_name': 'Nike Mercurial Superfly 7 Elite MDS FG', 'surface': ['Grass,Firm Ground,Artificial Grass,Soft Ground'], 'price': 8799000.0, 'feature': 'Reflection'}}, {'id': '1', 'values': {'id_shoes': 1, 'shoes_type': 'Running', 'catalogy': 'Snacker', 'color': ['Black,Orange,White,Red'], 'describe': 'Shoes suitable for every one,!', 'athleter': None, 'sale': 0, 'image': '/static/image/shoes_image/1/Black/52600ab1-4a17-4822-91f1-cfeb580c3004.webp', 'gender_shoes': 'Both', 'shoes_name': 'Nike React Infinity Run Flyknit', 'surface': ['Grass,Firm Ground,Artificial Grass,Soft Ground'], 'price': 4699000.0, 'feature': 'Waterproof'}}, {'id': '8', 'values': {'id_shoes': 8, 'shoes_type': 'Basketball', 'catalogy': 'Snacker', 'color': ['Black,Grey'], 'describe': 'The Air Jordan XXXIV PF continues the legacy of a cultural icon. Light, responsive sculpted', 'athleter': None, 'sale': 0, 'image': '/static/image/shoes_image/8/Black/3d7b03ea-3466-4056-a344-3492e88f8b6c.webp', 'gender_shoes': 'Man', 'shoes_name': 'Air Jordan XXXIV PF', 'surface': ['Artificial Grass,Multi Ground,Indoor,Grass'], 'price': 5129000.0, 'feature': 'Reflection'}}, {'id': '4', 'values': {'id_shoes': 4, 'shoes_type': 'Training', 'catalogy': 'Sandals', 'color': ['Purple'], 'describe': 'Comfortable for Woman and has style perfect\r\n', 'athleter': '', 'sale': 0, 'image': '/static/image/shoes_image/3/White Purple/112ade84-3b68-4b31-962f-8ce56d55ca71.webp', 'gender_shoes': 'Woman', 'shoes_name': 'Nike Air Max 200', 'surface': ['Multi Ground,Indoor'], 'price': 3519000.0, 'feature': 'Waterproof'}}]}
        
        # 1: id_item,3:id_account,2 is number get_recommend
    # recommended = client.send(RecommendItemsToUser(0,4,
    #                                         scenario='product_detail',
    #                                         return_properties=True,
    #                                         cascade_create=True))
        
    print(recommended)
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes LIMIT 4")
    shoes=cur.fetchall()

    cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes ORDER BY shoes.id_shoes DESC LIMIT 4")
    shoes_new=cur.fetchall()

    cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes.sale!=0 AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes LIMIT 8")
    shoes_sale=cur.fetchall()

    return render_template('user_index.html',shoes=recommended,shoes_new=shoes_new,shoes_sale=shoes_sale)




@app.route('/user_product')
def user_product():
    a=[]
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes")
    shoes=cur.fetchall()


    cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color GROUP BY shoes_color.id_shoes_color")
    color =cur.fetchall()  

    cur.execute("SELECT * FROM shoes,shoes_surface WHERE shoes.id_shoes=shoes_surface.id_shoes")
    surface=cur.fetchall()
    
    cur.execute("SELECT shoes_type,COUNT(*) as number FROM `shoes` GROUP BY shoes_type")
    shoe_type = cur.fetchall()

    return render_template('user_category.html',shoes=shoes,colors=color,shoe_type=shoe_type,surface=surface,a=a)

@app.route('/user_product/<type_s>')
def shoes_type(type_s):
    print(type_s)
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes.shoes_type=%s GROUP BY shoes.id_shoes",[type_s])
    rows=cur.fetchall()

    a=[]
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes")
    shoes=cur.fetchall()


    cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color GROUP BY shoes_color.id_shoes_color")
    color =cur.fetchall()  

    cur.execute("SELECT * FROM shoes,shoes_surface WHERE shoes.id_shoes=shoes_surface.id_shoes")
    surface=cur.fetchall()
    
    cur.execute("SELECT shoes_type,COUNT(*) as number FROM `shoes` GROUP BY shoes_type")
    shoe_type = cur.fetchall()

    return render_template('user_category.html',shoes=rows, colors=color, shoe_type=shoe_type,surface=surface,a=a,type_shoes=type_s)


@app.route('/user_search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        cur=mysql.connection.cursor()
        search_in4 = request.form['search_input']
        string = "%"+search_in4+"%"
        a=[]

        cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color AND shoes.shoes_name LIKE %s GROUP BY shoes.id_shoes",[string])
        rows= cur.fetchall()

        cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color GROUP BY shoes_color.id_shoes_color")
        color =cur.fetchall()    

        cur.execute("SELECT shoes_type,COUNT(*) as number FROM `shoes` GROUP BY shoes_type")
        shoe_type = cur.fetchall()

        cur.execute("SELECT * FROM shoes,shoes_surface WHERE shoes.id_shoes=shoes_surface.id_shoes")
        surface=cur.fetchall()

        return render_template('user_category.html',shoes=rows, colors=color, shoe_type=shoe_type,surface=surface,a=a,search=search_in4)
@app.route('/user_productdetail/<id_shoes>')
def detail_product(id_shoes):
    recommended={'recommId': 'a7f9137877465c2b505c468010440298', 'recomms': [{'id': '4', 'values': {'sale': 0, 'image': '/static/image/shoes_image/3/White Purple/112ade84-3b68-4b31-962f-8ce56d55ca71.webp', 'id_shoes': 4, 'shoes_type': 'Training', 'catalogy': 'Sandals', 'athleter': '', 'color': ['Purple'], 'describe': 'Comfortable for Woman and has style perfect\r\n', 'gender_shoes': 'Woman', 'shoes_name': 'Nike Air Max 200', 'surface': ['Multi Ground,Indoor'], 'price': 3519000.0, 'feature': 'Waterproof'}}, {'id': '8', 'values': {'sale': 0, 'image': '/static/image/shoes_image/8/Black/3d7b03ea-3466-4056-a344-3492e88f8b6c.webp', 'id_shoes': 8, 'shoes_type': 'Basketball', 'catalogy': 'Snacker', 'athleter': None, 'color': ['Black,Grey'], 'describe': 'The Air Jordan XXXIV PF continues the legacy of a cultural icon. Light, responsive sculpted', 'gender_shoes': 'Man', 'shoes_name': 'Air Jordan XXXIV PF', 'surface': ['Artificial Grass,Multi Ground,Indoor,Grass'], 'price': 5129000.0, 'feature': 'Reflection'}}, {'id': '3', 'values': {'sale': 10, 'image': '/static/image/shoes_image/2/Lemon Venom/i1-e43bc0a3-290d-4620-983e-4d3d0a4688aa.webp', 'id_shoes': 3, 'shoes_type': 'Football', 'catalogy': 'Boot', 'athleter': 'Cristiano Ronaldo', 'color': ['Blue'], 'describe': 'Has alot of Surface and has durable with time\r\n', 'gender_shoes': 'Man', 'shoes_name': 'Nike Mercurial Superfly 7 Elite MDS FG', 'surface': ['Grass,Firm Ground,Artificial Grass,Soft Ground'], 'price': 8799000.0, 'feature': 'Reflection'}}]}
    # if 'id' in session:
    # # 1: id_item,3:id_account,2 is number get_recommend
    #     recommended = client.send(RecommendItemsToItem('1', session['id'], 3,
    #                                            scenario='product_detail',
    #                                            return_properties=True,
    #                                            cascade_create=True))
    # else:
    #     recommended = client.send(RecommendItemsToItem('1', '0', 3,
    #                                            scenario='product_detail',
    #                                            return_properties=True,
    #                                            cascade_create=True))
    # print(recommended)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_color_image,shoes_color WHERE shoes.id_shoes=shoes_color.id_shoes and shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes.id_shoes=%s ORDER BY shoes_color.id_shoes_color",[id_shoes])
    shoe= cur.fetchall()

    cur.execute("SELECT * FROM shoes,shoes_color_image,shoes_color WHERE shoes.id_shoes=shoes_color.id_shoes and shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes.id_shoes=%s GROUP BY shoes_color.id_shoes_color ORDER BY shoes_color.id_shoes_color",[id_shoes])
    color=cur.fetchall()
    
    cur.execute("SELECT * FROM comment,account WHERE comment.id_user=account.id_account AND id_shoes=%s",[id_shoes])
    comment=cur.fetchall()

    cur.execute("SELECT ROUND(AVG(star),2) as St,count(*) as numb FROM comment WHERE id_shoes=%s GROUP BY id_shoes",[id_shoes])
    star=cur.fetchall()

    cur.execute("SELECT count(*) as number,star FROM comment WHERE id_shoes=%s GROUP BY star",[id_shoes])
    count_cm=cur.fetchall()

    cur.execute("SELECT * FROM shoes_surface WHERE id_shoes=%s",[id_shoes])
    surface=cur.fetchall()

    cur.execute("SELECT * FROM `shoes_color` WHERE shoes_color.id_shoes=%s",[id_shoes])
    all_color=cur.fetchall()

    return render_template("user_productdetail.html",shoe_detail=shoe,color=color,comment=comment,star=star,count_cm=count_cm,surface=surface,all_color=all_color,recommended=recommended)

@app.route('/user_login', methods=['POST','GET'])
def user_login():
    if 'id' in session:
        return redirect(url_for('user_index'))
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        admin = request.form.getlist('admin_check')
        temp=2
        if admin:
            temp=1
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE email=%s AND password =%s AND role=%s",[email,password,temp])
        rows=cur.fetchall()
        if len(rows) ==0:
            error="Incorrect email or password"
            return render_template('user_login.html',error=error)
        else:
            session['id'] = rows[0]['id_account']
            session['name'] = rows[0]['username']
            session["email"] =rows[0]['email']
            session['role'] =rows[0]['role']
            session['address']=rows[0]['address']
            session['phone_number']=rows[0]['phone_number']
            session['cover_image']=rows[0]['cover_image']
            if session['role']==1:
                return redirect(url_for('dashboard'))
            else :
                return redirect(url_for('user_index'))

    else:
        return render_template('user_login.html')

@app.route('/user_check', methods=['POST'])
def email_check():
	# conn = None
	# cursor = None
    cur =mysql.connection.cursor()
    print("1")
    email = request.form['email']
    print("2")
    
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


@app.route('/user_register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        user_name=request.form['user_name']
        phone_number=request.form['phone_number']
        address=request.form['address']
        cur=mysql.connection.cursor()
        # cur.execute("SELECT * FROM account WHERE email=%s",[email])
        # row=cur.fetchall()
        
        cur.execute("INSERT INTO account(id_account,email,username,password,phone_number,address,cover_image,role) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",["NULL",email,user_name,password,phone_number,address,"NULL","2"])
        mysql.connection.commit()
        flash("Complete Register")
        # login()
        return render_template('user_login.html')
    return  redirect(url_for('user_index'))

@app.route('/user_productdetail/comment/<id_shoes>', methods=['GET','POST'])
def comment(id_shoes):
    if 'id' in session:
        if request.method == 'POST':
            id_user=session['id']
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM user_order,order_detail WHERE user_order.id_order=order_detail.id_order AND user_order.id_user=%s AND order_detail.id_shoes=%s",[id_user,id_shoes])
            temp=cur.fetchall()
            if temp:
                print("1")
                star=request.form['rate']
                print("2")
                comment=request.form['comment']
                print("3")
                cur_time=datetime.datetime.now()
                
                cur.execute("INSERT INTO comment(id_comment,id_user,id_shoes,star,comments,time_review) VALUES(%s,%s,%s,%s,%s,%s)",["NULL",id_user,id_shoes,star,comment,cur_time])
                mysql.connection.commit()
                return redirect(url_for('detail_product',id_shoes=id_shoes))
            else :
                flash("You haven't purchase product to review !")
                return redirect(url_for("detail_product",id_shoes=id_shoes))
    else:
        flash('You are not login !')
        return redirect(url_for('detail_product',id_shoes=id_shoes))

@app.route('/user_cart')
def user_cart():
    if 'id' in session:
        if session['role']==2:
            recommended={'recommId': 'a7f9137877465c2b505c468010440298', 'recomms': [{'id': '4', 'values': {'sale': 0, 'image': '/static/image/shoes_image/3/White Purple/112ade84-3b68-4b31-962f-8ce56d55ca71.webp', 'id_shoes': 4, 'shoes_type': 'Training', 'catalogy': 'Sandals', 'athleter': '', 'color': ['Purple'], 'describe': 'Comfortable for Woman and has style perfect\r\n', 'gender_shoes': 'Woman', 'shoes_name': 'Nike Air Max 200', 'surface': ['Multi Ground,Indoor'], 'price': 3519000.0, 'feature': 'Waterproof'}}, {'id': '8', 'values': {'sale': 0, 'image': '/static/image/shoes_image/8/Black/3d7b03ea-3466-4056-a344-3492e88f8b6c.webp', 'id_shoes': 8, 'shoes_type': 'Basketball', 'catalogy': 'Snacker', 'athleter': None, 'color': ['Black,Grey'], 'describe': 'The Air Jordan XXXIV PF continues the legacy of a cultural icon. Light, responsive sculpted', 'gender_shoes': 'Man', 'shoes_name': 'Air Jordan XXXIV PF', 'surface': ['Artificial Grass,Multi Ground,Indoor,Grass'], 'price': 5129000.0, 'feature': 'Reflection'}}, {'id': '3', 'values': {'sale': 10, 'image': '/static/image/shoes_image/2/Lemon Venom/i1-e43bc0a3-290d-4620-983e-4d3d0a4688aa.webp', 'id_shoes': 3, 'shoes_type': 'Football', 'catalogy': 'Boot', 'athleter': 'Cristiano Ronaldo', 'color': ['Blue'], 'describe': 'Has alot of Surface and has durable with time\r\n', 'gender_shoes': 'Man', 'shoes_name': 'Nike Mercurial Superfly 7 Elite MDS FG', 'surface': ['Grass,Firm Ground,Artificial Grass,Soft Ground'], 'price': 8799000.0, 'feature': 'Reflection'}}]}
            # if 'id' in session:
            # 1: id_item,3:id_account,2 is number get_recommend
            recommended = client.send(RecommendItemsToUser(session['id'],3,
                                                    scenario='product_detail',
                                                    return_properties=True,
                                                    cascade_create=True))
            
            print(recommended)
            id_account= session['id']
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM cart,cart_detail,shoes_color_image,shoes_color,shoes WHERE cart.id_cart=cart_detail.id_cart AND shoes_color_image.id_shoes_color=cart_detail.id_color AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes.id_shoes=cart_detail.id_shoes AND cart.id_user =%s GROUP BY cart_detail.id_cart_detail",[id_account])
            temp=cur.fetchall()
            return render_template('user_cart.html',cart_detail=temp,recommended=recommended)
        return redirect(url_for('user_login'))
    return redirect(url_for('user_login'))


@app.route('/add_to_cart', methods= ['GET','POST'] )
def add_to_cart():
    if 'id' in session:
        if session['role']==2:
            if request.method == 'POST':
                print("Av")
                id_account =session['id']
                print(request.form)
                id_shoes_color=request.form['color']
                size=request.form['size']
                quantity=request.form['quantity']
                cur =mysql.connection.cursor()
                cur.execute("SELECT * FROM shoes_color,shoes_color_image,shoes WHERE shoes.id_shoes= shoes_color.id_shoes AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes_color.id_shoes_color =%s GROUP BY shoes_color.id_shoes_color",[id_shoes_color])
                rows =cur.fetchall()
                id_shoes =rows[0]['id_shoes']
                price_per_product = round( rows[0]['price']*(1-rows[0]['sale']/100))

                # cart exist ?

                cur =mysql.connection.cursor()
                cur.execute("SELECT * FROM cart WHERE id_user=%s",[id_account])
                cart =cur.fetchall()
                if len(cart)==0 :
                    # add cart if not exist
                    print("aaaa")
                    cur.execute("INSERT INTO cart(id_cart,id_user,cart_quantity,cart_total_price) VALUES(%s,%s,%s,%s)",["NULL",id_account,"1","0"])
                    mysql.connection.commit()

                # query id_cart
                cur.execute("SELECT id_cart FROM cart WHERE id_user = %s",[id_account])
                temp = cur.fetchall()
                id_cart = temp[0]['id_cart']
                # add product
                cur.execute("INSERT INTO cart_detail(id_cart_detail,id_shoes,id_color,size,id_cart,quantity,price_per_product) VALUES(%s,%s,%s,%s,%s,%s,%s)",["NULL",id_shoes,id_shoes_color,size,id_cart,quantity,price_per_product])
                mysql.connection.commit()



                cur.execute("SELECT * FROM `cart_detail` WHERE id_cart=%s",[id_cart])
                temp2= cur.fetchall()
                total_price=0
                total_sp=0
                for item in temp2:
                    total_price+=item['price_per_product']*item['quantity']
                    total_sp+=item['quantity']
                cur.execute("UPDATE cart SET cart_quantity=%s,cart_total_price=%s WHERE id_cart=%s",[total_sp,total_price,id_cart])
                mysql.connection.commit()
                return redirect(url_for("user_cart"))
            return redirect(url_for("user_cart"))
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@app.route('/user_cart/delete/<id_cart_detail>')
def delete_cart_detail(id_cart_detail):
    if 'id' in session:
        cur=mysql.connection.cursor()
        cur.execute("SELECT id_cart FROM cart_detail WHERE id_cart_detail =%s",[id_cart_detail])
        rows=cur.fetchall()
        id_cart=rows[0]['id_cart']
        cur.execute("DELETE FROM cart_detail WHERE id_cart_detail=%s",[id_cart_detail])
        mysql.connection.commit()
        update_cart(id_cart)
    
        return redirect(url_for("user_cart"))
    return redirect(url_for('user_index'))

def update_cart(id_cart):
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM cart_detail WHERE id_cart=%s",[id_cart])
    temp2= cur.fetchall()
    total_price=0
    total_sp=0
    for item in temp2:
        total_price+=item['price_per_product']*item['quantity']
        total_sp+=item['quantity']
    cur.execute("UPDATE cart SET cart_quantity=%s,cart_total_price=%s WHERE id_cart=%s",[total_sp,total_price,id_cart])
    mysql.connection.commit()

@app.route('/user_update/cart',methods= ['GET','POST'])
def update_usercart():
    if 'id' in session:
        if request.method=='POST':
            number=request.form['number']
            id_cart_detail =request.form['id_cart_detail']
            cur=mysql.connection.cursor()
            cur.execute('UPDATE cart_detail SET quantity= %s  WHERE id_cart_detail=%s',[number,id_cart_detail])
            mysql.connection.commit()
            cur.execute("SELECT id_cart FROM cart_detail WHERE id_cart_detail =%s",[id_cart_detail])
            temp=cur.fetchall()
            id_cart=temp[0]['id_cart']
            update_cart(id_cart)
            # return "1"
            cur.execute("SELECT * FROM cart WHERE id_cart=%s",[id_cart])
            # cur.execute("SELECT * FROM cart_detail WHERE id_cart_detail=%s",[id_cart_detail])
            temp2=cur.fetchall()
            total_price = temp2[0]['cart_total_price']
            resp="<td></td><td></td><td><h5>Subtotal</h5></td> <td><h5>"+str(total_price)+"<ins>đ</ins></h5></td><td></td>"
            
            cur.execute("SELECT * FROM cart_detail,shoes WHERE shoes.id_shoes=cart_detail.id_shoes AND id_cart_detail=%s",[id_cart_detail])
            temp3=cur.fetchall()
            factor = temp3[0]['quantity']*(temp3[0]['price']*(1-temp3[0]['sale']/100))
            resp2= "<h5>"+str(factor)+"<ins>đ</ins></h5>"
            return json.dumps({"resp1":resp,"resp2":resp2})
        return redirect(url_for('user_cart'))
    return redirect(url_for('user_login'))

@app.route('/user_cart/checkout',methods=['POST','GET'])
def checkout():
    if 'id' in session:
        if request.method== 'POST':
            print('ahihi')
            name= request.form['receiver']
            address_order =request.form['address_ship']
            phone=request.form['phone_number']


            id_user=session['id']
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM cart,cart_detail WHERE cart.id_cart=cart_detail.id_cart AND cart.id_user=%s",[id_user])
            rows=cur.fetchall()
            total_price = rows[0]['cart_total_price']
            order_quantity =rows[0]['cart_quantity']
            time_order=datetime.datetime.now()
            print(time_order)
            cur.execute ("INSERT INTO user_order(id_order,id_user,order_quantity,total_price,time_order) VALUES(%s,%s,%s,%s,%s)",["NULL",id_user,order_quantity,total_price,time_order])
            mysql.connection.commit()
            cur.execute ("SELECT * FROM user_order WHERE id_user=%s ORDER BY time_order DESC LIMIT 1",[id_user])
            temp=cur.fetchall()
            id_user_order = temp[0]['id_order']

            for item_cart in rows:
                id_shoes = item_cart['id_shoes']
                id_shoes_color =item_cart['id_color']
                order_size =item_cart['size']
                order_detail_quantity=item_cart['quantity']
                price_per_order=item_cart['price_per_product']
                cur.execute("INSERT INTO order_detail(id_order_detail,id_shoes,id_shoes_color,order_detail_quantity,order_size,id_order,price_per_order) VALUES(%s,%s,%s,%s,%s,%s,%s)",["NULL",id_shoes,id_shoes_color,order_detail_quantity,order_size,id_user_order,price_per_order])
                mysql.connection.commit()

                ## send recombee
                client.send(AddPurchase(id_user,id_shoes,cascade_create=True))

            
            cur.execute("DELETE FROM cart_detail WHERE id_cart=(SELECT cart.id_cart FROM cart WHERE cart.id_user=%s)",[id_user])
            mysql.connection.commit()
            cur.execute("DELETE FROM cart WHERE id_user=%s",[id_user])
            mysql.connection.commit()

            cur.execute("INSERT INTO ship(id_ship,id_order,address_order,phone,name,status) VALUES(%s,%s,%s,%s,%s,%s)",["NULL",id_user_order,address_order,phone,name,"Giao Hàng"])
            mysql.connection.commit()

            cur.execute("SELECT * FROM user_order WHERE user_order.id_user=%s ORDER BY user_order.id_order DESC LIMIT 1",[id_user])
            done=cur.fetchall()
            id_new_order= done[0]['id_order']
            print(id_new_order)
            flash("Your order is complete! Your id_order is: ",id_new_order)

            return redirect(url_for('user_cart'))
        return redirect(url_for('user_cart'))
    return redirect(url_for('user_login')) 

@app.route('/user_profile')
def user_profile():
    if 'id' in session:
        id_account = session['id']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE id_account =%s" ,[id_account])
        rows=cur.fetchall()
        return render_template('user_profile.html',person=rows)
    return redirect(url_for('user_login'))

@app.route('/user_update_infor', methods= ['GET','POST'])
def update_person_infor():
    if 'id' in session:
        if request.method == 'POST':
            id_account = session['id']
            username= request.form['username']
            phone_number =request.form['phone_number']
            address=request.form['address']
            cur=mysql.connection.cursor()
            cur.execute("UPDATE account SET username=%s,phone_number=%s,address=%s WHERE id_account=%s",[username,phone_number,address,id_account])
            mysql.connection.commit()
            flash("Complete")
            return redirect(url_for('user_profile'))
        return redirect(url_for('user_login'))
    return redirect(url_for('user_login'))

@app.route('/personal_infor/upload_image',methods=['GET','POST'])
def upload():
    if 'id' in session:
        if request.method =='POST':
            # print("ahihi")
            # file = request.form['img']
            # print("ahihi1")
            # f = request.files['image']
            # f.save(f.filename)
            # print("ahihi3")
                # filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile = request.files['image']
            profile.save(os.path.join(uploads_dir_account, secure_filename(profile.filename)))
            link="/static/image/people/"+profile.filename
            id_account =session['id']
            cur=mysql.connection.cursor()
            cur.execute("UPDATE account SET cover_image=%s WHERE id_account=%s",[link,id_account])
            mysql.connection.commit()


            # save each "charts" file
            # for file in request.files.getlist('charts'):
            #     file.save(os.path.join(uploads_dir, secure_filename(file.name)))
            return redirect(url_for('user_profile'))
        return redirect(url_for('user_profile'))
    return redirect(url_for('user_login'))

@app.route('/user_history_order')
def user_history():
    if 'id' in session:
        if session['role']==2:
            id_account = session['id']
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM account WHERE id_account =%s" ,[id_account])
            rows=cur.fetchall()

            # cur = mysql.connection.cursor()
            # cur.execute("SELECT * FROM shoes")
            # abc=cur.fetchall()

            id_user = session['id']
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM user_order,ship WHERE user_order.id_order=ship.id_order AND user_order.id_user =%s",[id_user])
            rows=cur.fetchall()

            cur.execute("SELECT * FROM user_order,order_detail,shoes,shoes_color_image WHERE user_order.id_order= order_detail.id_order AND shoes.id_shoes=order_detail.id_shoes AND shoes_color_image.id_shoes_color=order_detail.id_shoes_color AND user_order.id_user =%s GROUP BY order_detail.id_order_detail",[id_user])
            detail=cur.fetchall()

            return render_template('user_historyorder.html',order_history=rows,order_detail=detail,person=rows)
        return redirect(url_for('user_login'))
    return redirect(url_for('user_login'))



@app.route('/reset', methods=["GET", "POST"])
def reset():
    # form = EmailForm()
    if request.method=='POST':
        # user = User.query.filter_by(email=form.email.data).first_or_404()
        email=request.form['email']
        # print('Email:'+email)
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE email=%s",[email])
        rows=cur.fetchall()
        if len(rows) ==0:
            return "Email not exist or hasn't use !"
        else:
            subject = "Password reset requested"

            # Here we use the URLSafeTimedSerializer we created in `util` at the
            # beginning of the chapter
            s = URLSafeSerializer(app.config['SECRET_KEY'])
            # s = URLSafeSerializer('super-secret-key')
            token =s.dumps(email, salt='recover-key')
            # token = "1232312sdgs4124"
            print('Token:')
            print(token)

            recover_url = url_for(
                'reset_with_token',
                token=token,
                _external=True)

            html = render_template(
                'recover.html',
                recover_url=recover_url)

            # Let's assume that send_email was defined in myapp/util.py
            send_email(subject,[email],html)

            return "Access Email to confirm !"
    return render_template('reset.html', form=form)


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    # try:
        s = URLSafeSerializer(app.config['SECRET_KEY'])
        email = s.loads(token, salt="recover-key")
       

        if request.method=='POST':
            
            password=request.form['password']
            cur=mysql.connection.cursor()
            cur.execute("UPDATE account SET password=%s WHERE email =%s ",[password,email])
            mysql.connection.commit()
            print('Xong')

            return redirect(url_for('user_login'))

        return render_template('reset_with_token.html',  token=token,email=email)

def send_email(message,recei,body):
	# try:
		msg = Message(message,
		  sender="seeyouagain791142@gmail.com",
		  recipients=recei)
		msg.body = body           
		mail.send(msg)
		return 'Mail sent!'
        

@app.route('/tracking',  methods=["GET", "POST"])
def tracking():
    if request.method=='POST':
        id_user=request.form['id_user']
        id_shoes=request.form['id_shoes']
        a={'id_user':id_user,'id_shoes':id_shoes}

        # print(id_shoes)
        # with open('./log.json') as data_file:    
        #     data = json.load(data_file)
        #     # data.append()
        # data.append(a)
        # with open('log.json', 'w') as f:
        #     json.dump(data, f)
        #     f.close()
        # print(data)

    #     return "done"
        # time=datetime.datetime.today(),
        # client.send(AddDetailView(id_user, id_shoes, cascade_create=True))
        return "done"


@app.route('/add_to_cart/tracking',  methods=["GET", "POST"])
def add_to_cart_tracking():
    if request.method=='POST':
        id_user=request.form['id_user']
        id_shoes=request.form['id_shoes']
        a={'id_user':id_user,'id_shoes':id_shoes}
        print(id_shoes)
        with open('./add_to_cart.json') as data_file:    
            data = json.load(data_file)
            # data.append()
        data.append(a)
        with open('add_to_cart.json', 'w') as f:
            json.dump(data, f)
            f.close()
        print(data)
    #     return "done"
        # time=datetime.datetime.today(),
        client.send(AddCartAddition(id_user, id_shoes, cascade_create=True))
        return "done"


@app.route('/comments/tracking/<id_shoes>',  methods=["GET", "POST"])
def comments_tracking(id_shoes):
    print("123")
    if request.method=='POST':
        print('comment_tracking')
        # id_user=request.form['id_user']
        # id_shoes=request.form['id_shoes']
        id_user=session['id']
        # id_shoes=id_shoes
        rate=(int(request.form['rate'])-3)/2
        a={'id_user':id_user,'id_shoes':int(id_shoes),'rating':rate}
        print(id_shoes)
        with open('./comments.json') as data_file:    
            data = json.load(data_file)
            # data.append()
        data.append(a)
        with open('comments.json', 'w') as f:
            json.dump(data, f)
            f.close()
        print(data)
    #     return "done"
        # time=datetime.datetime.today(),
        client.send(AddRating(id_user, id_shoes,rate, cascade_create=True))
        return "done"




@app.route('/update_data')
def update_data_server():

    cur=mysql.connection.cursor()

    # cur.execute("SELECT * FROM shoes")
    # temp=cur.fetchall()
    
    
    # for item in temp:
    #     print(item['id_shoes'])
    #     client.send(SetItemValues(item['id_shoes'],item,cascade_create=True))
        # print(item)

    # print(json_data)
    cur.execute("SELECT * FROM account WHERE role='2'")
    account= cur.fetchall()
    for ac in account:
        client.send(SetUserValues(ac['id_account'],{'address':ac['address'],'id_account':ac['id_account']},cascade_create=True))
    return "Store user complete !"
@app.route('/update_item')
def update_item():
    cur=mysql.connection.cursor()

    cur.execute("SELECT shoes.id_shoes,shoes_name,gender_shoes,shoes_type,feature,price,athleter,sale,catalogy,shoes.describe,image,GROUP_CONCAT(DISTINCT surface SEPARATOR ',') as surface,GROUP_CONCAT(DISTINCT color SEPARATOR ',') as color FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes AND shoes.id_shoes=shoes_color.id_shoes and shoes_color.id_shoes_color=shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes")
    temp=cur.fetchall()
    
    
    for item in temp:
        print(item['id_shoes'])
        current_item={
            "id_shoes":item['id_shoes'],
            "shoes_name":item['shoes_name'],
            "gender_shoes":item['gender_shoes'],
            "shoes_type":item['shoes_type'],
            "feature":item['feature'],
            "price":item['price'],
            "athleter":item['athleter'],
            "sale":item['sale'],
            "catalogy":item['catalogy'],
            "describe":item['describe'],
            "image":"/static/image/shoes_image/"+item['image'],
            "surface":[item['surface']],
            "color":[item['color']]
        }
        client.send(SetItemValues(item['id_shoes'],current_item,cascade_create=True))
    return "Update item complete !"

def update_item_id(id_shoes):
    cur=mysql.connection.cursor()
    cur.execute("SELECT shoes.id_shoes,shoes_name,gender_shoes,shoes_type,feature,price,athleter,sale,catalogy,shoes.describe,image,GROUP_CONCAT(DISTINCT surface SEPARATOR ',') as surface,GROUP_CONCAT(DISTINCT color SEPARATOR ',') as color FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes AND shoes.id_shoes=shoes_color.id_shoes and shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes.id_shoes=%s GROUP BY shoes.id_shoes",[id_shoes])
    temp=cur.fetchall()
    
    
    for item in temp:
        # print(item['id_shoes'])
        current_item={
            "id_shoes":item['id_shoes'],
            "shoes_name":item['shoes_name'],
            "gender_shoes":item['gender_shoes'],
            "shoes_type":item['shoes_type'],
            "feature":item['feature'],
            "price":item['price'],
            "athleter":item['athleter'],
            "sale":item['sale'],
            "catalogy":item['catalogy'],
            "describe":item['describe'],
            "image":"/static/image/shoes_image/"+item['image'],
            "surface":[item['surface']],
            "color":[item['color']]
        }
        client.send(SetItemValues(item['id_shoes'],current_item,cascade_create=True))
    return "Update item "+temp[0]['shoes_name'] +" complete !"


@app.route('/getdata_recomendation')
def getdata_recomendation(id_shoes):
    return update_item_id(id_shoes)
    # 1: id_item,3:id_account,2 is number get_recommend
    # recommended = client.send(RecommendItemsToItem('1', '3', 2,
    #                                            scenario='product_detail',
    #                                            return_properties=True,
    #                                            cascade_create=True))
    # print(recommended)
    # return "1"



@app.route('/page_view/com.snowplowanalytics.snowplow/tp2',methods=["GET", "POST"])
def ahihidongoc():
    if request.method=='POST':
        temp=request.data.decode("utf-8")
        data=json.loads(temp)
        
        print(type(data))
        # print(data)
        link= data['data'][0]['co']
        # print(link)
        data2=json.loads(link)
        print(data2['data'][1])
        id_user=int(data2['data'][1]['id_user'])
        id_shoes=int(data2['data'][1]['id_shoes'])
        print(id_user)
        
        a={'id_user':id_user,'id_shoes':id_shoes}
        # print(id_shoes)
        with open('./log.json') as data_file:    
            n_data = json.load(data_file)
            # data.append()
        n_data.append(a)
        with open('log.json', 'w') as f:
            json.dump(n_data, f)
            f.close()
        print(n_data)
    #     return "done"
        # time=datetime.datetime.today(),
        client.send(AddDetailView(id_user, id_shoes, cascade_create=True))
    return "1"

@app.route('/addtocart/com.snowplowanalytics.snowplow/tp2',methods=["GET", "POST"])
def addtocart_tracking():
    if request.method=='POST':
        print(request.data)
        temp=request.data.decode("utf-8")
        data=json.loads(temp)

        link=data['data'][0]['co']
        
        # print(link)
        
        data2=json.loads(link)
        id_user=int(data2['data'][1]['id_user'])
        id_shoes=int(data2['data'][1]['id_shoes'])
        print(id_shoes)
        a={'id_user':id_user,'id_shoes':id_shoes}
        print(id_shoes)

        # with open('./add_to_cart.json') as data_file:    
        #     n_data = json.load(data_file)
        #     # data.append()
        # n_data.append(a)
        # with open('add_to_cart.json', 'w') as f:
        #     json.dump(n_data, f)
        #     f.close()
        # print(n_data)
    
        # client.send(AddCartAddition(id_user, id_shoes, cascade_create=True))
      
    return "1"


@app.route('/rating/com.snowplowanalytics.snowplow/tp2',methods=["GET", "POST"])
def rating_tracking():
    if request.method=='POST':
        print(request.data)
        temp=request.data.decode("utf-8")
        data=json.loads(temp)

        link=data['data'][0]['co']
        
        # print(link)
        
        data2=json.loads(link)
        id_user=int(data2['data'][1]['id_user'])
        id_shoes=int(data2['data'][1]['id_shoes'])
        rating = (int(data2['data'][1]['rating'])-3)/2
        print(id_shoes)
        a={'id_user':id_user,'id_shoes':id_shoes,'rating':rating}
        print(rating)

        # with open('././comments.json') as data_file:    
        #     n_data = json.load(data_file)
        #     # data.append()
        # n_data.append(a)
        # with open('./comments.json', 'w') as f:
        #     json.dump(n_data, f)
        #     f.close()
        # print(n_data)
    
        # client.send(AddCartAddition(id_user, id_shoes, cascade_create=True))
      
    return "1"

@app.route('/purchase/com.snowplowanalytics.snowplow/tp2',methods=["GET", "POST"])
def purchase_tracking():
    if request.method=='POST':
        print(request.data)
        temp=request.data.decode("utf-8")
        data=json.loads(temp)

        link=data['data'][0]['co']
        
        print(link)
        
        data2=json.loads(link)
        id_user=data2['data'][1]['id_user']
        print(id_user)
      
    return "1"