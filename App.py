import os

from flask import Flask, request, render_template
import sqlite3
from werkzeug.utils import redirect, secure_filename



connection = sqlite3.connect("onestop.db", check_same_thread=False)
table1 = connection.execute("select * from sqlite_master where type = 'table' and name = 'SELLER'").fetchall()
table2 = connection.execute("select * from sqlite_master where type = 'table' and name = 'USER'").fetchall()
table3 = connection.execute("select * from sqlite_master where type = 'table' and name = 'PRODUCT'").fetchall()
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
                                SELLER_ID INTEGER); ''')
    print("Product table created")
app = Flask(__name__)

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
    if request.method == "POST":
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        cursor = connection.cursor()
        query = "SELECT * FROM USER WHERE CUST_EMAIL='"+getEmail+"' and CUST_PASSWORD='"+getPass+"' "
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            print("password correct")
            return redirect('/')
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
    if request.method == "POST":
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        cursor = connection.cursor()
        query = "SELECT * FROM SELLER WHERE SELLER_EMAIL='"+getEmail+"' AND SELLER_PASSWORD='"+getPass+"'"
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            return redirect("/addproduct")
        else:
            return render_template("seller_login.html", status=True)
    else:
        return render_template("seller_login.html", status=False)

@app.route("/addproduct",methods=['GET','POST'])
def Add_product():
    if request.method == "POST":
        upload_image= request.files["image"]
        if upload_image!='':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
            upload_image.save(filepath)

            getCat = request.form.get("cat")
            getName = request.form["name"]
            getPrice = request.form["price"]
            getFeature = request.form["fea"]
            getSeller_id = request.form["sid"]
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO PRODUCT(CATEGORY,NAME,PRICE,FEATURE,IMAGE,SELLER_ID)\
                VALUES('"+getCat+"','"+getName+"',"+getPrice+",'"+getFeature +"','"+upload_image.filename+"',"+getSeller_id+")")
                connection.commit()
                print("Inserted successfully")
                return redirect('/addproduct')
            except Exception as err:
                print(err)
    return render_template("add_product.html")

@app.route("/deleteproduct",methods=['GET','POST'])
def delete_product():
    if request.method == 'POST':
        getName = request.form["name"]
        connection.execute("DELETE FROM PRODUCT WHERE NAME='" + getName + "' ")
        connection.commit()
        return redirect('/addproduct')


    return render_template("delete_product.html")

@app.route("/dashboard",methods=['GET','POST'])
def Dashboard():
    getSearch = request.form[""]
    if len(getCategory)>0:
        cursor = connection.cursor()
        query = "SELECT * FROM PRODUCT WHERE CATEGORY='"+getCategory+"' "
        result1 = cursor.execute(query)
        return render_template("viewall.html",search=result1,staus=True)
    elif len(getSearch)>0:
        cursor = connection.cursor()
        query = "SELECT * FROM PRODUCT WHERE NAME='"+getSearch+"' "
        result2 = cursor.execute(query)
        return render_template("viewall.html", search=result2, staus=True)

    else:
        return render_template("viewall.html",search=[],status=False)

@app.route("/viewexpand")
def View_expand():
    getid = request.args.get('id')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCT")
    result = cursor.fetchall()
    return render_template("viewexpand.html",product=result)

@app.route("/viewseller")
def viewSeller():
    cursor = connection.cursor()
    count = cursor.execute("SELECT * FROM PRODUCT")
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
            return render_template("forgotpass.html", status=True)
    else:
        return render_template("forgotpass.html", status=False)


if __name__ == ("__main__"):
    app.run(debug=True)