from jose import jwt
from fastapi import Request, HTTPException, Header

JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    

async def login_required(Authorization: str = Header()):
    try:
        bearer, auth_token = Authorization[:6], Authorization[7:]
        if bearer != "Bearer":
            raise HTTPException(status_code=401, detail="Not authenticated, Invalid Header")

        token = jwt.decode(auth_token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated, Invalid token")
    except:
        raise HTTPException(status_code=401, detail="Not authenticated, Invalid Authorization header")
    
    return token


def createToken(data: dict):
    token = jwt.encode(data, JWT_SECRET_KEY, algorithm="HS256")
    return token