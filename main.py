from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "s3cre3tstr1ng" 

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(450))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(12))
    blogs = db.relationship("Blog", backref="owner")

    def __init__(self,username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    print(request.endpoint)
    allowed_routes = ['login', 'login_request', 'blogs', 'index', 'signup', 'signup_request']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect('/login')

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/add_blog', methods=['GET'])
def add_blog():
    return render_template('add_blog.html')

@app.route('/add_blog', methods=['POST'])
def validate_form():
    if request.form["title"] == "" or request.form["body"] == "":       
        return render_template('add_blog.html', error_message="Please add a post")
    else:
        user_id = session['user_id']
        owner = User.query.get(user_id)
        title = request.form['title']
        body = request.form['body']
        blog = Blog(title, body, owner)
        db.session.add(blog)
        db.session.commit()
        return redirect('/')

@app.route('/blog', methods=['GET'])
def id(): 
    post_id = request.args.get('id') 
    user = request.args.get('user')
    
    if post_id is not None:
        blog = Blog.query.get(post_id)
        return render_template('single_blog.html', blog=blog)    

    if user is not None:
        user = User.query.get(user)
        return render_template('blogs.html', blogs=user.blogs)

    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)


@app.route('/signup', methods = ['GET'])
def signup_request():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup(): 
    username= request.form['username']
    password= request.form['password']
    verify_password= request.form['verify_password']
    user_error= ""
    pass_error= ""
        
    if username == "":
        user_error = "Enter username"

    elif len(username) < 3:
        user_error = "Username is too short"
    
    if password == "":
        pass_error = "Please enter Password"

    elif verify_password != password:
        pass_error = "Password does not match"
    
    if user_error == "" and pass_error == "":

        user_signup= User(username, password)
        db.session.add(user_signup)
        db.session.commit()
        
        session['user_id'] = user_signup.id
      
        return redirect('/add_blog')

    else:
        return render_template('signup.html', user_error=user_error, pass_error=pass_error, verify_password=pass_error)


@app.route('/login', methods=['GET'])
def login_request():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password") 
    user = User.query.filter_by(username=username).first() 
    

    if user is None:
        return redirect("/signup")

    if password == user.password:
        session['user_id']=user.id
 
        return redirect('/add_blog')
    
    return render_template('login.html', error="verify password")

@app.route('/logout', methods=['GET'])
def logout():
    del session['user_id']
    return redirect('/')



   
if __name__ == "__main__":
    app.run()