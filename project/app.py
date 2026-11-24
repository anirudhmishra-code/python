from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Database Connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="changeme",
        database="agentic_ai"
    )


# Home Page
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "users": users
        }
    )


# Add Record
@app.post("/add")
def add_user(
    username: str = Form(...),
    email: str = Form(...),
    role: str = Form(...)
):

    conn = get_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO users(username,email,role,password_hash)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (username, email, role, "dummy_password")
    )

    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse("/", status_code=303)


# Update Record
@app.post("/update/{user_id}")
def update_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    role: str = Form(...)
):

    conn = get_db()
    cursor = conn.cursor()

    query = """
    UPDATE users
    SET username=%s,
        email=%s,
        role=%s
    WHERE id=%s
    """

    cursor.execute(
        query,
        (username, email, role, user_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse("/", status_code=303)


# Delete Record
@app.get("/delete/{user_id}")
def delete_user(user_id: int):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (user_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return RedirectResponse("/", status_code=303)
