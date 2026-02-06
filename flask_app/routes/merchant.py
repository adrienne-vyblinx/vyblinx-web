from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

merchant_bp = Blueprint('merchant', __name__)

@merchant_bp.route('/business-structure')
def business_structure():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('account-creation/business-structure.html')

@merchant_bp.route('/select-business-type', methods=['POST'])
def select_business_type():
    data = request.get_json()
    business_type = data.get('type')
    
    if not business_type:
        return jsonify({"error": "Business type is required"}), 400
    
    session['business_type'] = business_type
    
    return jsonify({
        "message": "Business type saved",
        "redirect": "/business-details"
    }), 200

@merchant_bp.route('/business-details')
def business_details():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if 'business_type' not in session:
        return redirect(url_for('merchant.business_structure'))
    
    return render_template('account-creation/business-details.html')

@merchant_bp.route('/save-business-details', methods=['POST'])
def save_business_details():
    data = request.get_json()
    
    required_fields = ['first_name', 'surname', 'role', 'contact_number', 'company_email']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field.replace('_', ' ').title()} is required"}), 400
    
    session['business_representative'] = {
        'first_name': data.get('first_name'),
        'middle_name': data.get('middle_name'),
        'surname': data.get('surname'),
        'role': data.get('role'),
        'contact_number': data.get('contact_number'),
        'company_email': data.get('company_email'),
        'profile_picture': data.get('profile_picture')
    }
    
    return jsonify({
        "message": "Business representative details saved",
        "redirect": "/create-brand"
    }), 200

@merchant_bp.route('/create-brand')
def create_brand():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if 'business_representative' not in session:
        return redirect(url_for('merchant.business_details'))
    
    return render_template('account-creation/business-create-brand.html')

@merchant_bp.route('/save-brand-details', methods=['POST'])
def save_brand_details():
    brand_name = request.form.get('brand_name')
    
    if not brand_name:
        return jsonify({"error": "Brand name is required"}), 400
    
    logo = request.files.get('logo')
    business_document = request.files.get('business_document')

    session['brand_details'] = {
        'brand_name': brand_name,
        'has_logo': logo is not None,
        'has_document': business_document is not None
    }

    return jsonify({
        "message": "Brand details saved successfully",
        "redirect": "/social-club-account"
    }), 200

@merchant_bp.route('/social-club-account')
def social_club_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if 'brand_details' not in session:
        return redirect(url_for('merchant.create_brand'))
    
    return render_template('account-creation/business-social-club-account.html')

@merchant_bp.route('/save-social-club', methods=['POST'])
def save_social_club():
    account_name = request.form.get('account_name')
    page_description = request.form.get('page_description')
    
    if not account_name or not page_description:
        return jsonify({"error": "All fields are required"}), 400
    
    wallpaper = request.files.get('wallpaper')

    session['social_club'] = {
        'account_name': account_name,
        'page_description': page_description,
        'has_wallpaper': wallpaper is not None
    }

    return jsonify({
        "message": "Social Club account created successfully",
        "redirect": "/business-verification"
    }), 200

@merchant_bp.route('/business-verification')
def business_verification():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if 'social_club' not in session:
        return redirect(url_for('merchant.social_club_account'))
    
    return render_template('account-creation/business-verification.html')