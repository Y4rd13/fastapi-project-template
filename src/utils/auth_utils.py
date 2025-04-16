from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.auth import TokenData, UserInDB
from core.config import settings
from utils.mongo_utils import MongoDBUtils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
mongodb_client = MongoDBUtils(settings.MONGO_URI).get_client()
database = mongodb_client['YourDatabaseName']  # Replace with your database name

def get_user(username: str):
    user = database["users"].find_one({"username": username})
    if user:
        return UserInDB(**user)

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user