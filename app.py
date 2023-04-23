from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
#from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY']='dev'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://victor:7mudaki@localhost/flask_auth"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(100),primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50),nullable=False)
    profiles  = db.relationship('Profile',backref='user',uselist=False,lazy=True)


class Profile(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    postal_code=db.Column(db.String(50))
    posta_address = db.Column(db.String(100))
    physical_address = db.Column(db.String(500))
    phone=db.Column(db.String(20),unique=True,nullable=False)
    website = db.Column(db.String(100),unique=True)
    town=db.Column(db.String(20),nullable=False)
    interests = db.Column(db.String(500))
    role=db.Column(db.String(20),nullable=False)
    twitter = db.Column(db.String(100),unique=True)
    facebook = db.Column(db.String(100),unique=True)
    youtube = db.Column(db.String(100),unique=True)
    linkedin = db.Column(db.String(100),unique=True)
    region=db.Column(db.String(20),nullable=False)
    country=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(100),db.ForeignKey('User.email'),nullable=False)
    profile_dp=db.Column(db.LargeBinary(max))

with app.app_context():
    db.create_all()




@app.route('/',strict_slashes=False)
def home():
    return render_template('home.html')

@app.route('/login', strict_slashes=False)
def login():
    return render_template('login.html')

@app.route('/register', strict_slashes=False)
def register():
    return render_template('register.html')

@app.route('/profile', strict_slashes=False)
def profile():
    return render_template('profile.html')

@app.route('/edit-profile', strict_slashes=False)
def edit_profile():
    return render_template('profile-2.html')


if __name__=='__main__':
    app.run(debug=True)
