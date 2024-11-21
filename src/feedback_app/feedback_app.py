import streamlit as st
import requests
import os
import json

CONFIG_FILE = "src/feedback_app/config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Load shared configuration
config = load_config()

if "admin_username" not in st.session_state:
    st.session_state["admin_username"] = os.getenv("ADMIN_USERNAME", "admin")
if "admin_password" not in st.session_state:
    st.session_state["admin_password"] = os.getenv("ADMIN_PASSWORD", "admin")
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Definir traduções
with open("src/feedback_app/data/translations.json", "r") as f:
    TRANSLATIONS =  json.load(f)

FEEDBACK_PATH = "src/feedback_app/data/feedback.json"

# Function to get the translated text
def t(key):
    language = st.session_state.get("language", "English")
    return TRANSLATIONS.get(language, {}).get(key, key)

def update_config(ngrok_url, ngrok_api_secret):
    config["NGROK_URL"] = ngrok_url
    config["NGROK_API_SECRET"] = ngrok_api_secret
    save_config(config)
    st.success(t("NGROK credentials updated successfully."))

def get_ngrok_url():
    return load_config().get("NGROK_URL")

def get_ngrok_api_secret():
    return load_config().get("NGROK_API_SECRET")

def save_feedback(response):
    feedback_file = FEEDBACK_PATH
    if os.path.exists(feedback_file):
        with open(feedback_file, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(response)
    with open(feedback_file, "w") as f:
        json.dump(data, f, indent=4)

def feedback():
    st.title(t("Feedback App"))
    st.write(t("Please provide your feedback on the music pairs below."))

    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "age" not in st.session_state:
        st.session_state["age"] = ""
    if "gender" not in st.session_state:
        st.session_state["gender"] = ""
    if "email" not in st.session_state:
        st.session_state["email"] = ""
    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    if not st.session_state["submitted"]:
        with st.form("user_info_form"):
            st.write(t("Please provide your information below."))
            name = st.text_input(t("Name"))
            age = st.number_input(t("Age"), min_value=0, max_value=120, step=1)
            gender = st.selectbox(t("Gender"), [t("Male"), t("Female"), t("Other")])
            email = st.text_input(t("Email"))
            submitted = st.form_submit_button(t("Submit"))

            if submitted and not any([name == "", age == 0, email == ""]):
                st.session_state["name"] = name
                st.session_state["age"] = age
                st.session_state["gender"] = gender
                st.session_state["email"] = email
                st.session_state["submitted"] = True
                st.success(t("Information submitted."))

    # Initialize session state for audio evaluation
    if "audio_list" not in st.session_state:
        music_folder = "src/feedback_app/media"
        audio_files = [f for f in os.listdir(music_folder) if f.endswith(".wav") or f.endswith(".mp3")]
        st.session_state.audio_list = [os.path.join(music_folder, f) for f in sorted(audio_files)]
        st.session_state.current_pair = 0
        st.session_state.responses = []

    # Avaliação dos pares de músicas
    if st.session_state["name"] and st.session_state["email"]:
        total_pairs = len(st.session_state.audio_list) // 2
        pair_index = st.session_state.current_pair

        if pair_index < total_pairs:
            audio1 = st.session_state.audio_list[pair_index * 2]
            audio2 = st.session_state.audio_list[pair_index * 2 + 1]

            col1, col2 = st.columns(2)

            with col1:
                st.audio(audio1)
                feeling1 = st.selectbox("Select a feeling for Music 1", ["Alert", "Creative", "Relaxed", "Productive", "Sleepy"], key=f"feeling1_{pair_index}")

            with col2:
                st.audio(audio2)
                feeling2 = st.selectbox("Select a feeling for Music 2", ["Alert", "Creative", "Relaxed", "Productive", "Sleepy"], key=f"feeling2_{pair_index}")

            preferred = st.radio("Which music do you prefer?", ("Music 1", "Music 2"), key=f"preferred_{pair_index}")

            if st.button("Next"):
                st.session_state.responses.append(
                    {
                        "pair": pair_index + 1,
                        "music1": audio1,
                        "music1_feeling": feeling1,
                        "music2": audio2,
                        "music2_feeling": feeling2,
                        "preferred": preferred
                    }
                )
                st.session_state.current_pair += 1
                st.rerun()
        else:
            st.text("Thank you for your feedback!")
            save_feedback(
                { 
                    "name": st.session_state["name"],
                    "age": st.session_state["age"],
                    "gender": st.session_state["gender"],
                    "email": st.session_state["email"],
                    "feedback": st.session_state["responses"]
                }
            )
    else:
        st.warning("Please submit your information to proceed.")

def try_it_out():
    st.title(t("Try it out"))
    st.write(t("Please provide the description of the music you want to generate:"))
    description = st.text_area("Description")
    st.write(t("Binaural beats explanation"))
    st.write(t("Please select the binaural beat frequency:"))
    frequency_options = [
        "3 Hz - Delta Waves (Deep sleep, relaxation)",
        "6 Hz - Theta Waves (Meditation, creativity)",
        "10 Hz - Alpha Waves (Calm focus, relaxation)",
        "18 Hz - Beta Waves (Active thinking, alertness)",
        "40 Hz - Gamma Waves (High-level cognitive functions)"
    ]
    frequency = st.radio(t("Select a frequency"), frequency_options)
    frequency = int(frequency.split()[0])
    # Generate audio button
    generate_audio = st.button(t("Generate Audio"))
    
    if generate_audio:
        if not get_ngrok_url() or not get_ngrok_api_secret():
            st.write(t("Service is not available."))
            return
        
        # Make the POST request to generate audio
        response = requests.post(
            f"{get_ngrok_url()}/api/music_gen",
            json={"description": description, "binaural_freq": frequency, "apply_binaural": True},
            headers={"Authorization": f"Bearer {get_ngrok_api_secret()}"}
        )

        non_binaural_response = requests.post(
            f"{get_ngrok_url()}/api/music_gen",
            json={"description": description, "binaural_freq": 0, "apply_binaural": False},
            headers={"Authorization": f"Bearer {get_ngrok_api_secret()}"}
        )
        
        if non_binaural_response.status_code == 200:
            st.write(t("Non-binaural audio:"))
            st.audio(non_binaural_response.content, format="audio/mpeg")
        else:
            st.write(t("Failed to generate non-binaural audio. Please try again."))
        
        if response.status_code == 200:
            # Save audio content in session state
            st.session_state["audio_content"] = response.content
            st.write(t("Audio with binaural beat:"))
            st.audio(response.content, format="audio/mpeg")
            st.write(t("Do you want to download the audio?"))
        else:
            st.write(t("Failed to generate audio. Please try again."))

    
    # Display download button if audio content is available
    if "audio_content" in st.session_state:
        download_audio = st.button(t("Yes!"))
        
        if download_audio:
            # Generate a filename from the description
            file_name = "_".join(description.lower().split()[:3]) + ".mp3"
            
            # Provide download option
            st.download_button(
                t("Download Audio"),
                st.session_state["audio_content"],
                file_name=file_name,
                mime="audio/mpeg"
            )

def dashboard():
    feedback_data = []
    if os.path.exists(FEEDBACK_PATH):
        with open(FEEDBACK_PATH, "r") as f:
            feedback_data = json.load(f)

    data = []
    for response in feedback_data:
        data.extend(response["feedback"])

    st.title(t("Dashboard"))
    st.write(t("Here you can visualize the data from the provided feedback."))

    if not data:
        st.warning(t("No feedback data available."))
        return

    # Count feelings for Music 1 and Music 2
    feelings_music1 = {}
    feelings_music2 = {}
    preferences = {t("Music 1"): 0, t("Music 2"): 0}

    for response in data:
        feelings_music1[response["music1_feeling"]] = feelings_music1.get(response["music1_feeling"], 0) + 1
        feelings_music2[response["music2_feeling"]] = feelings_music2.get(response["music2_feeling"], 0) + 1
        preferences[response["preferred"]] += 1

    # Prepare data for charts
    music1_chart_data = {"Feeling": list(feelings_music1.keys()), "Count": list(feelings_music1.values())}
    music2_chart_data = {"Feeling": list(feelings_music2.keys()), "Count": list(feelings_music2.values())}
    preferences_chart_data = {"Music": list(preferences.keys()), "Count": list(preferences.values())}

    # Bar charts for feelings
    st.subheader(t("Feelings for Music 1 and Music 2"))
    col1, col2 = st.columns(2)
    with col1:
        st.write(t("Feelings for Music 1"))
        st.bar_chart(music1_chart_data)
    with col2:
        st.write(t("Feelings for Music 2"))
        st.bar_chart(music2_chart_data)

    # Preferences chart
    st.subheader(t("Music Preferences"))
    st.bar_chart(preferences_chart_data)

    # Export button for feedback data
    st.subheader(t("Export Feedback Data"))
    st.download_button(
        t("Download data as JSON"),
        json.dumps(feedback_data, indent=4),
        file_name="feedback.json",
        mime="application/json"
    )

def admin():
    st.title(t("Admin - Update NGROK Credentials"))
    with st.form("ngrok_credentials_form"):
        new_url = st.text_input(t("NGROK URL"), value=load_config().get("NGROK_URL"))
        new_secret = st.text_input(t("NGROK API Secret"), value=load_config().get("NGROK_API_SECRET"), type="password")
        submit_button = st.form_submit_button(t("Update"))
        if submit_button:
            update_config(new_url, new_secret)

def auth():
    st.title(t("Authentication"))
    st.write(t("Please enter your credentials."))
    username = st.text_input(t("Username"))
    password = st.text_input(t("Password"), type="password")
    authenticate = st.button(t("Authenticate"))
    if authenticate:
        if username == st.session_state["admin_username"] and password == st.session_state["admin_password"]:
            st.session_state["authenticated"] = True
            st.success(t("Authentication successful."))
        else:
            st.error(t("Authentication failed."))

def run():
    # Seleção de idioma
    st.sidebar.title(t("Language"))
    language_options = ["English", "Português"]

    # Usar o parâmetro index para definir o idioma padrão
    default_language = st.session_state.get("language", "English")
    if default_language in language_options:
        default_index = language_options.index(default_language)
    else:
        default_index = 0

    # O selectbox gerencia st.session_state["language"]
    st.sidebar.selectbox(
        t("Select language / Selecione o idioma"),
        language_options,
        index=default_index,
        key="language"
    )

    # Navegação
    st.sidebar.title(t("Navigation"))

    # Definir chaves de página e seus nomes correspondentes
    page_names = {
        "feedback": t("Feedback"),
        "try_it_out": t("Try it out"),
        "admin": t("Admin"),
        "dashboard": t("Dashboard")
    }

    page_keys = list(page_names.keys())
    page_labels = list(page_names.values())

    # Definir página padrão
    if "page" not in st.session_state:
        st.session_state["page"] = "try_it_out"

    # Obter o índice da página atual
    current_page_index = page_keys.index(st.session_state["page"])

    # Exibir os botões de rádio com nomes de páginas traduzidos
    selected_page_label = st.sidebar.radio(
        t("Go to"),
        page_labels,
        index=current_page_index,
        key="navigation_radio"
    )

    # Mapear o rótulo selecionado de volta para a chave da página
    selected_page_key = page_keys[page_labels.index(selected_page_label)]

    # Atualizar o estado da sessão com a chave da página selecionada
    st.session_state["page"] = selected_page_key

    # Navegar para a página selecionada
    if st.session_state["page"] == "feedback":
        feedback()
    elif st.session_state["page"] == "try_it_out":
        try_it_out()
    elif st.session_state["page"] == "admin":
        if not st.session_state["authenticated"]:
            auth()
        if st.session_state["authenticated"]:
            admin()
    elif st.session_state["page"] == "dashboard":
        if not st.session_state["authenticated"]:
            auth()
        if st.session_state["authenticated"]:
            dashboard()

if __name__ == "__main__":
    run()
