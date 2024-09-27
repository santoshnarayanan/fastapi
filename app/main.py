from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from httpx import post
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from random import randrange
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", 
                                password="Atos#000", port="5432", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Error while connecting to database")
        print(error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like pizza", "id": 2}]


@app.get("/")
async def root():
    return {"message": "Hello Welcome to the world of FastAPI"}

@app.get("/post")
async def get_post():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                  (post.title, post.content, post.published))
    new_posts = cursor.fetchone()
    conn.commit()
    return {"data": new_posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    post = cursor.fetchone()
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


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = -1
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            index = i
            break
    if(index == -1):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    return {"data": post_dict}
