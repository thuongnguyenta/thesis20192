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
# app.config['UPLOAD_FOLDER'] ="./static/image/people"
uploads_dir = './static/image/people'

# os.makedirs(uploads_dir, exists_ok=True)

mysql = MySQL(app)

# dropzone = Dropzone(app)
# # Dropzone settings
# app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
# app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
# app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
# app.config['DROPZONE_REDIRECT_VIEW'] = 'results'
# # Uploads settings
# app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/image/people'
# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)
# patch_request_class(app)  # set maximum file size, default is 16MB

@app.route('/')
def db():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_color.id_shoes AND shoes_color_image.id_shoes_color=shoes_color.id_shoes_color GROUP BY shoes.id_shoes LIMIT 10")
    rows=cur.fetchall()
    return render_template('dashboard.html',shoes=rows)
@app.route('/index')
def dashboard():

    a=[]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes")
    rows= cur.fetchall()

    cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color GROUP BY shoes_color.id_shoes_color")
    color =cur.fetchall()    

    cur.execute("SELECT * FROM shoes,shoes_surface WHERE shoes.id_shoes=shoes_surface.id_shoes")
    surface=cur.fetchall()
    
    cur.execute("SELECT shoes_type,COUNT(*) as number FROM `shoes` GROUP BY shoes_type")
    shoe_type = cur.fetchall()


    return render_template('index.html',shoes=rows, shoes_color=color, shoe_type=shoe_type,surface=surface,a=a)
def content():
    a=[]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes")
    rows= cur.fetchall()

    cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color GROUP BY shoes_color.id_shoes_color")
    color =cur.fetchall()    

    cur.execute("SELECT shoes_type,COUNT(*) as number FROM `shoes` GROUP BY shoes_type")
    shoe_type = cur.fetchall()
    return [rows,color,shoe_type,a]
    
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
            profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))
            link="/static/image/people/"+profile.filename
            id_account =session['id']
            cur=mysql.connection.cursor()
            cur.execute("UPDATE account SET cover_image=%s WHERE id_account=%s",[link,id_account])
            mysql.connection.commit()


            # save each "charts" file
            # for file in request.files.getlist('charts'):
            #     file.save(os.path.join(uploads_dir, secure_filename(file.name)))
            return redirect(url_for('personal_infor'))
        return redirect(url_for('personal_infor'))
    return redirect(url_for('dashboard'))


@app.route('/shoes/<type_s>')
def shoes_type(type_s):

    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_surface,shoes_color,shoes_color_image WHERE shoes.id_shoes=shoes_surface.id_shoes_surface AND shoes.id_shoes=shoes_color.id_shoes AND shoes_color.id_shoes_color= shoes_color_image.id_shoes_color GROUP BY shoes.id_shoes AND shoes.shoes_type= %s",[type_s])
    rows=cur.fetchall()
    cur.execute("SELECT * FROM shoes,shoes_surface WHERE shoes.id_shoes=shoes_surface.id_shoes")
    surface=cur.fetchall()

    [temp,shoes_color,shoe_type,a]=content()
    return render_template('index.html',shoes=rows, shoes_color=shoes_color, shoe_type=shoe_type,surface=surface,a=a,type_shoes=type_s)


@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        cur=mysql.connection.cursor()
        search_in4 = request.form['searchbar']
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

        return render_template('index.html',shoes=rows, shoes_color=color, shoe_type=shoe_type,surface=surface,a=a,search=search_in4)

@app.route('/shoes_detail/<id_shoes>')
def shoe_detail(id_shoes):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shoes,shoes_color_image,shoes_color WHERE shoes.id_shoes=shoes_color.id_shoes and shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes.id_shoes=%s ORDER BY shoes_color.id_shoes_color",[id_shoes])
    shoe= cur.fetchall()

    cur.execute("SELECT * FROM shoes,shoes_color_image,shoes_color WHERE shoes.id_shoes=shoes_color.id_shoes and shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes.id_shoes=%s GROUP BY shoes_color.id_shoes_color ORDER BY shoes_color.id_shoes_color",[id_shoes])
    color=cur.fetchall()
    
    cur.execute("SELECT * FROM comment,account WHERE comment.id_user=account.id_account AND id_shoes=%s",[id_shoes])
    comment=cur.fetchall()

    cur.execute("SELECT AVG(star) as St,count(*) as numb FROM comment WHERE id_shoes=%s GROUP BY id_shoes",[id_shoes])
    star=cur.fetchall()


    return render_template("shoes_detail.html",shoe_detail=shoe,color=color,comment=comment,star=star)

