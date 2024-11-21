import audiocraft
from audiocraft.models import MusicGen

def load_model():
    print("Loading pretrained model facebook/musicgen-medium...")
    model = MusicGen.get_pretrained("facebook/musicgen-medium")
    
