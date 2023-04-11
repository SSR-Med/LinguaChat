from fastapi import FastAPI, Request, File, HTTPException, UploadFile
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from gpt_interface import GPTInterface
from fastapi import Body
import sqlite3


app = FastAPI()
templates = Jinja2Templates(directory="templates")

bot = "Hola desde Python!"  # Variable que se accederá desde el archivo HTML
usuario = None
# Serve static files in the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="templates")


@app.get("/chat", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# Para el mensaje del bot
@app.get("/bot")
async def get_bot():
    return {"bot": bot}


# Para el nombre del usuario
@app.get("/usName")
async def get_usName():
    global usuario
    return {"name": usuario}


@app.post("/lenguaje")
async def language_changed(value: str = Body()):
    if value != GPTInterface.LANGUAGE:
        GPTInterface.CHANGED = True
        GPTInterface.LANGUAGE = value


# Para guardar el audio
@app.post("/save-audio")
async def save_audio(audio: UploadFile = File(...)):
    # Check that the file is a WAV file
    if audio.content_type != "audio/mp3; codecs=opus":
        raise HTTPException(status_code=400, detail="File must be a mp3 file")

    # Save the file to the static folder
    file_path = os.path.join("static", audio.filename)
    with open(file_path, "wb") as f:
        f.write(audio.file.read())

    return {"message": "Audio saved successfully"}


@app.post("/saveText")
async def saveText(value: str = Body()):
    global bot
    bot = await GPTInterface.ProcessRequest(value)
    return value


@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    global usuario
    usuario = None
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login")
async def login(username: str, password: str):
    global usuario
    conn = sqlite3.connect("users.db")

    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password)
    )
    result = c.fetchone()

    conn.close()

    if result:
        usuario = username
        return {"status": 200, "message": "Login successful!"}
    else:
        return {"status": 400, "message": "Invalid username or password."}


@app.get("/registro")
async def registro(username: str, password: str):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        conn.close()
        return {"status": 200, "message": "Invalid username, select another username"}
    else:
        c.execute("INSERT INTO users VALUES(?,?)", (username, password))
        conn.commit()
        conn.close()
        return {"status": 400, "message": "Register successful!"}


@app.get("/menu", response_class=HTMLResponse)
async def get_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})


@app.get("/help", response_class=HTMLResponse)
async def get_help(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.post("/usNamePost")
async def userChanged(value: str = Body()):
    global usuario
    usuario = value


@app.get("/perfil", response_class=HTMLResponse)
async def get_perfil(request: Request):
    return templates.TemplateResponse("perfil.html", {"request": request})


@app.post("/uploadImage")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    with open(f"static/user.png", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}


# Changing user
@app.get("/changeUser")
async def changingUser(username: str):
    global usuario
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        conn.close()
        return {"status": 200, "message": "Invalid user"}
    else:
        c.execute("UPDATE users SET username=? WHERE username=?", (username, usuario))
        conn.commit()
        conn.close()
        usuario = username
        return {"status": 400, "message": "Modification was valid"}


# Changing password
@app.get("/changePass")
async def changingPass(oldPass: str, newPass: str):
    global usuario
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (usuario, oldPass))
    result = c.fetchone()
    if result:
        c.execute(
            "UPDATE users SET password=? WHERE username=? AND password=?",
            (newPass, usuario, oldPass),
        )
        conn.commit()
        conn.close()
        return {"status": 200, "message": "Modification was valid"}
    else:
        conn.close()
        return {"status": 400, "message": "Modification was invalid"}


@app.get("/security", response_class=HTMLResponse)
async def get_security(request: Request):
    return templates.TemplateResponse("security.html", {"request": request})


@app.get("/deleteAccount")
async def delete(user: str, passw: str):
    global usuario
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, passw))
    result = c.fetchone()
    if result:
        c.execute(
            "DELETE FROM users WHERE username=? AND password=?",
            (user, passw),
        )
        conn.commit()
        conn.close()
        return {"status": 200, "message": "Account deleted"}
    else:
        conn.close()
        return {"status": 400, "message": "Error"}
