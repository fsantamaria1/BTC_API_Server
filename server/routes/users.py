from flask import request, jsonify
from flask import current_app as app
from server.resources import db, messages
from server.resources.models import User
from server.resources.decorators import token_required
from werkzeug.security import generate_password_hash
import uuid

@app.route('/user', methods=['GET'])
@token_required
def get_users(current_user):

    if not current_user.admin:
        return messages.CannotPerformThatAction()
    elif not current_user.active:
        return messages.CannotPerformThatAction()

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['manager'] = user.manager
        user_data['admin'] = user.admin
        user_data['active'] = user.active
        output.append(user_data)
    # return jsonify({'users': output})
    users_data_message = messages.ApiMessage(200, "success", {'users': output})
    return users_data_message()

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    if not current_user.admin:
        return messages.CannotPerformThatAction()
    elif not current_user.active:
        return messages.CannotPerformThatAction()

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

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return messages.CannotPerformThatAction()
    elif not current_user.active:
        return messages.CannotPerformThatAction()

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return messages.UserDoesNotExist()

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['manager'] = user.manager
    user_data['admin'] = user.admin
    user_data['active'] = user.active

    # return jsonify({'user': user_data})
    user_data_message = messages.ApiMessage(200, "success", {'user': user_data})
    return user_data_message()

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):

    if not current_user.admin:
        return messages.CannotPerformThatAction()
    elif not current_user.active:
        return messages.CannotPerformThatAction()

    #Get data from request
    try:
        data = request.get_json()
        if not data.get("promotion"):
            return messages.NoPromotionFound()
    except:
         return messages.NoDataFound()

    #Query database to see if user exists
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return messages.UserDoesNotExist()

    #Promote User 
    if data.get("promotion") == "admin":
        user.admin = True
    elif data.get("promotion") == "manager":
        user.manager = True
    elif data.get("promotion") == "inactive":
        user.active = False
    else:
        return messages.NoValidPromotionFound()
    db.session.commit()
    return messages.UserPromoted()

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return messages.CannotPerformThatAction()
    elif not current_user.active:
        return messages.CannotPerformThatAction()

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return messages.UserDoesNotExist()

    db.session.delete(user)
    db.session.commit()

    return messages.UserDeleted()
