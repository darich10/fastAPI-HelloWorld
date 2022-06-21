# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# Fast API
from fastapi import FastAPI
from fastapi import Body, Query

app = FastAPI()


# Models creation
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"Hello": "World"}


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validations: Query parameters
@app.get("/person/detail")
def show_person(
        name: Optional[str] = Query(None, min_length=1, max_length=50),
        age: int = Query(...)
):
    return {"name": name,
            "age": age}
