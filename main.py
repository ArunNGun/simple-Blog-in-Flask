from flask import Flask,redirect,render_template,request,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLAlchemy_DATABASE_URI']='sqlite:///posts.db'
db=SQLAlchemy(app)
current_user=''
class BlogPost(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    article=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False,default='N/A')
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post'+str(self.id)

class UserData(db.Model):
    username=db.Column(db.String(10),primary_key=True)
    password=db.Column(db.String(8),nullable=False)

    def __repr__(self):
        return 'pass'+str(self.password)

db.create_all()
db.session.commit()

@app.route('/home')
@app.route('/home.html')
@app.route('/')
def index():
    all_posts=BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('home.html',posts=all_posts)

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signupprocess',methods=['POST','GET'])
def signupprocess():

    if request.method == 'POST':
        new_username=request.form['username']
        new_password=request.form['password']
        new_user=UserData(username='new_username',password='new_password')
        db.session.add(new_user)
        db.session.commit()
        current_user=new_username
        return render_template('newpost.html',author=new_username)
    else:
        return redirect(url_for('index'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/newpost')
def newpost():
    return render_template('newpost.html',author=current_user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/newblog',methods=['POST','GET'])
def newblog():
    all_posts=BlogPost.query.order_by(BlogPost.date_posted).all()
    if request.method == 'POST':
        if request.form['author']=='':
            return "please enter all fields"
        post_title=request.form['title']
        post_author=request.form['author']
        post_article=request.form['article']
        new_post = BlogPost(title=post_title,article=post_article,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('home.html',posts=all_posts)

@app.route('/deleteblog/<int:id>')
def deleteblog(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/home')


if __name__=='__main__':
    app.run(host = '0.0.0.0')
