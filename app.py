from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import io
import PIL.Image as Image
import google.generativeai as genai
import logging

app = FastAPI()

GOOGLE_API_KEY = 'key'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_image(request: Request, anime_image: UploadFile = File(...)):
    try:
        # Read the uploaded image
        image_data = await anime_image.read()
        image = Image.open(io.BytesIO(image_data))

        logger.info("Image uploaded successfully")

        response = model.generate_content(["Name of the anime?", image])

        logger.info("Model response received")

        anime_name = response.text

        return templates.TemplateResponse("index.html", {"request": request, "anime_name": anime_name})
    
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

