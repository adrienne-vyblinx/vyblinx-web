from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

merchant_bp = Blueprint('merchant', __name__, url_prefix='/account')

@merchant_bp.route('/business-structure')
def business_structure():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('layout/app.html')