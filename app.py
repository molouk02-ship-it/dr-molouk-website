from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = "dr_molouk_super_secret_key"

# Simulated Database
DATABASE = {
    "courses": [
        {"id": 1, "year": "1st", "subject": "Anatomy", "title": "Intro to Cardiovascular System", "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
        {"id": 2, "year": "2nd", "subject": "Pharmacology", "title": "Beta Blockers & Mechanisms", "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}
    ],
    "leaderboard": [
        {"student": "MedStudent_101", "points": 350},
        {"student": "FutureSurgeon", "points": 280}
    ]
}

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html', courses=DATABASE["courses"], leaderboard=DATABASE["leaderboard"])

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    score = data.get('score', 0)
    student_name = data.get('student_name', 'Guest Student')
    
    # Calculate points based on performance
    earned_points = score * 10
    DATABASE["leaderboard"].append({"student": student_name, "points": earned_points})
    DATABASE["leaderboard"] = sorted(DATABASE["leaderboard"], key=lambda x: x['points'], reverse=True)
    
    return jsonify({"status": "success", "earned_points": earned_points, "leaderboard": DATABASE["leaderboard"]})

@app.route('/admin/add-course', methods=['POST'])
def admin_add_course():
    # Restricted Admin Upload Route
    admin_key = request.headers.get('X-Admin-Key')
    if admin_key != "MOLOUK_ADMIN_2026":
        return jsonify({"status": "error", "message": "Unauthorized! Admin access only."}), 403
    
    data = request.json
    new_course = {
        "id": len(DATABASE["courses"]) + 1,
        "year": data.get("year"),
        "subject": data.get("subject"),
        "title": data.get("title"),
        "video_url": data.get("video_url")
    }
    DATABASE["courses"].append(new_course)
    return jsonify({"status": "success", "course": new_course})

if __name__ == '__main__':
    app.run(debug=True, port=5000)