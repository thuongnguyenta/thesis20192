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

uploads_dir = './static/image/shoes_image/'

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
    
@app.route('/customer')
def customer(): 
    # if 'id' in session:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE role=2 ")
        user=cur.fetchall()
        # cur.execute("SELECT * FROM user_order,order_detail,shoes,shoes_color_image WHERE user_order.id_order= order_detail.id_order AND shoes.id_shoes=order_detail.id_shoes AND shoes_color_image.id_shoes_color=order_detail.id_shoes_color GROUP BY order_detail.id_order_detail")
        # order_detail=cur.fetchall()
        return render_template('customer.html',user=user)


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

@app.route('/dashboard/comment',methods=['POST'])
def comment_ap():
    print("1")
    if request.method=='POST':
        print("2")
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
            div3="<div class='mail-contnet'><h5>"+cm['username']+"</h5><span class='time'>"+cm['time_review'].strftime("%H:%M %D,%B %Y")+"</span><br/><span class='mail-desc' >"+cm['comments']+"</span> <div id='comment_"+str(cm['id_comment'])+"' class='btn btn btn-rounded btn-default btn-outline m-r-5 approve'><i class='ti-check text-success m-r-5'></i>Approve</div><div href='javacript:void(0)' class='btn-rounded btn btn-default btn-outline'><i class='ti-close text-danger m-r-5'></i> Reject</div></div>"
            div4="<div class='name_product'>"+cm['shoes_name']+"</div>"
            div5="<div class='star' id='"+str(cm['star'])+"'>"
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
            reps+="<input type='checkbox' name='color_image' value='"+str(pr['id_shoes_color_image'])+"' id='id_color_image_"+str(pr['id_shoes_color_image'])+"'><label for='id_color_image_"+str(pr['id_shoes_color_image'])+"'><img src='./static/image/shoes_image/"+pr['image']+"' width='50px' height='50px'></label>"
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
            resp+="<input type='checkbox' name='color_image' value='"+str(pr['id_shoes_color_image'])+"' id='id_color_image_"+str(pr['id_shoes_color_image'])+"'><label for='id_color_image_"+str(pr['id_shoes_color_image'])+"'><img src='./static/image/shoes_image/"+pr['image']+"' width='50px' height='50px'></label>"
        print (resp)
        return resp


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

        shoes_image = request.files['file']
        path_save=uploads_dir+str(id_shoes)+"/"+str(shoes_color)+"/"
        if not os.path.exists(path_save): 
            os.makedirs(path_save)
        shoes_image.save(os.path.join(path_save, secure_filename(shoes_image.filename)))
        
        link=str(id_shoes)+"/"+str(shoes_color)+"/"+shoes_image.filename
        # print("4")
        print(path_save,link)
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM shoes,shoes_color WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes.id_shoes=%s AND shoes_color.color=%s",[id_shoes,shoes_color])
        temp=cur.fetchall()
        id_shoes_color = temp[0]['id_shoes_color']
        cur.execute("INSERT INTO shoes_color_image(id_shoes_color_image,id_shoes_color,image) VALUES(%s,%s,%s)",["NULL",id_shoes_color,link])
        mysql.connection.commit()
        # print(shoes_delete,shoes_image)
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
