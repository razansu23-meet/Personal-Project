from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {

  "apiKey": "AIzaSyB9V5AqdglDsqyw5CodtJPMxZgmqgF18Co",

  "authDomain": "project-e5b96.firebaseapp.com",

  "databaseURL": "https://project-e5b96-default-rtdb.europe-west1.firebasedatabase.app",

  "projectId": "project-e5b96",

  "storageBucket": "project-e5b96.appspot.com",

  "messagingSenderId": "36693287004",

  "appId": "1:36693287004:web:04e59126059d71453fc699",

  "measurementId": "G-9SECFJGRLB"

}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'ygy77t7gyvjfcxsz88yuiuiucet56dz,;,;zewzewwew88yvtyjzdyhuvdfxtxdtty7866rt6yuffy7'
@app.route('/', methods=['GET', 'POST'])
def start():
    error=""
    if request.method == 'POST':
        try:
            return redirect(url_for('plans'))
        except:
            error = "Authentication failed"
            return render_template("index.html")
    return render_template("index.html")
  
@app.route('/plans', methods=['GET', 'POST'])
def plans():
    error=""
    # if request.method == 'GET':
    #     try:
    #         return redirect(url_for('signup'))
    #     except:
    #         error = "Authentication failed"
    #         return render_template("index.html")
    return render_template("plans.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['password']
        #username = request.form['username']
        user={"email" : email , "password" : password , fname:"fname" , lname:"lname"  }
        
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password )
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    else:
        return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('/signin'))
        except:
            error = "Authentication failed"
            return render_template("index.html")
    else:
        return render_template("signin.html")
    

@app.route('/prices', methods=['GET', 'POST'])
def prices():
    # error=""
    # if request.method == 'GET':
    #     try:
    #         return redirect(url_for('index'))
    #     except:
    #         error = "Authentication failed"
    #         return render_template("index.html")
    return render_template("prices.html")
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart = db.child("Cart").child(login_session['user']['localId']).get().val()
    #price = request.form['price']
    # error=""
    # if request.method == 'GET':
    #     try:
    #         return redirect(url_for('index'))
    #     except:
    #         error = "Authentication failed"
    #         return render_template("index.html")

    return render_template("cart.html" , cart=cart)

@app.route('/home', methods=['GET', 'POST'])
def home():
    # error=""
    # if request.method == 'GET':
    #     try:
    #         return redirect(url_for('index'))
    #     except:
    #         error = "Authentication failed"
    #         return render_template("index.html")
    return render_template("home.html")
@app.route('/electronics', methods=['GET', 'POST'])
def electronics():
    
    return render_template("electronics.html")
@app.route('/food', methods=['GET', 'POST'])
def food():
    
    return render_template("food.html")

@app.route('/clothes', methods=['GET', 'POST'])
def clothes():
    return render_template("clothes.html")
@app.route('/bags', methods=['GET', 'POST'])
def bags():
    return render_template("bags.html")
@app.route('/phome', methods=['GET', 'POST'])
def phome():
    return render_template("phome.html")
@app.route('/add', methods=['GET', 'POST'])
def add():
    error=""
    if request.method == 'POST':
        try:
            return redirect(url_for('index'))
        except:
            error = "Authentication failed"
            return render_template("index.html")
    return render_template("home.html")

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method =='POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        product = {"title":title, "price":price, "description":description}
        db.child("Product").child(title).set(product)
        return render_template("products.html" , title=title , price=price, description=description)
    else:
        return render_template("products.html" )

@app.route('/create', methods=['GET', 'POST'])
def create():
    error=""
    if request.method == 'POST':
        try:
            
            return redirect(url_for('products') )
        except:
            error = "Authentication failed"
            return render_template("index.html")
    return render_template("create.html")
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if request.method == 'GET':
        return render_template("shop.html")
    # else:
    #     cart = db.child("Cart").child(login_session['user']['localId']).get().val()
    #     if cart:
    #         if request.form['Add to Cart'] in cart:
    #             cart[request.form['Add to Cart']]+=1
    #         else:
    #             cart[request.form['Add to Cart']]=1
    #             db.child("Cart").child(login_session['user']['localId']).update(cart)
    #     else:
    #         cart = {request.fom['Add to Cart']:1}
    #         db.child("Cart").child(login_session['user']['localId']).set(cart)
    #     return render_template("shop.html")

@app.route('/item/<string:product>',)
def add_item(product):
    cart = db.child("Cart").child(login_session['user']['localId']).get().val()
    if cart is None:
        cart = {}
    if product in cart:
        cart[product] += 1
    else:
        cart[product] = 1
    db.child("Cart").child(login_session['user']['localId']).set(cart)
    return redirect(url_for('shop'))

#return render_template("shop.html")
# from firebase_admin import credentials, initialize_app, storage
# # Init firebase with your credentials
# cred = credentials.Certificate("idk.json")
# initialize_app(cred, {'storageBucket': 'project-e5b96.appspot.com'})

# # Put your local file path 
# fileName = "myImage.jpg"
# bucket = storage.bucket()
# blob = bucket.blob(fileName)
# blob.upload_from_filename(fileName)

# # Opt : if you want to make public access from the URL
# blob.make_public()

# print("your file url", blob.public_url)
if __name__ == '__main__':
    app.run(debug=True)