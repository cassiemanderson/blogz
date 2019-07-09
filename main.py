from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))

    def __init__(self, name):
        self.title = title
        self.body = body

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():

    blog_title_error = ""
    blog_body_error = ""

    if request.method == 'POST':

        blog_title = request.form.get('blog-title')
        if len(blog_title) == 0:
            blog_title_error = 'Blog entry must have a title.'

        blog_body = request.form.get('blog-body')
        if len(blog_body) == 0:
            blog_body_error = "Blog entry must have a body."

        if not blog_title_error and not blog_body_error:
            return render_template('newpost.html', blog_title_error=blog_title_error, blog_body_error=blog_body_error, blog_body=blog_body, blog_title=blog_title)
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            new_blog_id = new_blog.id
            blog = Blog.querty.get(new_blog_id)
            return render_template('/blog.html', blog=blog)

    return render_template('/newpost.html', title="Add New Blog Post")

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

        
    blogs = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", blogs=blogs)

if __name__ == '__main__':
    app.run()