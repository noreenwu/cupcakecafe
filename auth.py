import json
import base64
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
# from exceptions import JWTError
from urllib.request import urlopen


AUTH0_DOMAIN = 'wudev.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'cupcakecafe'


# -------------------------------------------------------------
# AuthError Exception
#   A standardized way to communicate auth failure modes
# -------------------------------------------------------------
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# --------------------------------------------------------------
#  get_token_auth_header() method:
#     gets the header from the request
#         and aborts with AuthError if no header is present
#     it splits the bearer and the token
#         and aborts with AuthError if the header is malformed
#     it return the token part of the header
# --------------------------------------------------------------
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        print("authorization header missing")
        abort(401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        print("authorization header must start with Bearer")
        abort(401)

    elif len(parts) == 1:
        print("Token not found")
        abort(401)

    elif len(parts) > 2:
        print("Invalid header: authorization header must be bearer token")
        abort(401)

    token = parts[1]
    return token


# --------------------------------------------------------------
#   check_permissions(permission, payload) method
#     @INPUTS
#         permission: string permission (i.e. 'post:drink')
#         payload: decoded jwt payload
#
#     if permissions are not included in the payload,
#         abort with AuthError (400)
#
#     if the requested permission string is not in the
#         abort with AuthError (403)
#
#     return true if specified permission is present in payload
# --------------------------------------------------------------
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        print("permissions not in payload")
        abort(403)

    if permission not in payload['permissions']:
        abort(403)

    return True


# --------------------------------------------------------------
#   verify_decode_jwt(token) method
#     @INPUTS
#         token: a json web token (string)
#
#     it should be an Auth0 token with key id (kid)
#     it should verify the token using Auth0 /.well-known/jwks.json
#     it should decode the payload from the token
#     it should validate the claims
#     return the decoded payload
# --------------------------------------------------------------
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        print("Invalid jwt")
        abort(401)

    rsa_key = {}
    if 'kid' not in unverified_header:
        print("invalid header")
        abort(401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            print("Token expired")
            abort(401)
        except jwt.JWTClaimsError:
            print("Incorrect claims. Please check audience and issuer")
            abort(401)
        except Exception:
            print("Unable to parse authentication token")
            abort(400)

    print("Unable to find the appropriate key", rsa_key)
    abort(400)


# --------------------------------------------------------------
# @requires_auth(permission) decorator method
#     @INPUTS
#         permission: string permission (i.e. 'post:drink')
#
#     it should use the get_token_auth_header method to get the token
#     it should use the verify_decode_jwt method to decode the jwt
#     it should use the check_permissions method validate claims and
#     check the requested permission
#     return the decorator which passes the decoded payload to the
#     decorated method
# --------------------------------------------------------------
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
