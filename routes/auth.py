from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user
from app import db
from models import User, Program, Subscription
from forms import SignupForm
import secrets
import string

auth_bp = Blueprint('auth', __name__)

def generate_referral_code(length=8):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    
    # Populate program choices from database
    programs = Program.query.all()
    form.program.choices = [(p.slug, f"{p.name} - ₦{p.price:,.0f}") for p in programs]
    form.program.choices.insert(0, ('', 'Choose a program...'))
    
    if form.validate_on_submit():
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            referral_code=generate_referral_code()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        
        # Create subscription for selected program
        program = Program.query.filter_by(slug=form.program.data).first()
        if program:
            subscription = Subscription(user=user, program=program)
            db.session.add(subscription)
        
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup_modal.html', form=form)

@auth_bp.route('/login')
def login():
    # Your login implementation here
    pass