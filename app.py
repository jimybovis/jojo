import streamlit as st
import json
import os
from datetime import datetime

# ======================
# CONFIG
# ======================
OBJECTIF_KM = 15
FICHIER = "data.json"

# ======================
# CHARGEMENT DONNÉES
# ======================
def charger_donnees():
    if os.path.exists(FICHIER):
        with open(FICHIER, "r") as f:
            return json.load(f)
    return {
        "total_km": 0,
        "historique": []
    }

def sauvegarder_donnees(data):
    with open(FICHIER, "w") as f:
        json.dump(data, f)

data = charger_donnees()

# ======================
# INTERFACE
# ======================
st.title("🏃‍♂️ Jajou Running Motivation")
st.write("Si tu ne vas pas courir, la loutre va mourir de faim !")
st.title("🦦")
st.write("Objectif : ", OBJECTIF_KM, "km par semaine")

if "show_gif" not in st.session_state:
    st.session_state["show_gif"] = False

if st.session_state["show_gif"]:
    st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3VtOTRuem4zNDFncDN4d3o3ZjdxM2diZDlrM2h5NTNsYnJuNjduYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/11p8Lr9eVeXq2Q/giphy.gif")
    st.success("🏃‍♂️ Course ajoutée !")

    st.session_state["show_gif"] = False




progress_percent = min(data["total_km"] / OBJECTIF_KM, 1) * 100

st.markdown(f"""
<div style="position: relative; width: 100%; background-color: #eee; border-radius: 10px; height: 25px;">
  
  <div style="
    width: {progress_percent}%;
    background-color: #4CAF50;
    height: 100%;
    border-radius: 10px;
    position: relative;
  ">
    <span style="
      position: absolute;
      right: -15px;
      top: -10px;
      font-size: 20px;
    ">
      🥕
    </span>
  </div>

  <!-- loutre -->
  <div style="
    position: absolute;
    right: -10px;
    top: -12px;
    font-size: 28px;
  ">
    🦦
  </div>


</div>

<p>{int(progress_percent)}% — {data['total_km']} / {OBJECTIF_KM} km</p>
""", unsafe_allow_html=True)


if data["total_km"] >= OBJECTIF_KM:
    st.image(
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjNzbzRsemc1cDQ3cTNhMTZhdXhtZzl0bnBwcm1udzdnaW4yZHd5cSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/N52vvvIAO4SYDvTNZY/giphy.gif",
        caption="🎉 Objectif atteint ! La loutre est fière de toi 🦦"
    )




# ======================
# AJOUT KM
# ======================
st.subheader("Ajouter une course")

km = st.number_input("Kilomètres courus", min_value=0.0, step=0.1)

if st.button("Ajouter"):
    data["total_km"] += km

    data["historique"].append({
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "km": km
    })

    sauvegarder_donnees(data)

    st.session_state["show_gif"] = True
    st.rerun()



# ======================
# RESET
# ======================

st.subheader("Reset")

if st.button("Réinitialiser tout"):
    data["total_km"] = 0
    data["historique"] = []
    sauvegarder_donnees(data)
    st.rerun()


# ======================
# HISTORIQUE
# ======================
st.subheader("Historique")

for course in reversed(data["historique"]):
    st.write(f"📅 {course['date']} — {course['km']} km")

# ======================
# BADGES MOTIVATION
# ======================
st.subheader("Badges")

if data["total_km"] >= 5:
    st.success("🥉 Bien joué ma Petite Loutre, fonce !")

if data["total_km"] >= 10:
    st.success("🥈 ça c'est ma copine à moi !")

if data["total_km"] >= 15:
    st.success("🥇 Trop forte, je suis fier de toi mon ptit citron 🍋")