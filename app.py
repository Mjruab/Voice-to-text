import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ── Estilos ────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #fffde7; color: #333333; }

div.stButton > button {
    background-color: #f9a825;
    color: white;
    border-radius: 10px;
    padding: 10px 24px;
    border: none;
    font-size: 16px;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover { background-color: #f57f17; color: white; }

section[data-testid="stSidebar"] { background-color: #fff9c4; }

h1, h2, h3 { color: #f57f17; }

/* Tarjeta del poema */
.poema {
    background-color: #fff8e1;
    border-left: 5px solid #f9a825;
    padding: 20px 28px;
    border-radius: 10px;
    font-style: italic;
    font-size: 17px;
    line-height: 1.8;
    color: #4a4a4a;
    margin: 16px 0;
}
.autor {
    text-align: right;
    font-weight: bold;
    color: #f57f17;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Encabezado ─────────────────────────────────────────────────────
st.title("🎧 Conversión de Texto a Audio")

try:
    image = Image.open('Ondas sonoras de colores vibrantes.png')
    st.image(image, width=500)
except:
    st.info("📷 Imagen no encontrada.")

# ── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔊 Texto a Audio")
    st.info(
        "1️⃣ Lee el poema\n\n"
        "2️⃣ Copia el texto o escribe el tuyo\n\n"
        "3️⃣ Selecciona el idioma\n\n"
        "4️⃣ Presiona **Convertir a Audio**"
    )
    st.markdown("---")
    st.caption("Powered by gTTS")

# ── Poema ──────────────────────────────────────────────────────────
try:
    os.mkdir("temp")
except:
    pass

st.markdown("### 📜 Espero curarme de ti")
st.markdown("""
<div class="poema">
    ¿Te parece bien que te quiera nada más una semana?<br>
    No es mucho, ni es poco, es bastante.<br>
    En una semana se puede reunir todas las palabras de amor<br>
    que se han pronunciado sobre la tierra<br>
    y se les puede prender fuego.<br><br>
    <div class="autor">— Jaime Sabines</div>
</div>
""", unsafe_allow_html=True)

# ── Entrada de texto ───────────────────────────────────────────────
st.markdown("---")
st.markdown("### ✏️ ¿Quieres escucharlo?")
st.caption("Copia el poema o escribe tu propio texto:")

text = st.text_area("Ingresa el texto a escuchar", height=160)

# ── Configuración ──────────────────────────────────────────────────
idiomas = {"Español": "es", "Italiano": "it", "Francés": "fr"}
col1, col2 = st.columns(2)
with col1:
    option_lang = st.selectbox("🌐 Selecciona el idioma", list(idiomas.keys()))
    lg = idiomas[option_lang]
with col2:
    velocidad = st.radio("⚡ Velocidad", ("Normal", "Lenta"))
    slow = velocidad == "Lenta"

# ── Función de conversión ──────────────────────────────────────────
def text_to_speech(text, lg, slow):
    tts = gTTS(text, lang=lg, slow=slow)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name

def get_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = (f'<a href="data:application/octet-stream;base64,{bin_str}" '
            f'download="{os.path.basename(file_path)}">'
            f'⬇️ Descargar audio</a>')
    return href

# ── Botón convertir ────────────────────────────────────────────────
st.markdown("---")
if st.button("🔄 Convertir a Audio"):
    if not text.strip():
        st.warning("⚠️ Por favor escribe o pega algún texto primero.")
    else:
        with st.spinner("Generando audio..."):
            result = text_to_speech(text, lg, slow)
            audio_file = open(f"temp/{result}.mp3", "rb")
            audio_bytes = audio_file.read()

        st.success("✅ ¡Audio generado!")
        st.markdown("### 🔊 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.markdown(
            get_download_link(f"temp/{result}.mp3"),
            unsafe_allow_html=True
        )

# ── Limpieza de archivos ───────────────────────────────────────────
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n * 86400:
                os.remove(f)
remove_files(7)
