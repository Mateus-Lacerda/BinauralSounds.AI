from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid

from model_api.models.music_gen_input_data import MusicGenInputData
from audio_model.generate_music import generate_music
from utils.colors import Colors as cl

app = FastAPI()
security = HTTPBearer()
SECRET = str(uuid.uuid4())

async def verify_credentials(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")
    
@app.get('/')
def index():
    return {
        "message": "Model API is running!",
        "docs": "/docs"
        }

@app.post("/api/music_gen")
async def music_gen(data: MusicGenInputData, credentials: HTTPAuthorizationCredentials = Depends(security)):
    description = data.description
    binaural_freq = data.binaural_freq
    apply_binaural = data.apply_binaural
    audio = generate_music(description, binaural_freq, apply_binaural)
    return Response(content=audio, status_code=200, media_type="audio/mpeg")

@app.get("/docs")
async def get_docs():
    docs = {
        "POST /api/music_gen/": {
            "description": "This route receives a description and a frequency and returns a binaural sound.",
            "request_body": {
                "description": "The description of the music to be generated.",
                "binaural_freq": "The frequency of the binaural sound."
                },
            "response": {
                "description": "The audio generated.",
                "content": "audio/mpeg"
            }
        }
    }
    return docs

def start_ngrok():
    from pyngrok import ngrok, exception
    try:
        tunnel = ngrok.connect(8000)
    except exception.PyngrokNgrokError as e:
        print('Erro ao iniciar o ngrok:', e)
        ngrok_token = input('Insira o seu token do ngrok: ')
        ngrok.set_auth_token(ngrok_token)
        tunnel = ngrok.connect(8000)
    url = tunnel.public_url
    print(cl.colored(f' * Tunnel URL: {url}', 'YELLOW'))

def run():
    import uvicorn
    start_ngrok()
    print(cl.colored(' * Iniciando o servidor...', 'BLUE'))
    print(cl.colored(f" * Secret: {SECRET}", "YELLOW"))
    uvicorn.run(app, host="0.0.0.0", port=8000)
