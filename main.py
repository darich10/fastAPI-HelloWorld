# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# Fast API
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()


class Location(BaseModel):
    city: str
    state: str
    country: str


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
