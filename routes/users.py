from fastapi import APIRouter , HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/users", 
                   tags=["users"],
                   responses ={404 :{"message":"no encontrado"}})


#entidad

class User(BaseModel):
    id:int
    name: str
    surname: str
    url:str
    age:int

users_list =[User(id = 1, name= "Juan", surname = "Eraso", url= "http://Mouredev.com",age= 35),
        User(id = 2, name= "Juan", surname = "Eraso", url= "http://Mouredev.com",age= 35),
        User(id = 3, name= "Juan", surname = "Eraso", url= "http://Mouredev.com",age= 35)]



@router.get("/json")
async def usersjson():
    return [{
        "nombre":"Juan"
    },
    {
        "nombre":"Juan"
    }]


@router.get("/")
async def users():
#    return User(name= "Juan",surname="Eraso",url="http:/holaa.com",age=29) 
   return users_list



# @router.get("/user/{id}")
# async def user(id : int):
    
#    return users_list[id-1]


#Path
@router.get("/{id}")
async def user(id : int):
    return search_user(id)
    # users = filter(lambda user: user.id == id , users_list)
    # try:
    #     return list(users)[0]
    # except:
    #     return {"error": "no se ha encontrado el usuario"}

# Query
@router.get("/query/")
async def user(id : int):
    return search_user(id)


@router.post("/", response_model = User, status_code=201)     # Con status code
async def user(user: User):
    print(type(search_user(user.id)))
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail= "Usuario ya existe")
     
    else:
        users_list.append(user)
        return user


@router.put("/")
async def user(user:User):
    found = False

    for  index , saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    
    else:
        return user
 
@router.delete("/{id}")
async def user(id: int):
  found  = False
  
  for  index , saved_user in enumerate(users_list):
     if saved_user.id == id:       
        user_delete = users_list[index]   # Linea agregada por mi
        del users_list[index]
        found = True
  if not found:
        return {"error": "No se ha eliminado el usuario"}
  
  else:
        return user_delete


def search_user(id:int):
    users = filter(lambda user: user.id == id , users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "no se ha encontrado el usuario"}
    