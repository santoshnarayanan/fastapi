from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from httpx import post
from pydantic import BaseModel
from random import randrange

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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post = None
    for p in my_posts:
        if p["id"] == id:
            post = p
    if(not post):
        # response.status_code = 404
        # return {"message": f"post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = -1
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            index = i
            break
    if(index == -1):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

