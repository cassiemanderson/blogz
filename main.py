from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


blogs = []


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog = request.form['blog']
        blogs.append(blog)

    return render_template('blog.html',title="Build A Blog", blogs=blogs)


app.run()