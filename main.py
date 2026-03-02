from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from rembg import remove

app = FastAPI(title="Pro AI BG Remover API")

# Allow Cloudflare front-end to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your Cloudflare site URL if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    """
    Endpoint to remove background from uploaded image
    """
    input_data = await file.read()           # Read uploaded file
    output = remove(input_data)              # Remove background using rembg
    return Response(content=output, media_type="image/png")  # Return PNG
