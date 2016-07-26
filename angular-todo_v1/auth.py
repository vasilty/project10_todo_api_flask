from flask import g, jsonify, make_response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

import models

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')
auth = MultiAuth(token_auth, basic_auth)


@basic_auth.verify_password
def verify_password(username, password):
    """Verifies username + password."""
    try:
        user = models.User.get(models.User.username ** username)
        if not user.verify_password(password):
            return False
    except models.User.DoesNotExist:
        return False
    else:
        g.user = user
        return True


@token_auth.verify_token
def verify_token(token):
    """Verifies token."""
    user = models.User.verify_auth_token(token)
    if user is not None:
        g.user = user
        return True
    return False


@basic_auth.error_handler
def unauthorized():
    """Handles an unauthorized error. 403 status code ("Forbidden") is returned
    instead of 401 ("Unauthorized") to avoid a browser authentication dialog.
    """
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)