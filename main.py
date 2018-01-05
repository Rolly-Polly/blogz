from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ror1ch3l@localhost:8889/build-a-blog'
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


  
if __name__ == "__main__":
    app.run()