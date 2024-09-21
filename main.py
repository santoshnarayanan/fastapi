from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like pizza", "id": 2}]


@app.get("/")
async def root():
    return {"message": "Hello Welcome to the world of FastAPI"}

@app.get("/post")
async def get_post():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(new_post:Post):
    print(new_post)
    print(new_post.dict())
    return {"data": new_post}

