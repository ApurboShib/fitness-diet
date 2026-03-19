from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()


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

def dave_info(data):
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