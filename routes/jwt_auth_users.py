from fastapi import APIRouter, Depends,HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone



ALGORITMO = "HS256"
ACCES_TOKEN_DURATION = 1
SECRET = "dbabb3973961a51510e4b81d4756d6fa0056023d0ff91cead124a399f1851599"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):    
    username: str
    full_name: str    
    email:str
    disabled:bool

class UserDB(User):  #Herencia
    password: str


users_db = {
    "juangui":{
       "username": "juangui",
       "full_name": "Juan Eraso",
       "email":"juan@gmail.com",
       "disabled":False,
       "password":"$2a$12$/i.coGeuAPZG0ZFbqhmTIOMp1/yERNwJbqVoy14Otb6sumv2AVZ.i"
     },
    "juangui2":{
       "username": "juangui2",
       "full_name": "Juan Eraso2",
       "email":"juan2@gmail.com",
       "disabled":True,
       "password":"$2a$12$SaDquqbpPgZnXV.6AadOfuilGmpn2x9xcHQ.aLvquYzBrSULEEajC"
    }
}


def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):
    exception =  HTTPException(status_code = 401, detail= "Credenciales invalidas", headers={"www-Authentiticate" : "Bearer"})

    try:
       username = jwt.decode(token,SECRET,algorithms=[ALGORITMO]).get("sub")
       if username is None : 
            raise exception

    


    except JWTError:
            raise exception
    
    return search_user(username)

    
async def current_user(user : User = Depends(auth_user)):   # El token es el propio usuario de la base de datos
         
    if user.disabled:
       raise HTTPException(status_code = 400, detail= "Usuario inactivo")
     
    return user 


@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
   user_db = users_db.get(form.username) 
   if not user_db : 
       raise HTTPException(status_code=400, detail= "El usuario no es correcto")
   
   user = search_user_db(form.username)
  

   if not  crypt.verify(form.password, user.password): 
       raise HTTPException(status_code=400, detail= "La contraseña no es correcta")
   
   
#    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCES_TOKEN_DURATION)

   acces_token = {
        "sub":user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCES_TOKEN_DURATION),

   }

   return {"access_token" : jwt.encode(acces_token, SECRET, algorithm = ALGORITMO) ,"token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
