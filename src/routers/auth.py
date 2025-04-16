from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.auth import Token, TokenData, User, UserInDB
from core.config import settings
from utils.mongo_utils import MongoDBUtils

router = APIRouter()

# Security configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB setup
mongodb_client = MongoDBUtils(settings.MONGO_URI).get_client()
database = mongodb_client['YourDatabaseName']  # Replace with your database name
users_collection = database['users']  # Replace with your collection name

def get_user(username: str):
    """Retrieve a user from MongoDB by username."""
    user = users_collection.find_one({"username": username})
    if user:
        return UserInDB(**user)

def authenticate_user(username: str, password: str):
    """Authenticate user by username and password."""
    user = get_user(username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT token."""
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Generate an access token for a valid user."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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

@router.post("/register", response_model=User)
async def register_user(new_user: UserInDB, current_user: User = Depends(read_users_me)):
    """Register a new user (only accessible to superusers)."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can create new users.",
        )
    
    new_user.hashed_password = pwd_context.hash(new_user.hashed_password)
    new_user.is_active = True
    
    try:
        users_collection.insert_one(new_user.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    return new_user