import os
from flask_session import Session
from flask import Flask, request, render_template, session
import sqlite3
from werkzeug.utils import redirect, secure_filename



connection = sqlite3.connect("onestop.db", check_same_thread=False)
table1 = connection.execute("select * from sqlite_master where type = 'table' and name = 'SELLER'").fetchall()
table2 = connection.execute("select * from sqlite_master where type = 'table' and name = 'USER'").fetchall()
table3 = connection.execute("select * from sqlite_master where type = 'table' and name = 'PRODUCT'").fetchall()
table4 = connection.execute("select * from sqlite_master where type = 'table' and name = 'CART'").fetchall()
table5 = connection.execute("select * from sqlite_master where type = 'table' and name = 'BUY'").fetchall()
if table1 !=[]:
    print("Seller table already exits")
else:
    connection.execute('''CREATE TABLE SELLER(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                SELLER_NAME TEXT,
                                SELLER_EMAIL TEXT,
                                SELLER_PASSWORD TEXT,
                                SELLER_NUMBER INTEGER,
                                SELLER_ACC INTEGER,
                                SELLER_IFSC TEXT
);''')
    print("Seller Table created")
if table2!=[]:
    print("Customer table exists")
else:
    connection.execute('''CREATE TABLE USER(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                CUST_NAME TEXT,
                                CUST_EMAIL TEXT,
                                CUST_GENDER TEXT,
                                CUST_AGE INTEGER,
                                CUST_NUMBER INTEGER,
                                CUST_ADDRESS TEXT,
                                CUST_PASSWORD TEXT
                                );''')
    print("Customer Table created ")
if table3!=[]:
    print("Product table exists")
else:
    connection.execute('''CREATE TABLE PRODUCT(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                CATEGORY TEXT,
                                NAME TEXT,
                                PRICE INTEGER,
                                FEATURE TEXT,
                                IMAGE BLOB,
                                SELLER_ID TEXT); ''')
    print("Product table created")

if table4 !=[]:
    print("Seller table already exits")
else:
    connection.execute('''CREATE TABLE CART(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                PRODUCT_ID INTEGER,
                                USER_ID TEXT
);''')

if table5 != []:
    print("Buy table already exits")
else:
    connection.execute('''CREATE TABLE BUY(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                PRODUCT_ID INTEGER,
                                USER_ID TEXT);''')
    print("Buy table created")


application = Flask(__name__)
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)

application.config['UPLOAD_FOLDER'] = "static\images"

@application.route("/userreg", methods=["GET", "POST"])
def User_register():
    if request.method == "POST":
        getName = request.form["name"]
        getEmail = request.form["email"]
        getGender = request.form.get('gen')
        getAge = request.form["age"]
        getNumber = request.form["pno"]
        getAddress = request.form["add"]
        getPass = request.form["pass"]
        cursor = connection.cursor()
        query = "SELECT * FROM USER WHERE CUST_EMAIL='" + getEmail + "'"
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            return render_template("userregister.html", status=True)
        else:
            cursor.execute("INSERT INTO USER(CUST_NAME,CUST_EMAIL,CUST_GENDER,CUST_AGE,CUST_NUMBER,CUST_ADDRESS,CUST_PASSWORD)\
                            VALUES('"+getName+"','"+getEmail+"','"+getGender+"',"+getAge+","+getNumber+",\
                            '"+getAddress+"','"+getPass+"')")
            cursor.connection.commit()
            print("Customer details inserted successfully")
            return redirect('/')
    else:
        return render_template("userregister.html", status=False)




@application.route("/", methods=["GET", "POST"])
def User_login():
    global Uid,getuName
    if request.method == "POST":
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        cursor = connection.cursor()
        query = "SELECT * FROM USER WHERE CUST_EMAIL='"+getEmail+"' and CUST_PASSWORD='"+getPass+"' "
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            for i in result:
                getuName = i[1]
                getuId = i[0]
                session["name"] = getuName
                session["id"] = getuId
                Uid = str(session["id"])
            print("password correct")
            return redirect('/dashboard')
        else:
            return render_template("userlogin.html", status=True)
    else:
        return render_template("userlogin.html", status=False)

