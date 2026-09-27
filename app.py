from flask import Flask, render_template, request, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'dr_molouk_secret_key_2026'

ADMIN_EMAIL = "molouk08@hotmail.com"
DATA_FILE = 'app_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "users": {},
        "subjects": [],
        "quizzes": [],
        "videos": []
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user, admin_email=ADMIN_EMAIL)

@app.route('/api/data', methods=['GET'])
def get_data():
    db = load_data()
    return jsonify({
        "subjects": db["subjects"],
        "quizzes": db["quizzes"],
        "videos": db["videos"]
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    name = data.get('name')
    pin = data.get('pin')

    if not email or not password or not pin:
        return jsonify({"success": False, "message": "All fields required"}), 400

    db = load_data()
    if email in db["users"]:
        return jsonify({"success": False, "message": "User already exists"}), 400

    is_admin = (email == ADMIN_EMAIL.lower())
    db["users"][email] = {
        "name": name,
        "password": password,
        "security_pin": pin,
        "is_admin": is_admin
    }
    save_data(db)
    
    session['user'] = {"email": email, "name": name, "is_admin": is_admin}
    return jsonify({"success": True, "user": session['user']})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password')

    db = load_data()
    user = db["users"].get(email)

    if not user or user["password"] != password:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    session['user'] = {
        "email": email, 
        "name": user["name"], 
        "is_admin": (email == ADMIN_EMAIL.lower())
    }
    return jsonify({"success": True, "user": session['user']})

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email', '').strip().lower()
    pin = data.get('pin')
    new_password = data.get('new_password')

    db = load_data()
    user = db["users"].get(email)

    if not user:
        return jsonify({"success": False, "message": "Email not found"}), 404

    if user.get("security_pin") != pin:
        return jsonify({"success": False, "message": "Incorrect Security PIN"}), 401

    user["password"] = new_password
    save_data(db)
    return jsonify({"success": True, "message": "Password reset successfully!"})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True})

@app.route('/api/admin/add-subject', methods=['POST'])
def add_subject():
    user = session.get('user')
    if not user or not user.get('is_admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    data = request.json
    db = load_data()
    new_subject = {
        "id": len(db["subjects"]) + 1,
        "name": data.get("name"),
        "year": data.get("year")
    }
    db["subjects"].append(new_subject)
    save_data(db)
    return jsonify({"success": True, "subjects": db["subjects"]})

@app.route('/api/admin/add-quiz', methods=['POST'])
def add_quiz():
    user = session.get('user')
    if not user or not user.get('is_admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    data = request.json
    db = load_data()
    new_quiz = {
        "id": len(db["quizzes"]) + 1,
        "subject_id": data.get("subject_id"),
        "title": data.get("title"),
        "questions": data.get("questions", [])
    }
    db["quizzes"].append(new_quiz)
    save_data(db)
    return jsonify({"success": True, "quizzes": db["quizzes"]})

@app.route('/api/admin/add-video', methods=['POST'])
def add_video():
    user = session.get('user')
    if not user or not user.get('is_admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    data = request.json
    db = load_data()
    new_video = {
        "id": len(db["videos"]) + 1,
        "subject_id": data.get("subject_id"),
        "title": data.get("title"),
        "url": data.get("url")
    }
    db["videos"].append(new_video)
    save_data(db)
    return jsonify({"success": True, "videos": db["videos"]})

if __name__ == '__main__':
    app.run(debug=True)