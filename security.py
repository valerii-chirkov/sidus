from config import SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials


class JWTConfig:
    def generate_token(data: dict, expires_data: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_data:
            expire = datetime.utcnow() + expires_data
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    def decode_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decode_token if decode_token["expires"] >= datetime.time() else None
        except:
            return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=400, detail="Invalid authentication scheme")
            if self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorisation code")

    def verify_jwt(self, jwttoken: str):
        is_token_valid: bool = True

        try:
            payload = jwt.decode(jwttoken, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            payload = None

        if payload:
            is_token_valid = True
        return is_token_valid