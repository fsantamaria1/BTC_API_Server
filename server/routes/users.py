from flask import request, jsonify
from flask import current_app as app
from server.resources import db, messages
from server.resources.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['manager'] = user.manager
        user_data['admin'] = user.admin
        user_data['active'] = user.active
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/user', methods=['POST'])
def create_user():
    try:
        # Get data from request
        data = request.get_json()
        if not data.get("username"):
            return messages.NoUsernameFound()
        elif not data.get("password"):
            return messages.NoPasswordFound()
        elif (len(data.get("username")) <4) or (len(data.get("username")) >= 20):
            return messages.UsernameTooShort()
        elif len(data.get("password")) <5:
            return messages.PasswordTooShort()
    except:
        return messages.NoDataFound()

    # Query dabatase to see if the username already exists
    existing_user = User.query.filter_by(username=data["username"]).first()

    if not existing_user:
        hashed_password= generate_password_hash(data['password'], method='sha256')
        #Create new user
        new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, manager=False, admin=False, active=True)
        db.session.add(new_user)
        db.session.commit()
        return messages.UserCeated()
    else:
        return messages.UserAlreadyExists()


