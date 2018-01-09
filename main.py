from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(450))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['GET'])
def index():
    blogs = Blog.query.all()
    return render_template('blogs.html', blogs=blogs)


@app.route('/add_blog', methods=['GET'])
def add_blog():
    return render_template('add_blog.html')

@app.route('/add_blog', methods=['POST'])
def validate_form():
    if request.form["title"] == "" or request.form["body"] == "":       
        return render_template('add_blog.html', error_message="Please add a post")
    else:
        title = request.form['title']
        body = request.form['body']
        blog = Blog(title, body)
        db.session.add(blog)
        db.session.commit()
        return redirect('/')

@app.route('/blog', methods=['GET'])
def id():
    post_id = int(request.args.get('id'))
    blog = Blog.query.get(post_id)
    return render_template('single_blog.html', blog=blog)    


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(12))

    def __init__(self,username, password):
        self.username = username
        self.password = password

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
        
        return redirect('/')

    else:
        return render_template('signup.html', user_error=user_error, pass_error=pass_error, verify_password=pass_error)


    


  
if __name__ == "__main__":
    app.run()