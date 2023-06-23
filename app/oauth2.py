from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas

SECRET_KEY = "6094be9a946b710e29306b4ae4215ee20bce7c8e882268bdacb739f33bc3cce1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPRIE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    exprie = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPRIE_MINUTES)
    to_encode.update({"exp": exprie})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        print(token)
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id)

        return token_data
    
    except JWTError as error:
        print(error)
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception=credentials_exception)