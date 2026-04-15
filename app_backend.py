from fastapi import FastAPI, Header, HTTPException
from voxcpm import VoxCPM
import torch
import os
import soundfile as sf
import io
from fastapi.responses import StreamingResponse

app = FastAPI()
API_KEY = os.getenv("API_KEY", "Swarup_TTS_Secret_2026")

# Load model once on startup
print("Loading Model...")
model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)
model.tts_model.to('cuda').to(torch.bfloat16)

@app.get("/generate")
async def generate(text: str, x_api_key: str = Header(None)):
    if x_api_key != API_KEY: raise HTTPException(status_code=403)
    
    wav = model.generate(text=text, cfg_value=2.0, inference_timesteps=15)
    
    # Return as a stream instead of saving to file for cloud deployment
    buffer = io.BytesIO()
    sf.write(buffer, wav, model.tts_model.sample_rate, format='WAV')
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="audio/wav")
