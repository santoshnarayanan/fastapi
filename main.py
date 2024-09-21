from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Welcome to the world of FastAPI"}

@app.get("/post")
async def get_post():
    return {"data": "This is your post"}

@app.post("/createposts")
def create_posts(payLoad:dict = Body(...)):
    print(payLoad)
    return {
            "new_post": f"title {payLoad['title']}, content: {payLoad['content']}"        # <--- added closing quote
        }

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None