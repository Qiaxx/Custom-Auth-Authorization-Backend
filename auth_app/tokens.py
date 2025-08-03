import datetime

import jwt
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
TOKEN_TTL_SECONDS = 60 * 60 * 24  # 1 день


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(seconds=TOKEN_TTL_SECONDS),
        "iat": datetime.datetime.now(datetime.UTC),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
