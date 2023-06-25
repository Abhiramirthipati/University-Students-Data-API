from typing import List
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdateRequest
from uuid import UUID
app = FastAPI()

db: List[User] = [
    User(
        id=UUID("214e91d8-d2de-4c5f-981f-3f68bddd4bbf"),             
        first_name="Scarlet",   
        last_name="johnson",
        gender=Gender.female,
        roles=[Role.student] 
    ),

     User(
        id=UUID("5edb6b1e-3243-4695-abe1-61aa65a817b8"),             
        first_name="Naruto",   
        last_name="Uzumaki",
        gender=Gender.male,
        roles=[Role.admin, Role.student]
    )
] 
 
@app.get("/")
def root():
    return {"Hello": "Mundo"} 
 
@app.get("/api/v1/users")
async def fetch_users(): 
    return db;

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id} 

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id : UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user) 
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id:{user_id} does not exists"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID ):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
        raise HTTPException(
            status_code=404,
            detail=f"user with id: {user_id} does not exists"
        )