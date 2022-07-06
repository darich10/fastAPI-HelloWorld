# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# Fast API
from fastapi import FastAPI
from fastapi import Body, Query, Path
import uvicorn

app = FastAPI()


# Models creation
class Location(BaseModel):
    city: str
    state: str
    country: str


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, lt=90)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(..., min_length=8)


class PersonOut(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, lt=90)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


@app.get("/")
def home():
    return {"Hello": "world"}


@app.post("/person/new", response_model=PersonOut)
def create_person(person: Person = Body(...)):
    return person


# Validations: Query parameters
@app.get("/person/detail")
def show_person(
        name: str = Query(None,
                          min_length=1,
                          max_length=50,
                          title="Person Name",
                          description="This is the person name. It's between 1 and 50 characters"
                          ),
        age: str = Query(...,
                         title="Person Age",
                         description="This is the person age. It's required"
                         )
):
    return {"name": name,
            "age": age}


# Validations: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(...,
                              ge=0,
                              title="Person Number Identification",
                              description="Brings if an person already exists"
                              )
):
    return {
        person_id: "It exists!"
    }


# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            ...,
            title="Person ID",
            description="This is the person ID",
            gt=0
        ),
        person: Person = Body(...),
        location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
