from fastapi import FastAPI
from routes import products , users , basic_auth_users , jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# print("database")

#Routers

app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.include_router(users_db.router)


app.mount("/statics",StaticFiles(directory="static"),name = "static") #ruta /statics

@app.get("/")
async def root():
    return "¡Hola amigos como estan!"

@app.get("/url")
async def root():
    return {"url_curso":"hpttps://holaamigos.com",
            "nombre":"Juan"
            }


## Inicar el servidor 
## uvicorn main:app --reload