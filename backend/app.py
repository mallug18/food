# /backend/app.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import jwt
from supabase import create_client, Client

# --- SETUP ---
load_dotenv()
app = Flask(__name__)
# This specific CORS configuration is crucial for it to work with your Vue app
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# --- SUPABASE CLIENT INITIALIZATION ---
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") # Uses the secret service key
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
            "donor_id": user.get('sub') # 'sub' is the user ID from the JWT
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
        # Step 1: Create the request
        new_request = {
            "food_item_id": data.get('food_item_id'),
            "requester_id": user.get('sub'),
            "donor_id": data.get('donor_id')
        }
        request_response = supabase.table('requests').insert(new_request).execute()
        
        # Step 2: Update the food item's status to 'requested'
        supabase.table('food_items').update({"status": "requested"}).eq("id", data.get('food_item_id')).execute()
        
        return jsonify(request_response.data[0]), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/api/my-donations', methods=['GET'])
def get_my_donations():
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401
    
    # Fetch donations by the user, joining with requests and the requester's profile
    response = supabase.table('food_items').select('*, requests(*, profiles:requester_id(username, phone))').eq('donor_id', user.get('sub')).execute()
    
    return jsonify(response.data)

@app.route('/api/requests/<int:request_id>/approve', methods=['POST'])
def approve_request(request_id):
    user, error = get_user_from_token()
    if error:
        return jsonify(error), 401

    try:
        # Step 1: Find the request
        request_to_approve = supabase.table('requests').select('*').eq('id', request_id).single().execute()
        if not request_to_approve.data:
            return jsonify({"error": "Request not found"}), 404

        # Step 2: Security Check - Ensure the logged-in user is the donor
        if request_to_approve.data['donor_id'] != user.get('sub'):
            return jsonify({"error": "You are not authorized to approve this request"}), 403

        food_item_id = request_to_approve.data['food_item_id']

        # Step 3: Update the request status to 'approved'
        supabase.table('requests').update({"status": "approved"}).eq("id", request_id).execute()

        # Step 4: Update the food item status to 'claimed'
        supabase.table('food_items').update({"status": "claimed"}).eq("id", food_item_id).execute()
        
        return jsonify({"message": "Request approved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)