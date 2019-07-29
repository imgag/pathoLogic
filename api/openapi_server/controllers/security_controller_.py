import os
import json
from urllib.request import urlopen

from flask import current_app
from jose import jwt, exceptions
from werkzeug.exceptions import Unauthorized

AUTH_DOMAIN = os.getenv('AUTH_DOMAIN', 'auth.imgag.de')
ALGORITHMS = ['RS256']
REALM = os.getenv('AUTH_REALM', 'debug')


def info_from_jwt(token):
    """
    Check and retrieve authentication information from custom bearer token.
    Returned value will be passed in 'token_info' parameter of your operation function, if there is one.
    'sub' or 'uid' will be set in 'user' parameter of your operation function, if there is one.

    :param token Token provided by Authorization header
    :type token: str
    :return: Decoded token information or None if token is invalid
    :rtype: dict | None
    """

    # NOTE: Implements validation as suggested on the Auth0 site at
    # https://auth0.com/docs/quickstart/backend/python/01-authorization#validate-access-tokens
    json_url = urlopen(
        'https://{}/auth/realms/{}/protocol/openid-connect/certs'.format(AUTH_DOMAIN, REALM))
    jwks = json.loads(json_url.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

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
                issuer='https://{}/auth/realms/{}'.format(AUTH_DOMAIN, REALM)
            )
        except jwt.ExpiredSignatureError:
            raise Unauthorized(
                {'code': 'token_expired', 'description': 'token is expired'})
        except jwt.JWTClaimsError as err:
            current_app.logger.error(err)
            raise Unauthorized(
                {'code': 'invalid_claims', 'description': 'incorrect claims'})
        except exceptions.JWSError as err:
            current_app.logger.error(err)
            raise Unauthorized(
                {'code': 'invalid_header', 'description': 'Unable to parse authentication token'})
        except exceptions.JWTError as err:
            current_app.logger.error(err)
            raise Unauthorized(
                {'code': 'invalid_header', 'description': 'Unable to parse authentication token'})

        return payload
