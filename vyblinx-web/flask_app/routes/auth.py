from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_app.config import supabase

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.signup'))

@auth_bp.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth_bp.route('/signup-otp')
def confirm_email():
    return render_template('auth/signup-otp.html')

@auth_bp.route('/signin')
def login():
    return render_template('auth/signin.html')

@auth_bp.route('/create-password')
def create_password():
    return render_template('auth/create-password.html')

@auth_bp.route('/forgot-password')
def forgot_password():
    return render_template('auth/forgot-password.html')

# API ROUTES

@auth_bp.route('/send_otp_email', methods=['POST'])
def send_otp_email():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    try:
        response = supabase.auth.sign_in_with_otp({
            "email": email
        })
        
        session['signup_email'] = email
        
        print(f"OTP sent to {email}")
        return jsonify({"message": "OTP sent successfully"}), 200
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = session.get('signup_email')
    otp = data.get('otp')
    
    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400
    
    try:
        response = supabase.auth.verify_otp({
            "email": email,
            "token": otp,
            "type": "email"
        })
        
        if response.user:
            session['user_id'] = response.user.id
            print(f"OTP verified for user: {response.user.id}")
            return jsonify({
                "message": "OTP verified successfully", 
                "redirect": url_for('auth.create_password')
            }), 200
        else:
            return jsonify({"error": "Invalid OTP"}), 400
            
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/set_password', methods=['POST'])
def set_password():
    data = request.get_json()
    password = data.get('password')
    user_id = session.get('user_id')
    
    if not password or not user_id:
        return jsonify({"error": "Password and user session required"}), 400
    
    try:
        response = supabase.auth.update_user({
            "password": password
        })
        
        print(f"Password set for user: {user_id}")
        return jsonify({
            "message": "Password set successfully", 
            "redirect": url_for('auth.login')
        }), 200
        
    except Exception as e:
        print(f"Error setting password: {e}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/signin_user', methods=['POST'])
def signin_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            session['user_id'] = response.user.id
            print(f"User signed in: {response.user.id}")
            return jsonify({"message": "Sign in successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        print(f"Error signing in: {e}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/logout')
def logout():
    try:
        supabase.auth.sign_out()
        session.clear()
        print("User logged out")
        return redirect(url_for('auth.login'))
    except Exception as e:
        print(f"Error logging out: {e}")
        return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_password_request', methods=['POST'])
def forgot_password_request():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    try:
        response = supabase.auth.reset_password_email(email)
        
        print(f"Password reset email sent to {email}")
        return jsonify({"message": "Password reset email sent"}), 200
        
    except Exception as e:
        print(f"Error sending reset email: {e}")
        return jsonify({"error": str(e)}), 500