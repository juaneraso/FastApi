from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                   tags=["products"],
                   responses ={404 :{"message":"no encontrado"}})

product_list = ["Producto1","Producto2","Producto3","Producto4","Producto5"]

@router.get("/")
async def products():
    return product_list


@router.get("/{id}")
async def products(id:int):
    return product_list[id]