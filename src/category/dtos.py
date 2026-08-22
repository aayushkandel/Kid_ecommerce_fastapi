from pydantic import BaseModel

class CategoryBase(BaseModel):

    name:str
    slug:str
    description:str