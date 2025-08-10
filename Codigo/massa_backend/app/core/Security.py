from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import jwt
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from app.core.Config import get_environment_variables
from app.core.Dependencies import get_repository
from app.infrastructure.repositories.UserRepository import UserRepository

env_variables = get_environment_variables()
oauth2_scheme = HTTPBearer()

class JWTAuth:
    def create_access_token(self, user_id: int) -> str:
        payload = {"user_id": user_id, "exp": datetime.now(timezone.utc) + timedelta(seconds=env_variables.JWT_EXP_DELTA_SECONDS)}
        encoded_jwt = jwt.encode(payload, env_variables.JWT_SECRET, algorithm=env_variables.JWT_ALGORITHM)
        return encoded_jwt

    def __decode_access_token(self, token: str) -> Optional[Dict[str, int]]:
        try:
            decoded_token = jwt.decode(token, env_variables.JWT_SECRET, algorithms=[env_variables.JWT_ALGORITHM])
            exp_timestamp = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)

            return decoded_token if exp_timestamp >= datetime.now(timezone.utc) else None
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    async def get_current_user(self, token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
                               user_repository: UserRepository = Depends(get_repository(UserRepository))):
        payload = self.__decode_access_token(token.credentials)
        user_id = payload.get("user_id")

        user = await user_repository.get_user(user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

        return user

class PasswordHandler:

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)