@application.route("/sellerregister", methods=['GET', 'POST'])
def Seller_register():
    if request.method == "POST":
        getName = request.form["name"]
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        getNumber = request.form["pno"]
        getAcc = request.form["ano"]
        getIfsc = request.form["ifsc"]
        cursor = connection.cursor()
        query = "SELECT * FROM SELLER WHERE SELLER_EMAIL='" + getEmail + "'"
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            return render_template("seller_register.html", status=True)
        else:
            cursor.execute("INSERT INTO SELLER(SELLER_NAME,SELLER_EMAIL,SELLER_PASSWORD,SELLER_NUMBER,SELLER_ACC,SELLER_IFSC)\
                                       VALUES('" + getName + "','" + getEmail + "','" + getPass + "'," + getNumber + "," + getAcc + ",'" + getIfsc + "')")
            cursor.connection.commit()
            print("Seller details inserted successfully")
            return redirect('/sellerlogin')
    else:
        return render_template("seller_register.html", status=False)

@application.route("/sellerlogin", methods=['GET', 'POST'])
def Seller_Login():
    global id
    if request.method == "POST":
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        cursor = connection.cursor()
        query = "SELECT * FROM SELLER WHERE SELLER_EMAIL='"+getEmail+"' AND SELLER_PASSWORD='"+getPass+"'"
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            for i in result:
                getsName = i[1]
                getsId = i[0]
                session["name"] = getsName
                session["id"] = getsId
                id = str(session["id"])
            return redirect("/addproduct")
        else:
            return render_template("seller_login.html", status=True)
    else:
        return render_template("seller_login.html", status=False)

@application.route("/addproduct", methods=['GET', 'POST'])
def Add_product():
    if not session.get("name"):
        return redirect('/sellerlogin')
    else:
        if request.method == "POST":
            upload_image = request.files["image"]
            if upload_image != '':
                filepath = os.path.join(application.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)

                getCat = request.form.get("cat")
                getName = request.form["name"]
                getPrice = request.form["price"]
                getFeature = request.form["fea"]
                getSeller_id = id
                try:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO PRODUCT(CATEGORY,NAME,PRICE,FEATURE,IMAGE,SELLER_ID)\
                    VALUES('" + getCat + "','" + getName + "'," + getPrice + ",'" + getFeature + "','" + upload_image.filename + "','" + getSeller_id + "')")
                    connection.commit()
                    print("Inserted successfully")
                    return redirect('/viewseller')
                except Exception as err:
                    print(err)
    return render_template("add_product.html")

@application.route("/buy")
def Buy_cart():
    getUid = Uid
    cursor = connection.cursor()
    cursor.execute("INSERT INTO BUY SELECT * FROM CART C WHERE C.USER_ID="+getUid)
    connection.commit()
    print("Inserted into buy")
    cursor.execute("DELETE FROM CART WHERE USER_ID="+getUid)
    connection.commit()
    print("Deleted from cart")
    return redirect("/thanks")

@application.route("/payment", methods=['GET', 'POST'])
def userr_pay():
    getUid = Uid
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(PRICE) AS PRICE FROM PRODUCT P JOIN CART C ON C.PRODUCT_ID = P.ID WHERE C.USER_ID=" + getUid)
    result1 = cursor.fetchall()

    cursor.execute("SELECT * FROM PRODUCT P JOIN CART C ON C.PRODUCT_ID=P.ID WHERE C.USER_ID=" + getUid)
    result = cursor.fetchall()
    for i in result1:
        print(i[0])
    Name = getuName

    return render_template("payment.html",total=result1,user=Name, cart=result)



@application.route("/order")
def Order_Received():
    global total
    getSid = id
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCT P JOIN BUY B ON B.PRODUCT_ID = P.ID WHERE P.SELLER_ID="+getSid)
    result = cursor.fetchall()
    cursor.execute("SELECT SUM(PRICE) AS PRICE FROM PRODUCT P JOIN BUY B ON B.PRODUCT_ID = P.ID WHERE P.SELLER_ID="+getSid)
    result1 = cursor.fetchall()
    for i in result1:
        print(i[0])
    for i in result:
        print(i[2])
    return render_template("order.html",order=result,total=result1)

@application.route("/deletecart", methods=['GET', 'POST'])
def Delete_cart():
    try:
        getPid = request.args.get('id')
        getUid = Uid
        cursor = connection.cursor()
        cursor.execute("DELETE FROM CART WHERE PRODUCT_ID="+getPid+" AND USER_ID='"+getUid+"'")
        connection.commit()
        print("Product deleted from cart")

    except Exception as err:
        print(err)
    return redirect('/cartview')



