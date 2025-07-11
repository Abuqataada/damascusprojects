from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import string
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# configure upload folder
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

# Ensure upload dir exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --------------------------------------------------
# MODELS
# --------------------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    referrals = db.relationship('User', backref=db.backref('referrer', remote_side=[id]), lazy='dynamic')
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    referral_code = db.Column(db.String(20), unique=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    profile_picture = db.Column(db.String(200), nullable=True)

    def get_profile_picture_url(self):
        if self.profile_picture:
            return url_for('static', filename=f'uploads/{self.profile_picture}')
        return url_for('static', filename='images/profile.png')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(50))
    subscriptions = db.relationship('Subscription', backref='program', lazy=True)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(100), default='pending', nullable=False)

# --------------------------------------------------
# INIT DATA
# --------------------------------------------------
def create_tables_and_initial_data():
    db.create_all()
    create_initial_programs()

def create_initial_programs():
    programs = [
        {'name': 'Project Management', 'slug': 'project_management', 'price': 50000, 'icon': 'fas fa-tasks'},
        {'name': 'Investor', 'slug': 'investor', 'price': 499999, 'icon': 'fas fa-chart-line'},
        {'name': 'Innovator or Idea Owner', 'slug': 'innovator', 'price': 21500, 'icon': 'fas fa-lightbulb'},
        {'name': 'Visa Sponsorship', 'slug': 'visa', 'price': 37500, 'icon': 'fas fa-passport'},
        {'name': 'Priority Housing', 'slug': 'housing', 'price': 50000, 'icon': 'fas fa-home'},
        {'name': 'Hire Purchase', 'slug': 'hire', 'price': 21000, 'icon': 'fas fa-truck-pickup'}
    ]
    for prog in programs:
        if not Program.query.filter_by(slug=prog['slug']).first():
            db.session.add(Program(**prog))
    db.session.commit()


def generate_referral_code(length=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def get_unique_referral_code():
    while True:
        code = f"USR{generate_referral_code()}"
        if not User.query.filter_by(referral_code=code).first():
            return code

@app.route('/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    file = request.files.get('profile_picture')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
            flash('Invalid file format. Please upload an image.', 'danger')
            return redirect(url_for('dashboard'))

        # rename to user id to avoid conflicts
        new_filename = f"user_{current_user.id}{file_ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        
        current_user.profile_picture = new_filename
        db.session.commit()
        flash('Profile picture updated successfully.', 'success')
    else:
        flash('No file selected.', 'warning')

    return redirect(url_for('dashboard'))

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/programs/project-management')
def project_management():
    return render_template('programs/project_management.html')

@app.route('/programs/investor')
def investor():
    return render_template('programs/investor.html')

@app.route('/programs/innovator')
def innovator():
    return render_template('programs/innovator.html')

@app.route('/programs/visa')
def visa():
    return render_template('programs/visa.html')

@app.route('/programs/housing')
def housing():
    return render_template('programs/housing.html')

@app.route('/programs/hire')
def hire():
    return render_template('programs/hire.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        program_slug = request.form.get('program')
        referral_code_input = request.form.get('referral_code')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        program = Program.query.filter_by(slug=program_slug).first()
        if not program:
            flash('Invalid program selected.', 'danger')
            return redirect(url_for('signup'))

        user = User(full_name=full_name, email=email)
        user.set_password(password)

        if referral_code_input:
            referrer = User.query.filter_by(referral_code=referral_code_input).first()
            if referrer:
                user.referrer_id = referrer.id

        db.session.add(user)
        db.session.commit()

        # Generate referral code
        user.referral_code = get_unique_referral_code()
        db.session.commit()

        subscription = Subscription(user_id=user.id, program_id=program.id)
        db.session.add(subscription)
        db.session.commit()

        flash('Account created! Now login.', 'success')
        return redirect(url_for('login'))
    programs = Program.query.all()
    return render_template('signup.html', programs=programs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    programs = Program.query.all()
    return render_template('dashboard.html', subscriptions=subscriptions, programs=programs)

@app.route('/mark_payment_done', methods=['POST'])
@login_required
def mark_payment_done():
    this_user = Subscription.query.filter_by(user_id=current_user.id).first()
    this_user.status = 'pending'
    db.session.commit()
    flash('Thank you! Your payment is being processed.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

with app.app_context():
    # Create tables and initial data
    create_tables_and_initial_data()
# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        create_tables_and_initial_data()
    app.run(debug=True)
