from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .user import user_router, JWTBearer, TokenData, UserLogin, UserIn
from .user import login as user_login
from .user import register as user_register
from .todo import todo_router, get_todos, create_todo, update_todo_by_id, TodoIn
import json

app = FastAPI(docs_url = "/api/docs")

# CORS middleware, allow all origins, methods and headers
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# /user router
app.include_router(user_router, prefix="/api/user", tags=["user"])

# /todo router, it is protected by oauth2_scheme, requires logged in user
app.include_router(todo_router, prefix="/api/todo", tags=["todo"])

@app.get("/api/")
async def root():
    return {"message": "Hello World"}


app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

def is_logged_in(request: Request) -> TokenData if True else False:
    token = request.cookies.get("access_token")
    if not token:
        return False
    
    try:
        token_data = JWTBearer().verify_jwt(token)
    except:
        return False
    
    # convert token_data to TokenData model
    token_data = TokenData(**token_data)
    return token_data


@app.get("/")
async def home(request: Request):
    user = is_logged_in(request)
    # render template from templates/index.html
    flush = request.query_params.get("status")
    data = {}
    if flush:
        print(flush)
        flush = flush.lower()
        if flush == "logged_in":
            data["status"] = "success"
            data["message"] = "You are logged in"
        elif flush == "logged_out":
            print("logged out")
            data["status"] = "success"
            data["message"] = "You are logged out"
        elif flush == "allready_logged_in":
            data["status"] = "error"
            data["message"] = "You are allready logged in"
        else:
            flush = None
    if not user:
        return templates.TemplateResponse("index.html", {"request": request, "data": data})
    
    todos = await get_todos(user.dict())
    return templates.TemplateResponse("home.html", {"request": request, "user": user, "data": data, "todos": todos})

@app.get("/login")
async def login(request: Request):

    if is_logged_in(request):
        return RedirectResponse(url="/?status=allready_logged_in", status_code=302)

    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request):
    # get username and password from form data

    if is_logged_in(request):
        return RedirectResponse(url="/", status_code=302)

    form = await request.form()
    
    username = form.get("username")
    password = form.get("password")

    if not username or not password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Username or password is empty"})
    
    login_data = UserLogin(username=username, password=password)
    response = await user_login(login_data)

    if not 'access_token' in response:
        return templates.TemplateResponse("login.html", {"request": request, "error": response['detail']})

    headers = {"Set-Cookie": f"access_token={response['access_token']}; HttpOnly"}
    response = RedirectResponse(url="/?status=logged_in", status_code=302, headers=headers)
    return response

@app.get("/logout")
async def logout(request: Request):
    
    headers = {"Set-Cookie": "access_token=; HttpOnly"}
    response = RedirectResponse(url="/?status=logged_out", status_code=302, headers=headers)
    return response

@app.get("/register")
async def register(request: Request):

    if is_logged_in(request):
        return RedirectResponse(url="/?status=allready_logged_in", status_code=302)

    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request):
    # get username and password from form data

    if is_logged_in(request):
        return RedirectResponse(url="/", status_code=302)

    form = await request.form()
    
    username = form.get("username")
    name = form.get("name")
    password = form.get("password")

    if not username or not name or not password:
        return templates.TemplateResponse("register.html", {"request": request, "data": {"status": "error", "message": "Username, name or password cannot be empty"}})
    
    user_data = UserIn(username=username, name=name, password=password)
    try:
        response = await user_register(user_data)
    except Exception as e:
        return templates.TemplateResponse("register.html", {"request": request, "error": str(e)})
    
    status = response.get("status")
    if not status or status != "success":
        return templates.TemplateResponse("register.html", {"request": request, "error": "Unknown error"})
    
    return RedirectResponse(url="/login", status_code=302)
