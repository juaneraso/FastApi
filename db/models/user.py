# from pydantic import BaseModel

# class User(BaseModel):
#     id:str | None
#     username: str
#     email: str

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
