from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import io
import os
import PIL.Image as Image
import google.generativeai as genai


app = FastAPI()
GOOGLE_API_KEY = "AIzaSyD-iOD7OtQz9iEztMGzjadZCcP__R1ABS4"
genai.configure(api_key=GOOGLE_API_KEY) #'AIzaSyD-iOD7OtQz9iEztMGzjadZCcP__R1ABS4

model = genai.GenerativeModel('gemini-1.5-flash')

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_image(request: Request, anime_image: UploadFile = File(...)):
    try:
        # Read the uploaded image
        image_data = await anime_image.read()
        image = Image.open(io.BytesIO(image_data))

        response = model.generate_content(["Name of the anime and what's the genre answer with 'Genre:'?", image])

        anime_name = response.text

        return templates.TemplateResponse("index.html", {"request": request, "anime_name": anime_name})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