@application.route("/search", methods=['GET', 'POST'])
def Search_dashboard():
    if request.method == 'POST':
        getName = request.form["sea"]
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PRODUCT WHERE NAME LIKE '%"+getName+"%' ")
        result = cursor.fetchall()
        return render_template("viewall.html",search=result, status=True)
    else:
        return render_template("viewall.html", search=[], status=False)


@application.route("/update", methods=['GET', 'POST'])
def Update_user():
    if request.method == 'POST':
        getUid = Uid
        getName = request.form["name"]
        getEmail = request.form["email"]
        getGender = request.form.get('gen')
        getAge = request.form["age"]
        getNumber = request.form["pno"]
        getAddress = request.form["add"]
        getPass = request.form["pass"]
        connection.execute("UPDATE USER SET CUST_NAME='"+getName+"',CUST_EMAIL='"+getEmail +"',CUST_GENDER='"+getGender+"',\
        CUST_AGE="+getAge+",CUST_NUMBER="+getNumber+",CUST_ADDRESS='"+getAddress+"',CUST_PASSWORD='"+getPass+"' WHERE ID="+getUid)
        connection.commit()
        print("Updated User Details")
        return redirect("/dashboard")

    return render_template("updateUser.html")


@application.route("/admin", methods=['GET', 'POST'])
def AdminLogin():
    if request.method == 'POST':
        getName = request.form["name"]
        getPass = request.form["pass"]
        if getName == "admin" and getPass == "12345":
            return redirect('/adminseller')
    return render_template("adminlogin.html")



@application.route("/adminseller")
def AdminSeller():
    cursor = connection.cursor()
    query = "SELECT * FROM SELLER"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.execute("SELECT SUM(PRICE) AS PRICE FROM PRODUCT P JOIN BUY B ON B.PRODUCT_ID = P.ID GROUP BY P.SELLER_ID")
    result2 = cursor.fetchall()
    for i in result2:
        print(i[0])
    return render_template("adminseller.html", sel=result, total1=result2)



@application.route("/deleteseller")
def Delete_seller():
    getSid = request.args.get("id")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM SELLER WHERE ID="+getSid)
    connection.commit()
    print("Deleted Seller Successfully")
    return redirect("/adminseller")



@application.route("/deleteuser")
def Delete_user():
    getUid = request.args.get("id")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM USER WHERE ID="+getUid)
    connection.commit()
    print("Deleted User Successfully")
    return redirect("/adminuser")




@application.route("/adminuser")
def AdminUser():
    cursor = connection.cursor()
    query = "SELECT * FROM USER"
    cursor.execute(query)
    result = cursor.fetchall()
    return render_template("adminuser.html", user=result)


@application.route("/sellerupdate", methods=['GET', 'POST'])
def Update_seller():
    if request.method == 'POST':
        getSid = id
        getName = request.form["name"]
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        getNumber = request.form["pno"]
        getAcc = request.form["ano"]
        getIfsc = request.form["ifsc"]
        connection.execute("UPDATE SELLER SET SELLER_NAME='"+getName+"',SELLER_EMAIL='"+getEmail +"',SELLER_PASSWORD='"+getPass+"',\
        SELLER_NUMBER="+getNumber+",SELLER_ACC="+getAcc+",SELLER_IFSC='"+getIfsc+"' WHERE ID="+getSid)
        connection.commit()
        print("Updated User Details")
        return redirect("/viewseller")

    return render_template("sellerupdate.html")


