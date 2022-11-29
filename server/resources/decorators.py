from flask import current_app as app
import jwt
from functools import wraps
from flask import request
from server.resources import messages
from server.resources.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return messages.TokenIsMissing()

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return messages.InvalidToken()

        return f(current_user, *args, **kwargs)
    return decorated