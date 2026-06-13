import streamlit as st
from google import genai
from google.genai import types

# 1. Streamlit Seiten-Konfiguration
st.set_page_config(page_title="Text-Entschwurbler", page_icon="✍️", layout="centered")

st.title("✍️ Text-Entschwurbler")
st.write("Verwandle holprige Sätze in wissenschaftliche, kompakte oder einfache Varianten.")

# 2. Gemini Client initialisieren (lädt den Key automatisch aus st.secrets)
try:
    # Streamlit sucht in st.secrets automatisch nach "GEMINI_API_KEY"
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Fehler beim Laden des API-Keys. Überprüfe deine .streamlit/secrets.toml-Datei!")
    st.stop()

# 3. Benutzeroberfläche (UI) bauen
user_input = st.text_area(
    "Füge hier den Satz ein, den du verbessern möchtest:",
    placeholder="Beispiel: Ich habe geguckt wie das mit den Zahlen ist und das war voll viel Aufwand...",
    height=100
)

# Button zum Auslösen der KI-Generierung
if st.button("Satz verbessern", type="primary"):
    if not user_input.strip():
        st.warning("Bitte gib zuerst einen Text ein!")
    else:
        with st.spinner("Ki arbeitet... Bitte einen Moment Geduld."):
            # System-Prompt definieren, um die Struktur der Antwort zu erzwingen
            system_instruction = """
            Du bist ein professioneller Text-Optimierer für wissenschaftliche Arbeiten und Berichte. 
            Deine Aufgabe ist es, den eingegebenen Satz des Nutzers in drei verschiedenen Varianten umzuformulieren.
            
            Gib IMMER genau diese drei Kategorien zurück und formatiere sie in Markdown (Nutze Fettgedruckt für die Titel):
            
            **Akademisch:** [Präzise, wissenschaftlich, sachlich und im passenden Fachjargon]
            **Kompakt:** [Auf den Punkt gebracht, ohne Füllwörter, maximale Informationsdichte]
            **Einfach:** [Leicht verständlich, klar formuliert, ohne unnötig komplizierte Schachtelsätze]
            
            Antworte ausschließlich mit den drei Varianten. Keine Begrüßung, kein Smalltalk.
            """
            
            try:
                # API-Aufruf mit dem gemini-2.5-flash Modell
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7 # Ein guter Balancewert für Kreativität und Struktur
                    )
                )
                
                st.success("Fertig! Hier sind deine Varianten:")
                st.divider()
                
                # Das Ergebnis von Gemini direkt auf der Seite anzeigen (Markdown wird unterstützt)
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Fehler bei der API-Anfrage: {e}")

