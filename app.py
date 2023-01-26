from flask import Flask ,render_template,request,redirect,url_for, flash, session, logging
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
db = SQLAlchemy(app)



class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        if request.method == 'POST':
            return render_template('home.html')
        return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('hello_world'))
            else:
                return render_template('sorry.html')
        except:
            return render_template('sorry.html')



@app.route('/register/', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html')
    return render_template('register.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404



@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500



@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))



class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    phone = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



def login_required(func):
    def inner():
        hello_world()
        return render_template('error.html')
        func()
    return inner



@app.route('/key',methods=['GET' ,'POST'])
def hello_world():
    if request.method=='POST':
        title = (request.form["title"])
        desc = (request.form["desc"])
        phone = (request.form["phone"])
        todo =Todo(title=title, desc=desc ,phone=phone)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)



@app.route('/show')
def show():
    allTodo=Todo.query.all()
    print(allTodo)
    return "all employees"



@app.route('/update/<int:sno>',methods=['GET' ,'POST'])
def update(sno):
    if request.method=='POST':
        title = (request.form["title"])
        desc = (request.form["desc"])
        phone = (request.form["phone"])

        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        todo.phone=phone

        db.session.add(todo)
        db.session.commit()
        return redirect("/key")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)



@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/key")



if __name__=="__main__":
    db.create_all()
    app.run(debug=True, port=5500)


