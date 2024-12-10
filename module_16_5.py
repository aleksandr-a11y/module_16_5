from fastapi import FastAPI, status, Body, HTTPException, Path, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory = 'templates')



class User(BaseModel):
    id: int
    username: str
    age: int

users: List[User ] = []

@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}')
async def get_user(request: Request, user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]) -> HTMLResponse:
    try:
        for user in users:
            if user.id == user_id:
                return templates.TemplateResponse("users.html", {"request": request, "user": user})

    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post(path='/user/{username}/{age}', response_model=User)
async def post_user(request: Request, username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age')]):
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put(path='/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> str:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    else:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete(path='/user/{user_id}', response_model=User)
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]) -> str:
    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)

    else:
        raise HTTPException(status_code=404, detail='User was not found')
