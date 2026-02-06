from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/sign-in')
    
    return render_template('dashboard/dashboard.html')