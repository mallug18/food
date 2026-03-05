import os
import uuid
import base64
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import jwt
from supabase import create_client, Client

# --- SETUP ---
load_dotenv()
app = Flask(__name__)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === THIS IS THE CORRECT, FINAL CORS SETUP ===
# It reads the allowed frontend URL from an environment variable.
frontend_url = os.environ.get('FRONTEND_URL')
if frontend_url:
    CORS(app, origins=frontend_url)
else:
    # Allows all origins if FRONTEND_URL is not set (useful for initial tests)
    CORS(app)
# ===============================================

# --- SUPABASE CLIENT INITIALIZATION ---
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase_jwt_secret = os.environ.get("SUPABASE_JWT_SECRET")
supabase: Client = create_client(supabase_url, supabase_key)

# --- HELPER FUNCTION FOR AUTHENTICATION ---
def get_user_from_token():
    """Helper function to decode and validate the JWT from the request header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, {"error": "Missing or invalid Authorization header"}
    
    token = auth_header.split(' ')[1]
    try:
        decoded_token = jwt.decode(
            token, supabase_jwt_secret, algorithms=["HS256"], audience='authenticated'
        )
        return decoded_token, None
    except Exception as e:
        return None, {"error": str(e)}

# --- API ENDPOINTS ---
@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/profile', methods=['GET', 'POST'])
def handle_profile():
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401
    
    if request.method == 'GET':
        try:
            profile_resp = supabase.table('profiles').select('username, phone, location, avatar_url').eq('id', user.get('sub')).single().execute()
            if profile_resp.data:
                return jsonify(profile_resp.data), 200
            return jsonify({"error": "Profile not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Handle POST
    data = request.get_json()
    phone = data.get('phone')
    username = data.get('username')
    location = data.get('location')
    profile_picture_base64 = data.get('profile_picture_base64')
    
    update_data = {}
    if phone is not None: update_data['phone'] = phone
    if username is not None: update_data['username'] = username
    if location is not None: update_data['location'] = location
        
    avatar_url = None
    if profile_picture_base64:
        try:
            # Generate a unique filename
            filename = f"{user.get('sub')}_{uuid.uuid4().hex[:8]}.jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Remove header if present (e.g., "data:image/jpeg;base64,")
            if ',' in profile_picture_base64:
                profile_picture_base64 = profile_picture_base64.split(',')[1]
                
            # Decode and save the image
            image_data = base64.b64decode(profile_picture_base64)
            with open(filepath, 'wb') as f:
                f.write(image_data)
                
            # Create the URL to access the image
            base_url = request.host_url.rstrip('/')
            avatar_url = f"{base_url}/uploads/{filename}"
            # Add to user metadata via Supabase Admin (or just return it to frontend to update auth user)
        except Exception as e:
            return jsonify({"error": f"Failed to save image: {str(e)}"}), 500

    if avatar_url:
        update_data['avatar_url'] = avatar_url

    if update_data:
        try:
            supabase.table('profiles').update(update_data).eq('id', user.get('sub')).execute()
            # Also update auth.users metadata for username if it changed
            if username or avatar_url:
                metadata_update = {}
                if username: metadata_update['username'] = username
                if avatar_url: metadata_update['avatar_url'] = avatar_url
                # Note: Updating auth user metadata generally requires the admin key
                # We'll just rely on the frontend to update its local session metadata. 
                pass
        except Exception as e:
            return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500
            
    return jsonify({"message": "Profile updated successfully", "avatar_url": avatar_url, "updated_fields": update_data}), 200

@app.route('/api/food-items', methods=['POST'])
def share_food_item():
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401
    data = request.get_json()
    if not all(key in data for key in ['name', 'quantity', 'location']):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        new_item = {
            "name": data.get('name'),
            "quantity": data.get('quantity'),
            "location": data.get('location'),
            "donor_id": user.get('sub')
        }
        response = supabase.table('food_items').insert(new_item).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/food-items', methods=['GET'])
def get_available_food_items():
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401
    response = supabase.table('food_items').select('*').eq('status', 'available').execute()
    return jsonify(response.data)

@app.route('/api/requests', methods=['POST'])
def create_request():
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401
    data = request.get_json()
    if not all(key in data for key in ['food_item_id', 'donor_id']):
        return jsonify({"error": "food_item_id and donor_id are required"}), 400
    try:
        new_request = {
            "food_item_id": data.get('food_item_id'),
            "requester_id": user.get('sub'),
            "donor_id": data.get('donor_id')
        }
        request_response = supabase.table('requests').insert(new_request).execute()
        supabase.table('food_items').update({"status": "requested"}).eq("id", data.get('food_item_id')).execute()
        return jsonify(request_response.data[0]), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/my-donations', methods=['GET'])
def get_my_donations():
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401
    response = supabase.table('food_items').select('*, requests(*, profiles:requester_id(username, phone))').eq('donor_id', user.get('sub')).execute()
    return jsonify(response.data)

@app.route('/api/incoming-requests', methods=['GET'])
def get_incoming_requests():
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401
    try:
        # Get all requests where the food item belongs to the logged in user
        # We need to query requests and join with food_items where food_items.donor_id = user.id
        # Supabase Python client can filter on embedded tables, but it's easier to:
        # 1. Get user's food items
        food_items_resp = supabase.table('food_items').select('id, name, quantity, location').eq('donor_id', user.get('sub')).execute()
        food_ids = [item['id'] for item in food_items_resp.data]
        
        if not food_ids:
            return jsonify([])
            
        # 2. Get requests for those food items
        requests_resp = supabase.table('requests').select('*, food_items(*), profiles:requester_id(username, phone)').in_('food_item_id', food_ids).execute()
        return jsonify(requests_resp.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/requests/<int:request_id>/approve', methods=['POST'])
def approve_request(request_id):
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401
    try:
        request_to_approve = supabase.table('requests').select('*').eq('id', request_id).single().execute()
        if not request_to_approve.data:
            return jsonify({"error": "Request not found"}), 404
        if request_to_approve.data['donor_id'] != user.get('sub'):
            return jsonify({"error": "You are not authorized to approve this request"}), 403
        food_item_id = request_to_approve.data['food_item_id']
        supabase.table('requests').update({"status": "approved"}).eq("id", request_id).execute()
        supabase.table('food_items').update({"status": "claimed"}).eq("id", food_item_id).execute()
        return jsonify({"message": "Request approved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Public health check endpoint — no auth required."""
    return jsonify({"status": "ok", "message": "WasteFood API is running"}), 200

@app.route('/api/stats', methods=['GET'])
def get_public_stats():
    """Return public platform stats for the home page."""
    try:
        food_resp = supabase.table('food_items').select('id', count='exact').execute()
        requests_resp = supabase.table('requests').select('id', count='exact').execute()
        return jsonify({
            "total_donations": food_resp.count or 0,
            "total_requests": requests_resp.count or 0,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)