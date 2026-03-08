from database import (get_con, register_user, user_exists, get_user, add_demand, 
                     get_user_demands, get_all_demands, update_demand_status)
from fastapi import FastAPI, Request, HTTPException, responses, status
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Global variables for simple session management (MVP only)
current_user = None
current_store_ic = None

templates = Jinja2Templates(directory="templates")

# Demo Store IC credentials (in production, use database)
STORE_IC_USERNAME = "store_ic"
STORE_IC_PASSWORD = "admin123"


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "current_user": current_user,
            "current_store_ic": current_store_ic
        }
    )


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
        {
            "current_user": current_user,
            "current_store_ic": current_store_ic
        }
    )


@app.post("/register")
async def register(request: Request):
    form_data = await request.form()
    army_no = form_data.get("army_no")
    full_name = form_data.get("full_name")
    position = form_data.get("position")
    email = form_data.get("email")
    phone = form_data.get("phone")
    password = form_data.get("password")
    
    # validate army number length (8 characters)
    if not army_no or len(army_no) != 8:
        return templates.TemplateResponse(
            request,
            "register.html",
            {"error": "Army number must be exactly 8 characters."}
        )

    # Check if user already exists
    if user_exists(army_no):
        return templates.TemplateResponse(
            request,
            "register.html",
            {"error": "Army number already registered!"}
        )
    
    # Register user
    if register_user(army_no, full_name, position, email, phone, password):
        return templates.TemplateResponse(
            request,
            "register.html",
            {"message": "Registration successful! Please login."}
        )
    else:
        return templates.TemplateResponse(
            request,
            "register.html",
            {"error": "Registration failed. Please try again."}
        )


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "current_user": current_user,
            "current_store_ic": current_store_ic
        }
    )


@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    army_no = form_data.get("army_no")
    password = form_data.get("password")
    
    # Check if user exists and password matches
    user = get_user(army_no)
    if not user or user[5] != password:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Invalid army number or password!"}
        )
    
    # Store user info in global variable (simple for MVP)
    global current_user
    current_user = {
        "army_no": user[0],
        "full_name": user[1],
        "position": user[2],
        "email": user[3]
    }
    
    return responses.RedirectResponse(url="/user-dashboard", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/logout")
def logout(request: Request):
    global current_user
    current_user = None
    return responses.RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/user-dashboard")
def user_dashboard(request: Request):
    global current_user
    if not current_user:
        return responses.RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    demands = get_user_demands(current_user["army_no"])
    user_obj = get_user(current_user["army_no"])
    
    # Check for success/error query parameters
    success = request.query_params.get("success") == "1"
    error = request.query_params.get("error") == "1"
    
    return templates.TemplateResponse(
        request,
        "user_dashboard.html",
        {
            "user": user_obj,
            "demands": demands,
            "success": success,
            "error": error,
            "current_user": current_user,
            "current_store_ic": current_store_ic
        }
    )


@app.post("/submit-demand")
async def submit_demand(request: Request):
    global current_user
    if not current_user:
        return responses.RedirectResponse(url="/login", status_code=303)
    
    form_data = await request.form()
    item = form_data.get("item")
    quantity = form_data.get("quantity")
    description = form_data.get("description")
    
    if add_demand(current_user["army_no"], item, int(quantity), description):
        return responses.RedirectResponse(url="/user-dashboard?success=1", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return responses.RedirectResponse(url="/user-dashboard?error=1", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/store-ic-login")
def store_ic_login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "store_ic_login.html",
        {
            "current_user": current_user,
            "current_store_ic": current_store_ic
        }
    )


@app.post("/store-ic-login")
async def store_ic_login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    # Verify credentials (basic check)
    if username == STORE_IC_USERNAME and password == STORE_IC_PASSWORD:
        global current_store_ic
        current_store_ic = {
            "username": username
        }
        return responses.RedirectResponse(url="/store-ic-dashboard", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse(
            request,
            "store_ic_login.html",
            {"error": "Invalid credentials!"}
        )


@app.get("/store-ic-dashboard")
def store_ic_dashboard(request: Request):
    global current_store_ic
    if not current_store_ic:
        return responses.RedirectResponse(url="/store-ic-login", status_code=status.HTTP_303_SEE_OTHER)
    
    demands = get_all_demands()
    
    return templates.TemplateResponse(
        request,
        "store_ic_dashboard.html",
        {
            "demands": demands,
            "current_user": current_user,
            "current_store_ic": current_store_ic
        }
    )


@app.get("/update-demand/{demand_id}/{status}")
def update_demand(request: Request, demand_id: int, status: str):
    global current_store_ic
    if not current_store_ic:
        return responses.RedirectResponse(url="/store-ic-login", status_code= 303)
    
    # Valid statuses
    valid_statuses = ["Pending", "Accepted", "Rejected", "Delayed"]
    if status not in valid_statuses:
        return responses.RedirectResponse(url="/store-ic-dashboard", status_code=303)
    
    update_demand_status(demand_id, status)
    
    return responses.RedirectResponse(url="/store-ic-dashboard", status_code=303)


@app.get("/store-ic-logout")
def store_ic_logout(request: Request):
    global current_store_ic
    current_store_ic = None
    return responses.RedirectResponse(url="/", status_code=303)