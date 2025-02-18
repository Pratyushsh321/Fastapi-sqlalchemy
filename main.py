from fastapi import FastAPI
from app import models
from app.database import engine  # absolute import
from app.routers import user, post, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "welcome to my API"}
