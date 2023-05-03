from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy_imageattach.entity import Image, image_attachment
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, login_user, LoginManager, current_user,login_required

app = Flask(__name__)
app.config['SECRET_KEY']='dev'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://victor:7mudaki@localhost/flask_auth"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.view='login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),unique=True,nullable=False)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    profiles  = db.relationship('Profile',backref='users',uselist=False,lazy=True)
    
    
class Profile(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    postal_code=db.Column(db.String(50))
    postal_address = db.Column(db.String(100))
    physical_address = db.Column(db.String(500))
    phone=db.Column(db.String(20),unique=True,nullable=False)
    website = db.Column(db.String(100),unique=True)
    town=db.Column(db.String(20),nullable=False)
    interests = db.Column(db.Text())
    role=db.Column(db.String(20),nullable=False)
    twitter = db.Column(db.String(100),unique=True)
    facebook = db.Column(db.String(100),unique=True)
    youtube = db.Column(db.String(100),unique=True)
    linkedin = db.Column(db.String(100),unique=True)
    region=db.Column(db.String(20),nullable=False)
    country=db.Column(db.String(20),nullable=False)
    profile_dp=db.Column(db.LargeBinary(max))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    

with app.app_context():
    db.create_all()




@app.route('/',strict_slashes=False)
def home():
    return render_template('home.html')



@app.route('/login', methods=('GET','POST'),strict_slashes=False)
def login():
    if request.method=='POST':
        email=request.form["email"]
        password = request.form["password"]

        user=Users.query.filter_by(email=email).first()

        if check_password_hash(user.password,password):
            login_user(user)
            flash("logged in successfully")
            return render_template('profile-2.html',user=user)
        
        else:
            flash("incorrect password")
        #else:
        #flash("email does not exist")



    return render_template('login.html')

@app.route('/register', methods=('GET','POST'), strict_slashes=False)
def register():
    if request.method=='POST':
        email = request.form['email']
        first_name=request.form['fname']
        last_name=request.form['lname']
        password=request.form['password']
        confirm_pass=request.form['confirm_pass']
        
        if confirm_pass==password:
            password=generate_password_hash(password)
            new_user=Users(email=email,first_name=first_name,last_name=last_name,password=password)
                
            try:
                db.session.add(new_user)
                db.session.commit()
                flash ("signed up successfully,kindly login")
                return redirect(url_for('login'))

            except:
                return f"Not added {email} {first_name} {last_name}"
        else:
            flash ("passwords do not match,kindly re enter the password")


    return render_template('register.html')

@app.route('/profile', strict_slashes=False)
def profile():
    return render_template('profile.html')

@app.route('/edit-profile', strict_slashes=False)
@login_required
def edit_profile():
    if request.method=='POST':
        postal_code=request.form['postal_code']
        postal_address=request.form['postal_address']
        physical_address=request.form['physical_address']
        town=request.form['town']
        region=request.form['region']
        country=request.form['country']
        role=request.form['role']
        phone=request.form['phone']
        website=request.form['website']
        interests=request.form['interest']
        linkedin=request.form['linkedin']
        twitter=request.form['twitter']
        facebook=request.form['facebook']
        youtube=request.form['youtube']


        try:
            new_profile=Profile(user_id=user_id,youtube=youtube,region=region,twitter=twitter,facebook=facebook,
                linkedin=linkedin,website=website,role=role,phone=phone,postal_code=postal_code,
                postal_address=postal_address,physical_address=physical_address,interests=interests,country=country,town=town)

            db.session.add(new_profile)
            db.session.commit()
            flash("profile updated succesfully")
            return render_template('profile.html')

        except:
            flash("profile note updated,kindly retry")

    return render_template('profile-2.html')


if __name__=='__main__':
    app.run(debug=True)