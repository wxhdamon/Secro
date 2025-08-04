#/ backend/app/routes.py
from flask import Blueprint, request, jsonify, render_template
from .license import check_license
from .scanner import run_scan
from .models import save_scan_result

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/api/scan', methods=['POST'])
def scan():
    if not check_license():
        return jsonify({'error': 'Invalid or expired license'}), 403
    try:
        result = run_scan()
        save_scan_result(result)
        return jsonify({'status': 'Scan completed', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
