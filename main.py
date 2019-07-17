from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dgDFr345FESW5m64ef'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password





    


@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/index')





@app.route('/login.html', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username 
            flash("Log in successful")
            return redirect('/')
        else:
            flash('Username and Password do not match. Or User does not exist', 'error')

    






@app.route('/blog.html', methods=['GET', 'POST'])
def display_posts():

    if request.args.get('id'):
        id = request.args.get('id')
        blog = Blog.query.get(id)
        return render_template('singleblog.html', titlebase= 'Build A Blog!', blog = blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', titlebase = 'Build a Blog', blogs=blogs)



@app.route('/signup.html', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password= request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()

        username_error = ''
        password_error = ''
        existing_error = ''

        if existing_user:
            username_error = 'Username already exists.' 
        if verify != password:
            password_error = 'Passwords do not match.' 
        if verify == '':
            verify_error = "Password must be verified."

        if len(password) <3:
            password_error = 'Password must be longer than 3 characters.'
        if password == '':
            password_error = 'Invalid password.'
        else: 
            password == password
            verify == verify     

        if len(username) < 3:
            username_error = 'Username must be longer than 3 characters.'
            username = ''
        if  username == '':
            username_error = 'Invalid username.'
            username = ''

        if existing_error != '':
            return render_template('/signup', existing_error=existing_error, username=username)

        if not username_error and not password_error and not verify_error and not existing_error:
            return render_template('/signup', username=username, username_error=username_error, password_error=password_error)
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('You have signed up!')


            return redirect('/login')

    return render_template('/signup')
        


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')




@app.route('/newpost.html', methods = ['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':

        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']

        blog_title_error = ""
        blog_body_error = ""

        if len(blog_title) == 0:
            blog_title_error = 'Blog entry must have a title.'

        if len(blog_body) == 0:
            blog_body_error = "Blog entry must have a body."

        if not blog_title_error and not blog_body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()

            recent_post= Blog.query.filter_by(title=blog_title).first()
            id = recent_post.id
            blog = Blog.query.filter_by(id=id).first()
            
            return redirect("/blog?id=" + str(id))
            
        else:
            return render_template('newpost.html', blog_title_error=blog_title_error, blog_body_error=blog_body_error, blog_title=blog_title, blog_body = blog_body)

@app.route('/', methods=['GET'])
def index():
    blogs = []
    id = request.args.get('id')
    if 'id' in request.args:

        blogs = Blog.query.filter_by(id=id).first()
        return render_template('singleblog.html', blogs=blogs)

    users = User.query.all()
    return redirect('index.html' blogs=blogs)

if __name__ == '__main__':
    app.run()



    
