from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from auth import hash_password
from auth import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from models import Post
from auth import get_current_user
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Allow CORS so the frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can replace * with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterInput(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: RegisterInput, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

class PostInput(BaseModel):
    content: str
    link: str | None = None

@app.post("/posts")
def create_post(post: PostInput, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_post = Post(content=post.content, link=post.link, user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "Post created", "id": new_post.id}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.votes.desc()).all()
    return posts

@app.post("/vote")
def vote_on_post(
    post_id: int = Body(...), 
    direction: int = Body(...), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if direction not in (-1, 1):
        raise HTTPException(status_code=400, detail="Vote must be 1 or -1")

    post.votes += direction
    db.commit()
    db.refresh(post)
    return {"msg": "Vote recorded", "post_id": post.id, "new_votes": post.votes}


