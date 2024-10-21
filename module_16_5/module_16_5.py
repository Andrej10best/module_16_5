from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int = None

@app.get('/')
def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/user/{user_id}')
async def get_users(request:Request, user_id: int) -> HTMLResponse:
    user = None
    for u in users:
        if u.id == user_id:
            user = u
    if user:
        return templates.TemplateResponse('users.html', context={'request': request, 'user': user})
    else:
        raise HTTPException(status_code=404, detail='User not found')


@app.post('/user/{username}/{age}')
async def post_user(username: str, age: int) -> User:
    user_id = len(users) + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user



@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail='User was not found')
