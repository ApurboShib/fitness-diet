from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

# create a pydantic baseModel

class Person(BaseModel):
    id : Annotated[str, Field(..., description="Unique ID of the person")]
    name : Annotated[str, Field(..., description="Name of the person")]
    age : Annotated[int, Field(...,gt=0, lt=120, description="Age of the person")]
    height : Annotated[float, Field(...,gt=0, description="Height of the person in cm")]
    weight : Annotated[float, Field(...,gt=0, description="Weight of the person in kg")]
    mental_health : Annotated[int, Field(..., description="Mental health score of the person on a scale of 1 to 10")]
    workout : Annotated[int, Field(..., description="Number of workouts per week")]
    has_personal_trainer : Annotated[bool, Field(..., description="Whether the person has a personal trainer or not")]
    calories : Annotated[int, Field(..., description="Daily calorie intake of the person")]
    diet : Annotated[str, Field(..., description="Diet type followed by the person")]
    gender : Annotated[str, Field(..., description="Gender of the person")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height  ** 2)

    @computed_field
    @property
    def health_score(self) -> float:
        # Calculate health score based on various factors
        score = 0

        # Age factor
        if self.age < 30:
            score += 20
        elif self.age < 50:
            score += 10
        else:
            score += 5

        # BMI factor
        if self.bmi < 18.5:
            score += 10
        elif self.bmi < 25:
            score += 20
        elif self.bmi < 30:
            score += 10
        else:
            score += 5

        # Mental health factor
        score += self.mental_health * 2

        # Workout factor
        if self.workout >= 5:
            score += 20
        elif self.workout >= 3:
            score += 10
        else:
            score += 5

        # Personal trainer factor
        if self.has_personal_trainer:
            score += 10

        return score

@app.get('/')
def home():
    return {"messege" : "Personal Fitness & Diet Recommender System "}

# About of my app.

@app.get('/about')
def about():
    return "The Personal Fitness & Diet Recommender System is an end-to-end machine learning–powered web application designed to help users make informed decisions about their health and nutrition. The system collects user fitness data, analyzes key health indicators, and recommends an optimal diet plan using a trained ML model. This project integrates machine learning, backend API development, and interactive frontend design to simulate a real-world intelligent health assistant."

# build a helper function to load the data.
def load_data():
   with open ('personal_info.json', 'r') as f:
       data = json.load(f)
   return data

# save the data

def save_info(data):
    with open ('personal_info.json','w') as f:
        json.dump(data,f)

# now we build the view endpoints

@app.get('/view')
def view():
    data = load_data()
    return data

# build the endpointsn with  path parameter.

@app.get('/view/{person_id}')
def view_person(person_id : str = Path(..., description="this is a unique ID of the person")):
    data = load_data()

    for person in data:
        if person.get("id") == person_id:
            return person
            
    raise HTTPException(status_code=404, detail="Person is not found")
    
                

# implemet the sorting and ordering of the data.

@app.get('/sort')
def sort_data(sort_by:str = Query(..., description="Sort on the basis of height and weight"), order:str = Query(..., description="You can order it ASC or DESC wise.")):
    Valid_feilds = ['height', 'weight', 'bmi']
    Valid_order = ['ASC', 'DESC']

    if sort_by not in Valid_feilds:
        raise HTTPException(status_code=400, detail= f"Invalid field selected. choose {Valid_feilds} ")
    if order not in Valid_order:
        raise HTTPException(status_code=400, detail="Invalid Order selected.")
    
    data = load_data()

    # DESC means reverse should be True. ASC means False.
    reverse_order = True if order == 'DESC' else False

    # data is a list object so we don't use .values()
    response_data = sorted(data, key = lambda x : x.get(sort_by, 0), reverse = reverse_order)
    return response_data

# build a post endpoint to add the data.
@app.post('/create')
def create_user(person : Person):
    data = load_data()
    for existing_person in data:
        if existing_person.get("id") == person.id:
            raise HTTPException(status_code=400, detail="Person with this ID already exists.")
            
    person_dict = person.model_dump()
    data.append(person_dict)
    save_info(data)
    return JSONResponse(content={"message": "Person added successfully."}, status_code=201)