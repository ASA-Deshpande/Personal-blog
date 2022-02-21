from datetime import datetime
from email.policy import default
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    content = db.Column(db.Text, nullable = False)
    posttype = db.Column(db.String(100), nullable = False, default = 'N/A')
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

all_posts = [
    {
        'title': 'Post1',
        'content': 'This is the content of post1 dfjsdfl.',
        'reading_time': str(22)
    },
    {
        'title': 'Post2',
        'content': 'This is the content of post2 dfjsdfl.'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods = ['GET', 'POST'])
def posts():
     
    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        post_type = request.form['posttype']
        new_post = BlogPost(title = post_title, content = post_content, posttype = post_type)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')

    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts = all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.posttype = request.form['posttype']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)

@app.route('/home/<string:name>', methods = ['GET', 'POST'])
def hello(name):
    return "Hello, " + name

if __name__ == "__main__":
    app.run(debug=True)