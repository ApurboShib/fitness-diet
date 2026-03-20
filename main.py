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


# updated pydantic model with computed fields.

class Updated_Person(Person):
    id : Annotated[Optional[str], Field(None, description="Unique ID of the person")]
    name : Annotated[Optional[str], Field(None, description="Name of the person")]
    age : Annotated[Optional[int], Field(None,gt=0, lt=120, description="Age of the person")]
    height : Annotated[Optional[float], Field(None,gt=0, description="Height of the person in cm")]
    weight : Annotated[Optional[float], Field(None,gt=0, description="Weight of the person in kg")]
    mental_health : Annotated[Optional[int], Field(None, description="Mental health score of the person on a scale of 1 to 10")]
    workout : Annotated[Optional[int], Field(None, description="Number of workouts per week")]
    has_personal_trainer : Annotated[Optional[bool], Field(None, description="Whether the person has a personal trainer or not")]
    calories : Annotated[Optional[int], Field(None, description="Daily calorie intake of the person")]
    diet : Annotated[Optional[str], Field(None, description="Diet type followed by the person")]

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

# add the endpoints to recommend the diet plan.

@app.get('/recommend/{person_id}')
def recommend_diet(person_id: str):
    data = load_data()
    for person in data:
        if person.get("id") == person_id:
            return {"person_id": person_id, "recommended_diet": person.get("diet")}
    raise HTTPException(status_code=404, detail="Person not found.")



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

# create a put endpoint to update the data.
@app.put('/update/{person_id}')
def update_person(person_id: str, updated_person: Updated_Person):
    data = load_data()

    # Find the person in the list
    for person in data:
        if person.get("id") == person_id:
            existing_person_info = person
            break
    else:
        raise HTTPException(status_code=404, detail="Person not found.")

    updated_data = updated_person.model_dump(exclude_unset=True)
    # Update the existing person dictionary
    for key, value in updated_data.items():
        existing_person_info[key] = value
        
    # Re-evaluate computed fields by passing through the Person model
    person_pydantic_object = Person(**existing_person_info)
    
    # Update the person in the original data list
    for idx, person in enumerate(data):
        if person.get("id") == person_id:
            data[idx] = person_pydantic_object.model_dump()
            break
            
    save_info(data)
    return JSONResponse(content={"message": "Person updated successfully."}, status_code=200)

# Recommendation Endpoints

@app.get('/recommend/diet/{person_id}')
def recommend_diet(person_id: str = Path(..., description="Unique ID of the person")):
    data = load_data()
    for person_data in data:
        if person_data.get("id") == person_id:
            # We can't strictly use Person(**person_data) if the json has missing fields. 
            # We'll calculate it safely using standard dictionaries fallback for raw json fields.
            try:
                person = Person(**person_data)
                bmi = person.bmi
                name = person.name
                diet = person.diet
            except Exception:
                # Fallback if Pydantic model validation fails due to missing keys in DB
                weight = person_data.get("weight", 0)
                height = person_data.get("height", 1) 
                bmi = weight / (height ** 2) if height else 0
                name = person_data.get("name", "Unknown")
                diet = person_data.get("diet", "Unknown")
            
            # Simple diet recommendation logic based on BMI
            if bmi < 18.5:
                recommendation = "High Calorie, Protein-rich diet (Caloric Surplus) for safe weight gain."
            elif 18.5 <= bmi < 25:
                recommendation = "Balanced diet to maintain current weight and health."
            else:
                recommendation = "Caloric Deficit, Low Carb/High Protein diet for safely losing weight."
            
            return {
                "person_id": person_id,
                "name": name,
                "current_diet": diet,
                "bmi": round(bmi, 2),
                "diet_recommendation": recommendation
            }
            
    raise HTTPException(status_code=404, detail="Person not found.")


@app.get('/recommend/workout/{person_id}')
def recommend_workout(person_id: str = Path(..., description="Unique ID of the person")):
    data = load_data()
    for person_data in data:
        if person_data.get("id") == person_id:
            # Safe Fallback Strategy like above
            try:
                person = Person(**person_data)
                bmi = person.bmi
                workout = person.workout
                health_score = person.health_score
                has_trainer = person.has_personal_trainer
                name = person.name
            except Exception:
                weight = person_data.get("weight", 0)
                height = person_data.get("height", 1) 
                bmi = weight / (height ** 2) if height else 0
                workout = person_data.get("workout", 0)
                has_trainer = person_data.get("has_personal_trainer", False)
                name = person_data.get("name", "Unknown")
                health_score = "Unable to compute (Missing Data)"
            
            # Simple workout recommendation logic based on workouts per week and BMI
            if workout < 3:
                recommendation = "Start with full-body workouts 3 days a week. Add 20-30 mins of moderate cardio."
            else:
                if bmi < 25:
                    recommendation = "Focus on a Push/Pull/Legs hypertrophy split to build or maintain muscle."
                else:
                    recommendation = "Combine heavy strength training with High-Intensity Interval Training (HIIT) to reduce body fat."
            
            trainer_note = " Consult your personal trainer for a specific routine!" if has_trainer else ""

            return {
                "person_id": person_id,
                "name": name,
                "current_workouts_per_week": workout,
                "health_score": health_score,
                "workout_recommendation": recommendation + trainer_note
            }
            
    raise HTTPException(status_code=404, detail="Person not found.")
