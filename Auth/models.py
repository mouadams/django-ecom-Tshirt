# from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from mongo import db
from bson.objectid import ObjectId


from datetime import datetime

from django.contrib.auth.hashers import make_password


def get_user_by_email(email: str):
    return db["users"].find_one({
        "email": email,
    })
    


def serialize(user):
    return {
        "id": str(ObjectId(user["_id"])),
        "email": user["email"],
        "password": user["password"],
        "createdAt": str(user["createdAt"])
    }



def check_password(password):
    try:
        validate_password(password)  # This checks the password
        return True,"Password is valid."
    except ValidationError as e:
        return False,f"Password is invalid: {', '.join(e.messages)}"
    
def create_user(email:str, password:str):
    
    hashed_pass = make_password(password)
    
    return db["users"].insert_one({
        "email": email,
        "password": hashed_pass,
        "createdAt": datetime.now()
    })
    
