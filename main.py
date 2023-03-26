from fastapi import FastAPI, Request, File, HTTPException, UploadFile
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Body

app = FastAPI()
templates = Jinja2Templates(directory="templates")

bot = "Hola desde Python!"  # Variable que se accederá desde el archivo HTML

# Serve static files in the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="templates")


@app.get("/chat", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# Para el mensaje del bot
@app.get("/bot")
async def get_bot():
    return {"bot": bot}


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
    return value
