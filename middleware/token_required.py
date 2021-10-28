from flask import request, jsonify
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        from database.models import User
        from RowingBoat.config import Config

        config = Config()
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
    
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])            
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
    
        return f(current_user, *args, **kwargs)
    return decorator