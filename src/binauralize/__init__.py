import librosa
import numpy as np
import soundfile as sf

def hertz_to_semitones(freq_original, freq_alvo):
    """Converte um intervalo de frequência de Hertz para semitons."""
    return 12 * np.log2(freq_alvo / freq_original)

def binauralize(input_file: str, binaural_frequency_hz):
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
    if "wav" in input_file:
        input_file = input_file.removesuffix(".wav")
    if "mp3" in input_file:
        input_file = input_file.removesuffix(".mp3")
    # Salvar o áudio estéreo em um arquivo WAV
    sf.write(f"audiooutput/{input_file.removeprefix("audioinput/")}_{str(binaural_frequency_hz)}_hz_binaural.wav", y_stereo.T, sr, format='WAV', subtype='PCM_16')

    print(f"Frequência binaural gerada com desvio de {binaural_frequency_hz} Hz entre canais.")
