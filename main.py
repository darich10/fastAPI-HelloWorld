# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# Fast API
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie
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


class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, lt=90, example=18)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


class PersonOut(PersonBase):
    pass


class Person(PersonBase):
    password: str = Field(..., min_length=8, example="holapassword")


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="Dario")
    message: str = Field(default="Login Successfully!")


@app.get(path="/",
         status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "world"}


@app.post(path="/person/new",
          response_model=PersonOut,
          status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person


# Validations: Query parameters
@app.get(path="/person/detail",
         status_code=status.HTTP_200_OK)
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

@app.put(path="/person/{person_id}",
         status_code=status.HTTP_202_ACCEPTED)
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


# Forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...,), password: str = Form(...)):
    return LoginOut(username=username)


# Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
        first_name: str = Form(
            ...,
            max_length=20,
            min_length=1
        ),
        last_name: str = Form(
            ...,
            max_length=20,
            min_length=1
        ),
        email: EmailStr = Form(...),
        message: str = Form(
            ...,
            min_length=20,
            max_length=500
        ),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None)
):
    return user_agent
