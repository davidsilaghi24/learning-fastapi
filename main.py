from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from typing import List
from models import User, Gender, Role, User_update

app = FastAPI()

db: List[User] = [
    User(id=UUID('08b92d7a-2894-4c0e-ac22-dc4ff23bb091'), 
        first_name="Jamila",
        last_name="Ahmed", 
        gender=Gender.female,
        roles=[Role.student]),
    User(id=UUID('01d56691-1510-406c-8fda-955242274c65'), 
        first_name="Davie",
        last_name="Jones",
        gender=Gender.male, 
        roles=[Role.admin, Role.user])
]

@app.get("/")
async def root():
    return {"Hello": "Mundo"}

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update:User_update, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name:
                user.first_name = user_update.first_name
            if user_update.last_name:
                user.last_name = user_update.last_name
            if user_update.middle_name:
                user.middle_name = user_update.middle_name
            if user_update.roles:
                user.roles = user_update.roles
            
            return
            
    raise HTTPException(
        status_code=404,
        detail=f"user with id {user_id} does not exist"
    )

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id {user_id} does not exist"
    )