@application.route("/deleteproduct", methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        getName = request.form["name"]
        connection.execute("DELETE FROM PRODUCT WHERE NAME='" + getName + "' ")
        connection.commit()
        return redirect('/viewseller')


    return render_template("delete_product.html")



@application.route("/thanks")
def thanks():
    return render_template("afterPaymet.html")


@application.route("/about")
def about():
    return render_template("about.html")

@application.route("/dashboard")
def Dashboard():

        cursor = connection.cursor()
        query = "SELECT * FROM PRODUCT WHERE CATEGORY='Mobile/computers' "
        count1 = cursor.execute(query)
        result1 = cursor.fetchall()
        query2 = "SELECT * FROM PRODUCT WHERE CATEGORY='TV/Appliances/electronics' "
        count2 = cursor.execute(query2)
        result2 = cursor.fetchall()
        query3 = "SELECT * FROM PRODUCT WHERE CATEGORY='Men’s Fashion' "
        count3 = cursor.execute(query3)
        result3 = cursor.fetchall()
        query4 = "SELECT * FROM PRODUCT WHERE CATEGORY='Women’s Fashion' "
        count4 = cursor.execute(query4)
        result4 = cursor.fetchall()
        query5 = "SELECT * FROM PRODUCT WHERE CATEGORY='Home/Kitchen' "
        count5 = cursor.execute(query5)
        result5 = cursor.fetchall()
        query6 = "SELECT * FROM PRODUCT WHERE CATEGORY='Beauty/Health' "
        count6 = cursor.execute(query6)
        result6 = cursor.fetchall()
        query7 = "SELECT * FROM PRODUCT WHERE CATEGORY='Sports/Fitness' "
        count7 = cursor.execute(query7)
        result7 = cursor.fetchall()
        query8 = "SELECT * FROM PRODUCT WHERE CATEGORY='Toys/Baby Products' "
        count8 = cursor.execute(query8)
        result8 = cursor.fetchall()
        query9 = "SELECT * FROM PRODUCT WHERE CATEGORY='Car/Automobile' "
        count9 = cursor.execute(query9)
        result9 = cursor.fetchall()
        query10 = "SELECT * FROM PRODUCT WHERE CATEGORY='Books' "
        count10 = cursor.execute(query10)
        result10 = cursor.fetchall()
        return render_template("viewall.html",mc=result1, tae=result2, mf=result3, wf=result4, hk=result5, bh=result6, sf=result7, tb=result8, ca=result9, b=result10, sta=True)

@application.route("/cart")
def User_cart():
    try:
        getPid = request.args.get('id')
        getUid = Uid
        cursor = connection.cursor()
        cursor.execute("INSERT INTO CART(PRODUCT_ID,USER_ID) VALUES("+getPid+",'"+getUid+"')")
        connection.commit()
        print("Product addedd to cart successfully")

    except Exception as err:
        print(err)
    return redirect('/cartview')

@application.route("/cartview")
def User_cart_View():
    try:
        getUid = Uid
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PRODUCT P JOIN CART C ON C.PRODUCT_ID=P.ID WHERE C.USER_ID="+getUid)
        result = cursor.fetchall()
        cursor.execute("SELECT SUM(PRICE) AS PRICE FROM PRODUCT P JOIN CART C ON C.PRODUCT_ID = P.ID WHERE C.USER_ID="+getUid)
        result1 = cursor.fetchall()
        if result1 is None:
            return render_template("cartview.html",total=[],statu=True)
        for i in result1:
            print(i[0])
        return render_template("cartview.html",cart=result,total=result1,status=True,statu=False)


    except Exception as err:
        print(err)
    return render_template("cartview.html",cart=[],status=False)

@application.route("/viewexpand")
def View_expand():
    getid = request.args.get('id')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE ID="+getid)
    result = cursor.fetchall()
    return render_template("viewexpand.html",product=result)

@application.route("/viewseller")
def viewSeller():
    getId = id
    cursor = connection.cursor()
    count = cursor.execute("SELECT * FROM PRODUCT P JOIN SELLER S ON S.ID=P.SELLER_ID WHERE S.ID="+getId)
    result = cursor.fetchall()
    return render_template("viewseller.html", sellers=result)


@application.route("/forgot", methods=['GET', 'POST'])
def Forgot():
    if request.method == "POST":
        getEmail = request.form["email"]
        cursor = connection.cursor()
        query = "SELECT * FROM SELLER WHERE SELLER_EMAIL='"+getEmail+"'"
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            getnPass = request.form["pass"]
            getnCpass = request.form["cpass"]
            if getnPass == getnCpass:
                query2 = "UPDATE SELLER SET SELLER_PASSWORD='" + getnPass + "'"
                cursor.execute(query2)
                connection.commit()
            return render_template("forgotpass.html", status=True)
    else:
        return render_template("forgotpass.html", status=False)


@application.route("/userorder")
def Order_view_User():
    getUid = Uid
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCT P JOIN BUY B ON B.PRODUCT_ID = P.ID WHERE B.USER_ID="+getUid)
    result = cursor.fetchall()
    for i in result:
        print(i[2])
    return render_template("yourorder.html",view=result)


@application.route('/userlogout')
def user_logout():
    session["name"] = None
    return redirect('/')


@application.route('/sellerlogout')
def seller_logout():
    session["name"] = None
    return redirect('/sellerlogin')

if __name__ == ("__main__"):
    application.run(debug=True)
