import os
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import Flask, request, jsonify, make_response, g, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

app = Flask(__name__)
PORT = int(os.getenv('PORT', 5000))
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY', 'default-refresh-secret')

# Setup CORS: allow credentials for HttpOnly Cookie
CORS(app, supports_credentials=True, origins=["*"])

# --- Mock User Database ---
users = {
    'admin': {
        'id': 1,
        'username': 'admin',
        'password': 'password123',
        'role': 'admin',
        'scopes': ['read:profile', 'read:admin_data', 'write:admin_data']
    },
    'user': {
        'id': 2,
        'username': 'user',
        'password': 'password456',
        'role': 'student',
        'scopes': ['read:profile']
    }
}

# --- Middleware (Decorators): Verify Access Token ---
def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Priority: Cookie -> Authorization Header
        token = request.cookies.get('access_token')
        
        if not token and 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Authentication required'}), 401
        
        try:
            # Decode token
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            g.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 403
            
        return f(*args, **kwargs)
    return decorated

# --- Middleware: RBAC (Roles) ---
def authorize_roles(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.user.get('role') not in roles:
                return jsonify({'message': f"Forbidden: Role {g.user.get('role')} not authorized"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

# --- Auth Endpoints ---

@app.route('/')
def index():
    return send_file('index.html')

# ✅ CHẾ ĐỘ 1: ĐĂNG NHẬP KHÔNG AN TOÀN (LỘ TOKEN)
@app.route('/api/login-insecure', methods=['POST'])
def login_insecure():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    
    if user and user['password'] == password:
        # Create Access Token (expires in 15m)
        access_token_payload = {
            'id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'scopes': user['scopes'],
            'exp': datetime.now(timezone.utc) + timedelta(minutes=15)
        }
        access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm='HS256')
        
        # Create Refresh Token (expires in 7d)
        refresh_token_payload = {
            'id': user['id'],
            'exp': datetime.now(timezone.utc) + timedelta(days=7)
        }
        refresh_token = jwt.encode(refresh_token_payload, REFRESH_SECRET_KEY, algorithm='HS256')
        
        # TRẢ VỀ TOKEN TRONG BODY -> DẪN ĐẾN RỦI RO LỘ TOKEN (TOKEN LEAKAGE)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

# ✅ CHẾ ĐỘ 2: ĐĂNG NHẬP AN TOÀN (DÙNG HTTPONLY COOKIE)
@app.route('/api/login-secure', methods=['POST'])
def login_secure():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    
    if user and user['password'] == password:
        # Create Access Token
        access_token_payload = {
            'id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'scopes': user['scopes'],
            'exp': datetime.now(timezone.utc) + timedelta(minutes=15)
        }
        access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm='HS256')
        
        # ĐẶT TOKEN VÀO COOKIE HTTPONLY (KHÔNG THỂ BỊ JAVASCRIPT ĐỌC)
        response = make_response(jsonify({'message': 'Logged in securely with HttpOnly Cookie'}))
        response.set_cookie(
            'access_token',
            value=access_token,
            httponly=True,  # Ngăn chặn XSS
            secure=False,   # Để false cho Demo Local (HTTPS thì true)
            samesite='Lax', # Tương đương 'strict' trong Node.js demo hoặc tùy nhu cầu
            max_age=15 * 60 # 15 phút (giây)
        )
        return response
        
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logged out'}))
    response.delete_cookie('access_token')
    return response

# --- Protected Resources ---

@app.route('/api/profile', methods=['GET'])
@verify_token
def get_profile():
    return jsonify({
        'user': g.user,
        'message': 'Welcome to your protected profile!'
    })

@app.route('/api/admin-only', methods=['GET'])
@verify_token
@authorize_roles('admin')
def get_admin_data():
    return jsonify({
        'message': 'Access granted: Secret admin data retrieved!'
    })

if __name__ == '__main__':
    print(f"Flask Auth Server is running on http://localhost:{PORT}")
    app.run(port=PORT, debug=True)
