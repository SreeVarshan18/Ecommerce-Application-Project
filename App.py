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


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['UPLOAD_FOLDER'] = "static\images"

@app.route("/",methods=["GET","POST"])
def User_register():
    if request.method == "POST":
        getName = request.form["name"]
        getEmail = request.form["email"]
        getGender = request.form.get('gen')
        getAge = request.form["age"]
        getNumber = request.form["pno"]
        getAddress = request.form["add"]
        getPass = request.form["pass"]
        connection.execute("INSERT INTO USER(CUST_NAME,CUST_EMAIL,CUST_GENDER,CUST_AGE,CUST_NUMBER,CUST_ADDRESS,CUST_PASSWORD)\
                            VALUES('"+getName+"','"+getEmail+"','"+getGender+"',"+getAge+","+getNumber+",\
                            '"+getAddress+"','"+getPass+"')")
        connection.commit()
        print("Customer details inserted successfully")
        return redirect('/userlogin')

    return render_template("userregister.html")

@app.route("/userlogin",methods=["GET","POST"])
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

@app.route("/sellerregister",methods=['GET','POST'])
def Seller_register():
    if request.method == "POST":
        getName = request.form["name"]
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        getNumber = request.form["pno"]
        getAcc = request.form["ano"]
        getIfsc = request.form["ifsc"]
        connection.execute("INSERT INTO SELLER(SELLER_NAME,SELLER_EMAIL,SELLER_PASSWORD,SELLER_NUMBER,SELLER_ACC,SELLER_IFSC)\
                           VALUES('"+getName+"','"+getEmail+"','"+getPass+"',"+getNumber+","+getAcc+",'"+getIfsc+"')")
        connection.commit()
        print("Seller details inserted successfully")
        return redirect('/sellerlogin')
    return render_template("seller_register.html")

@app.route("/sellerlogin",methods=['GET','POST'])
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

@app.route("/addproduct",methods=['GET','POST'])
def Add_product():
    if not session.get("name"):
        return redirect('/sellerlogin')
    else:
        if request.method == "POST":
            upload_image = request.files["image"]
            if upload_image != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
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

@app.route("/buy")
def Buy_cart():
    getUid = Uid
    cursor = connection.cursor()
    cursor.execute("INSERT INTO BUY SELECT * FROM CART C WHERE C.USER_ID="+getUid)
    connection.commit()
    print("Inserted into buy")
    cursor.execute("DELETE FROM CART WHERE USER_ID="+getUid)
    connection.commit()
    print("Deleted from cart")
    return redirect("/dashboard")

@app.route("/payment",methods=['GET','POST'])
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



@app.route("/order")
def Order_Received():
    getSid = id
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCT P JOIN BUY B ON B.PRODUCT_ID = P.ID WHERE P.SELLER_ID="+getSid)
    result = cursor.fetchall()
    for i in result:
        print(i[2])
    return render_template("order.html",order=result)

@app.route("/deletecart",methods=['GET','POST'])
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



@app.route("/search",methods=['GET','POST'])
def Search_dashboard():
    if request.method == 'POST':
        getName = request.form["sea"]
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PRODUCT WHERE NAME LIKE '%"+getName+"%' ")
        result = cursor.fetchall()
        return render_template("viewall.html",search=result, status=True)
    else:
        return render_template("viewall.html", search=[], status=False)


@app.route("/update",methods=['GET','POST'])
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




@app.route("/deleteproduct",methods=['GET','POST'])
def delete_product():
    if request.method == 'POST':
        getName = request.form["name"]
        connection.execute("DELETE FROM PRODUCT WHERE NAME='" + getName + "' ")
        connection.commit()
        return redirect('/addproduct')


    return render_template("delete_product.html")







@app.route("/dashboard")
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

@app.route("/cart")
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

@app.route("/cartview")
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

@app.route("/viewexpand")
def View_expand():
    getid = request.args.get('id')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE ID="+getid)
    result = cursor.fetchall()
    return render_template("viewexpand.html",product=result)

@app.route("/viewseller")
def viewSeller():
    getId = id
    cursor = connection.cursor()
    count = cursor.execute("SELECT * FROM PRODUCT P JOIN SELLER S ON S.ID=P.SELLER_ID WHERE S.ID="+getId)
    result = cursor.fetchall()
    return render_template("viewseller.html", sellers=result)


@app.route("/forgot",methods=['GET','POST'])
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


@app.route('/userlogout')
def user_logout():
    session["name"] = None
    return redirect('/userlogin')


@app.route('/sellerlogout')
def seller_logout():
    session["name"] = None
    return redirect('/sellerlogin')

if __name__ == ("__main__"):
    app.run(debug=True)
