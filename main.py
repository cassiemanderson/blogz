from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog2:build-a-blog2@localhost:8889/build-a-blog2'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['GET', 'POST'])
def display_posts():

    if request.args.get('id'):
        id = request.args.get('id')
        blog = Blog.query.get(id)
        return render_template('singleblog.html', titlebase= 'Build A Blog!', blog = blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', titlebase = 'Build a Blog', blogs=blogs)


@app.route('/newpost', methods = ['POST', 'GET'])
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
    return redirect('/blog')

if __name__ == '__main__':
    app.run()



    
