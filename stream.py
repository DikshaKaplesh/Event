from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Define the User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Define the Video model for storing video information
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)

# Create the database
db.create_all()

# Dummy video data (you would typically fetch this from the database)
# For demonstration purposes, let's add some videos
if not Video.query.all():
    video1 = Video(title='Video 1', url='video1.mp4')
    video2 = Video(title='Video 2', url='video2.mp4')
    db.session.add_all([video1, video2])
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    videos = Video.query.all()
    return render_template('index.html', videos=videos)

@app.route('/watch/<int:video_id>')
def watch(video_id):
    video = Video.query.get(video_id)
    if video:
        return render_template('watch.html', video=video)
    else:
        return "Video not found"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
