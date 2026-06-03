from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, SessionLocal, Base, User, get_db
from security import generate_salt, get_password_hash, verify_password

app = FastAPI(title="Cybersecurity Final API")

# Allow requests from Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# --- ROUTES ---
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # 1. Generate Salt
    salt = generate_salt()
    # 2. Hash Password (with salt and pepper)
    hashed_password = get_password_hash(user.password, salt)
    
    # 3. Store in DB
    new_user = User(username=user.username, password_hash=hashed_password, salt=salt)
    db.add(new_user)
    db.commit()
    
    return {"message": "Registration Successful"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    # 1. Retrieve stored salt from database
    # 2. Recompute hash and compare
    if not db_user or not verify_password(user.password, db_user.salt, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Username or Password")
        
    return {"message": "Login Successful"}