@app.route('/shoes_detail/comment/<id_shoes>', methods=['GET','POST'])
def comment(id_shoes):
    if 'id' in session:
        if request.method == 'POST':
            id_user=session['id']
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM user_order,order_detail WHERE user_order.id_order=order_detail.id_order AND user_order.id_user=%s AND order_detail.id_shoes=%s",[id_user,id_shoes])
            temp=cur.fetchall()
            if temp:
                star=request.form['rate']
                comment=request.form['comment']
                cur_time=datetime.datetime.now()
                
                cur.execute("INSERT INTO comment(id_comment,id_user,id_shoes,star,comments,time_review) VALUES(%s,%s,%s,%s,%s,%s)",["NULL",id_user,id_shoes,star,comment,cur_time])
                mysql.connection.commit()
                return redirect(url_for('shoe_detail',id_shoes=id_shoes))
            else :
                flash("You haven't purchase product to review !")
                return redirect(url_for("shoe_detail",id_shoes=id_shoes))
    else:
        flash('You are not login !')
        return redirect(url_for('shoe_detail',id_shoes=id_shoes))

@app.route('/login',methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE email=%s AND password=%s",(email,password))
        rows = cur.fetchall()
        if len(rows) ==0:
            error="Sai tai khoan hoac mat khau"
            [shoes, shoes_color, shoe_type,a] = content()
            return render_template('index.html',shoes=shoes,shoes_color=shoes_color,shoe_type=shoe_type,a=a,error=error)
        else:
            session['id'] = rows[0]['id_account']
            session['name'] = rows[0]['username']
            session["email"] =rows[0]['email']
            session['role'] =rows[0]['role']
            session['address']=rows[0]['address']
            session['phone_number']=rows[0]['phone_number']
            session['cover_image']=rows[0]['cover_image']
            return redirect(url_for('dashboard'))

@app.route('/user_check', methods=['POST'])
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
	

@app.route('/register',methods=['GET','POST'])
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
        login()
        return redirect(url_for('dashboard'))
    return  redirect(url_for('dashboard'))
        

@app.route('/add_to_cart', methods= ['GET','POST'] )
def add_to_cart():
    if 'id' in session:
        if request.method == 'POST':
            print("Av")
            id_account =session['id']
        
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
            return redirect(url_for("cart_infor"))
        return redirect(url_for("cart_infor"))
    return redirect(url_for('dashboard'))
            

    
    # return redirect(url_for('dashboard'))




@app.route('/cart_detail')
def cart_infor():
    if 'id' in session:
        id_account = session['id']
        cur =mysql.connection.cursor()
        cur.execute("SELECT * FROM cart,cart_detail,shoes_color_image,shoes_color,shoes WHERE cart.id_cart=cart_detail.id_cart AND shoes_color_image.id_shoes_color=cart_detail.id_color AND shoes_color.id_shoes_color=shoes_color_image.id_shoes_color AND shoes.id_shoes=cart_detail.id_shoes AND cart.id_user =%s GROUP BY cart_detail.id_cart_detail",[id_account])
        rows = cur.fetchall()
        return render_template("cart_detail.html",cart_detail=rows)
    return redirect(url_for('dashboard'))



@app.route('/cart_detail/delete/<id_cart_detail>')
def delete_cart_detail(id_cart_detail):
    if 'id' in session:
        cur=mysql.connection.cursor()
        cur.execute("SELECT id_cart FROM cart_detail WHERE id_cart_detail =%s",[id_cart_detail])
        rows=cur.fetchall()
        id_cart=rows[0]['id_cart']
        cur.execute("DELETE FROM cart_detail WHERE id_cart_detail=%s",[id_cart_detail])
        mysql.connection.commit()
        update_cart(id_cart)
    
        return redirect(url_for("cart_infor"))
    return redirect(url_for('dashboard'))

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

@app.route('/personal_infor')
def personal_infor():
    if 'id' in session:
        id_account = session['id']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM account WHERE id_account =%s" ,[id_account])
        rows=cur.fetchall()
        return render_template('person_infor.html',person=rows)
    
@app.route('/update_person_infor', methods= ['GET','POST'])
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
            return redirect(url_for('personal_infor'))
    
        
@app.route('/history_order')
def history_order():
    if 'id' in session:
        id_user = session['id']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM user_order,ship WHERE user_order.id_order=ship.id_order AND user_order.id_user =%s",[id_user])
        rows=cur.fetchall()

        cur.execute("SELECT * FROM user_order,order_detail,shoes,shoes_color_image WHERE user_order.id_order= order_detail.id_order AND shoes.id_shoes=order_detail.id_shoes AND shoes_color_image.id_shoes_color=order_detail.id_shoes_color AND user_order.id_user =%s GROUP BY order_detail.id_order_detail",[id_user])
        detail=cur.fetchall()
        return render_template('history_order.html',order_history=rows,details=detail)
    return redirect(url_for('dashboard'))

@app.route('/cart_detail/checkout',methods=['POST','GET'])
def checkout():
    if 'id' in session:
        if request.method== 'POST':
            print('ahihi')
            name= request.form['name']
            address_order =request.form['address']
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

            return redirect(url_for('history_order'))
        return redirect(url_for('cart_infor'))
    return redirect(url_for('dashboard')) 


@app.route('/logout')
def logout():
    session.clear()
    # session.pop('id',None)
    # session.pop('role',None)
    return redirect(url_for('dashboard'))



