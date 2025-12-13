from flask import Blueprint, render_template
pages_bp = Blueprint('pages', __name__, url_prefix = '/')
@pages_bp.route('/login')
def login():
    return render_template('login.html')
@pages_bp.route('/register')
def register():
    return render_template('register.html')
@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@pages_bp.route('/')
def main_page():
    return render_template('register.html')