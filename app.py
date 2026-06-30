import streamlit as st
import json
import os
from datetime import datetime

# ======================
# CONFIG
# ======================
OBJECTIF_KM = 300
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
st.title("🏃‍♂️ Janouille Running Motivation")

st.write("Objectif : ", OBJECTIF_KM, "km")

# Progression
progression = data["total_km"] / OBJECTIF_KM
if progression > 1:
    progression = 1

st.progress(progression)

st.write(f"### {data['total_km']} / {OBJECTIF_KM} km")

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

if data["total_km"] >= 50:
    st.success("🥉 Bronze runner")

if data["total_km"] >= 150:
    st.success("🥈 Silver runner")

if data["total_km"] >= 300:
    st.success("🥇 Gold runner")