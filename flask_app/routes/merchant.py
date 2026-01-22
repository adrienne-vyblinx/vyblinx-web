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
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    if 'business_type' not in session:
        return jsonify({"error": "Please select business type first"}), 400
    
    data = request.get_json()
    
    required_fields = ['business_name', 'address', 'city', 'country']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field.replace('_', ' ').title()} is required"}), 400
    
    session['business_details'] = {
        'business_name': data.get('business_name'),
        'address': data.get('address'),
        'city': data.get('city'),
        'country': data.get('country'),
        'phone': data.get('phone', ''),
        'website': data.get('website', '')
    }
    
    return jsonify({
        "message": "Business details saved",
        "redirect": "/create-brand"
    }), 200


@merchant_bp.route('/create-brand')
def create_brand():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if 'business_type' not in session or 'business_details' not in session:
        return redirect(url_for('merchant.business_structure'))
    
    return render_template('account-creation/business-create-brand.html')


@merchant_bp.route('/save-brand-details', methods=['POST'])
def save_brand_details():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    if 'business_type' not in session or 'business_details' not in session:
        return jsonify({"error": "Please complete previous steps first"}), 400
    
    brand_name = request.form.get('brand_name')
    
    if not brand_name:
        return jsonify({"error": "Brand name is required"}), 400
    
    session['brand_details'] = {
        'brand_name': brand_name
    }
    return jsonify({
        "message": "Brand details saved successfully",
        "redirect": "/dashboard"
    }), 200