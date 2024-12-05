import os

ENV = os.getenv("ENV", "gen-off")
CUDA_AVAILABLE = os.getenv("CUDA_AVAILABLE", "False")
if ENV == "gen-on":
    import audiocraft
    from audiocraft.models import MusicGen
    import torchaudio
    import io
    model = MusicGen.get_pretrained("facebook/musicgen-medium", device ='cuda' if CUDA_AVAILABLE == "True" else 'cpu')

import librosa
import numpy as np
import soundfile as sf

def hertz_to_semitones(freq_original, freq_alvo):
    """Converte um intervalo de frequência de Hertz para semitons."""
    return 12 * np.log2(freq_alvo / freq_original)

def alterar_frequencia(input_file, output_file, binaural_frequency_hz):
    # Carregar o arquivo de áudio
    y, sr = librosa.load(input_file, sr=None)  # sr=None preserva a taxa de amostragem original

    # Frequência original do áudio (aproximação para cálculo: taxa de amostragem / 2)
    freq_original = sr / 2

    # Calcular o desvio em semitons para o binaural
    n_steps_baixo = hertz_to_semitones(freq_original, freq_original - binaural_frequency_hz/2)
    n_steps_alto = hertz_to_semitones(freq_original, freq_original + binaural_frequency_hz/2)

    # Criar os dois canais com pitch alterado
    canal_esquerdo = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps_baixo)
    canal_direito = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps_alto)

    # Combinar os dois canais em um array estéreo
    y_stereo = np.vstack((canal_esquerdo, canal_direito))

    # Salvar o áudio estéreo em um arquivo WAV
    sf.write(output_file, y_stereo.T, sr, format='WAV', subtype='PCM_16')

    print(f"Frequência binaural gerada com desvio de {binaural_frequency_hz} Hz entre canais.")

def generate_music(description: str, binaural_frequency: int, apply_binaural: bool = False):
    """
    This function receives a description and generates a music based on it.
    Args:
        description (str): The description of the music to be generated.
        binaural_frequency (int): The frequency difference between the two channels.
    Returns:
        audio (bytes): The audio generated.
    """
    # is in the same directory as this file, inside a folder dummy_data, named audio.wav
    if ENV == "gen-off":
        if description == "dummy":
            dummy_path = "src/audio_model/dummy_data/audio.wav"
            with open(dummy_path, "rb") as f:
                audio = f.read()
            if apply_binaural:
                output_path = "src/audio_model/dummy_data/audio_binaural.wav"
                alterar_frequencia(dummy_path, output_path, binaural_frequency)
                with open(dummy_path, "rb") as f:
                    audio = f.read()
            return audio
        else:
            return "NADA"
    else:
        model.set_generation_params(duration=15)
        music = model.generate(descriptions=[description])[0].cpu()
        # Ensure the tensor is 2D (channels x samples)
        if music.dim() == 1:  # Add channel dimension if it's missing
            music = music.unsqueeze(0)

        # Create an in-memory buffer for the audio
        buffer = io.BytesIO()

        # Write the tensor as a WAV file into the buffer
        torchaudio.save(buffer, music, model.sample_rate, format="wav")

        # Get the byte data from the buffer
        buffer.seek(0)
        audio_bytes = buffer.read()

        if apply_binaural:
            alterar_frequencia(io.BytesIO(audio_bytes), buffer, binaural_frequency)
            buffer.seek(0)
            audio_bytes = buffer.read()

        return audio_bytes