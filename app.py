from flask import *
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'mysecretkey'


@app.route('/', methods=['GET', "POST"])
def index():
    if (request.method == "GET"):
        if 'username' in session:
            return render_template('home.html')
    if (request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from user")
        rows = cur.fetchall()
        passkey = [i["password"] for i in rows if i["username"] == username]
        print(*passkey)
        if password in passkey:
            session['username'] = username
            return redirect("/home")
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if (request.method == "GET"):
        return render_template('home.html')
    if (request.method == "POST"):
        if (request.form["b"] == "logout"):
            session.pop('username', None)
            return redirect('/')
        if request.form["b"] == "drinks":
            return redirect('/pras1')
        if request.form["b"] == "desert":
            return redirect('/pras2')
        return render_template('home.html')


# @app.route('/localhost/register',methods=['GET','POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == "POST":
        data = (request.form.get("username"), request.form.get("password"), request.form.get("email"))
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute('''insert into user values (?,?,?)''', data)
        con.commit()
        con.close()
        print(*data)
        return redirect('/')


@app.route('/pras1', methods=['GET', 'POST'])
def pras1():
    items=[]
    if request.method == "GET":
        return render_template('pras1.html')
    if (request.method == "POST"):
        if (request.form["b"] == "logout"):
            session.pop('username', None)
            return redirect('/')
        if request.form["b"] == "drinks":
            return redirect('/pras1')
        if request.form["b"] == "desert":
            return redirect('/pras2')
        res = make_response(redirect('/pras1'))
        order = request.form["b"]
        res.set_cookie('booked',order)
        # if request.cookies.get('order') == None:
        #     items.append(order)
        #     res.set_cookie('order', str(items))
        # else:
        #     items = eval(request.cookies.get("booked"))
        #     items.append(order)
        #     res.set_cookie('booked', str(items))
        return redirect('/pras1')


@app.route('/pras2', methods=['GET', 'POST'])
def pras2():
    if request.method == "GET":
        return render_template('pras2.html')
    if (request.method == "POST"):
        if (request.form["b"] == "logout"):
            session.pop('username', None)
            return redirect('/')
        if request.form["b"] == "drinks":
            return redirect('/pras1')
        if request.form["b"] == "desert":
            return redirect('/pras2')


@app.route('/cart', methods=['GET','POST'])
def cart():
    if request.method == "GET":
        return render_template('cart.html')
    if request.method == "POST":
        if (request.cookies.get('Item') == None):
            return render_template('cart.html', item="CART EMPTY")
        item = eval(request.cookies.get('Item'))
        return render_template('cart.html', item=item)


@app.route('/buy',methods=['POST','GET'])
def buy():
    if request.method == 'POST':
        resp = make_response(render_template('home.html'))
        resp.set_cookie('Item',expires=0)
        return resp
    return render_template('home.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        if(request.cookies.get('Item')==None):
            item=[]
        else:
            item = eval(request.cookies.get('Item'))
        new_item = request.form['b']
        print(item)
        if (new_item =='HOTDOG & SODA' or new_item =='POPCORN & SHAKE' or new_item =='CHOCOLATE ICECREAM' or new_item =='BAGEL SANDWICH'):
            resp = make_response(render_template('pras1.html'))
        else:
            resp = make_response(render_template('pras2.html'))
        item.append(new_item)
        resp.set_cookie('Item', str(item))
        # return render_template('pras1.html')
        return resp


@app.route('/getcookie')
def getcookie():
   item = request.cookies.get('Item')
   return render_template('cart.html',item=item)


@app.errorhandler(404)
@app.errorhandler(500)
def error(e):
    return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
