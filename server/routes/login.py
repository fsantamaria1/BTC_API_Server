from flask import current_app as app
from flask import request, jsonify
from server.resources import messages
from server.resources.models import User
from werkzeug.security import check_password_hash
import jwt
import datetime

@app.route('/login')
def login():
    auth = request.authorization

    # Authorization information does not exist
    if not auth or not auth.username or not auth.password:
        return messages.CouldNotVerify()

    user = User.query.filter_by(username=auth.username).first()
    ## Figure out what type user is
    print(user)

    # User does not exist
    if not user:
        return messages.UserDoesNotExist()

    # Check if the password matches
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        # return jsonify({'token': token})
        success_message = messages.ApiMessage(200, "success", {"token": token})
        return success_message()

    # Password does not exist or is invalid
    return messages.InvalidCredentials()