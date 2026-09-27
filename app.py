# Add this route to your app.py file

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email', '').strip().lower()
    security_pin = data.get('pin')
    new_password = data.get('new_password')

    db = load_data()
    user = db["users"].get(email)

    if not user:
        return jsonify({"success": False, "message": "Email not found"}), 404

    # Verify security PIN matches what they entered when registering
    if user.get("security_pin") != security_pin:
        return jsonify({"success": False, "message": "Incorrect Security PIN"}), 401

    # Update password
    user["password"] = new_password
    save_data(db)

    return jsonify({"success": True, "message": "Password updated successfully!"})