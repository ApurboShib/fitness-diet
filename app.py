# here we building our ML model .. 

from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import pickle 
import pandas as pd


app = FastAPI()

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    
