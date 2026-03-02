from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import requests

app = FastAPI(title="Free BG Remover API")

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

REMOVE_BG_API_KEY = "YOUR_FREE_API_KEY_HERE"  # Replace with your Remove.bg free API key

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_data = await file.read()
    if len(input_data) > 1024*1024:  # 1 MB limit
        return {"error":"File exceeds 1MB limit"}

    # Call Remove.bg API
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": input_data},
        data={"size":"auto"},
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
    )
    if r.status_code != 200:
        return {"error": "API error: " + r.text}

    return Response(content=r.content, media_type="image/png")
