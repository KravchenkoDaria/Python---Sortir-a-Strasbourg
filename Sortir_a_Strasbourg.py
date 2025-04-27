# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 23:40:19 2025

@author: kdash
"""

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests
from datetime import datetime, timedelta

# --- CONFIGURATION ---
API_KEY = "3d9621a41cf2ebb3c8cf62262ecd27a3"
CITY = "Strasbourg,FR"
lang = "fr"

# --- TEXTES ---
texts = {
    "fr": {
        "title": "Que faire à Strasbourg ?",
        "choose_date": "Choisissez une date (5 jours max) :",
        "show": "Afficher les recommandations",
        "forecast": "Prévisions météo pour le",
        "temperature": "Température",
        "rain": "Pluie",
        "description": "Description",
        "transport": "🚍 Transport recommandé",
        "activities": "🎉 Activités recommandées",
        "error": "Erreur",
        "no_data": "Aucune donnée météo disponible.",
        "lang_button": "🇬🇧 English",
        "see_cinemas": "🎬 Voir les cinémas",
        "see_museums": "🏛 Voir les musées",
        "see_malls": "🛍 Voir les centres commerciaux"
    },
    "en": {
        "title": "What to do in Strasbourg?",
        "choose_date": "Choose a date (next 5 days):",
        "show": "Show recommendations",
        "forecast": "Weather forecast for",
        "temperature": "Temperature",
        "rain": "Rain",
        "description": "Description",
        "transport": "🚍 Recommended transport",
        "activities": "🎉 Recommended activities",
        "error": "Error",
        "no_data": "No weather data available.",
        "lang_button": "🇫🇷 Français",
        "see_cinemas": "🎬 View cinemas",
        "see_museums": "🏛 View museums",
        "see_malls": "🛍 View shopping centers"
    }
}

# --- DONNÉES ---
centres_commerciaux = [
    ("Rivetoile", "https://www.rivetoile.com"),
    ("Place des Halles", "https://www.placedeshalles.com")
]

musees = [
    ("Musée d’Art Moderne", "https://www.musees.strasbourg.eu/musee-d-art-moderne-et-contemporain"),
    ("Musée Alsacien", "https://www.musees.strasbourg.eu/musee-alsacien"),
    ("Musée Historique", "https://www.musees.strasbourg.eu/musee-historique"),
    ("Musée Tomi Ungerer", "https://www.musees.strasbourg.eu/musee-tomi-ungerer"),
    ("Musée de l’Œuvre Notre-Dame", "https://www.musees.strasbourg.eu/musee-de-l-oeuvre-notre-dame")
]

cinemas = [
    ("Cinéma Star", "https://www.cinema-star.com/films-a-l-affiche/"),
    ("UGC Ciné Vox", "https://www.ugc.fr/cinema.html?id=37"),
    ("CGR Strasbourg VOX", "https://www.cgrcinemas.fr/strasbourg/")
]

# --- MÉTÉO ---
def get_dates():
    return [(datetime.now() + timedelta(i)).strftime("%Y-%m-%d") for i in range(5)]

def get_weather(date_str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang={lang}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    for item in data["list"]:
        if item["dt_txt"].startswith(date_str):
            temp = item["main"]["temp"]
            rain = "rain" in item["weather"][0]["main"].lower()
            desc = item["weather"][0]["description"]
            return {"temp": temp, "rain": rain, "desc": desc}
    return None

# --- INTERACTIONS ---
def open_url(url):
    webbrowser.open_new_tab(url)

def create_window(title, items):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("600x400")
    ttk.Label(win, text=title, font=("Helvetica", 14, "bold")).pack(pady=10)
    for name, url in items:
        ttk.Button(win, text=name, command=lambda u=url: open_url(u)).pack(anchor="w", padx=20, pady=3)

def show_shopping():
    create_window(texts[lang]["see_malls"], centres_commerciaux)

def show_museums():
    create_window(texts[lang]["see_museums"], musees)

def show_cinemas():
    create_window(texts[lang]["see_cinemas"], cinemas)

def show_recommendations():
    for w in result_frame.winfo_children():
        w.destroy()
    date_str = date_var.get()
    data = get_weather(date_str)
    if not data:
        messagebox.showerror(texts[lang]["error"], texts[lang]["no_data"])
        return

    ttk.Label(result_frame, text=f"📅 {texts[lang]['forecast']} {date_str}", font=("Helvetica", 13, "bold")).pack(anchor="w")
    ttk.Label(result_frame, text=f"{texts[lang]['temperature']}: {data['temp']} °C").pack(anchor="w")
    ttk.Label(result_frame, text=f"{texts[lang]['rain']}: {'Oui' if data['rain'] else 'Non'}").pack(anchor="w")
    ttk.Label(result_frame, text=f"{texts[lang]['description']}: {data['desc']}").pack(anchor="w")

    ttk.Label(result_frame, text=f"\n{texts[lang]['transport']}:", font=("Helvetica", 13, "bold")).pack(anchor="w")
    transport = "Tramway ou bus 🚋" if data['rain'] else "Vélo ou marche 🚴" if data['temp'] > 25 else "Tous moyens 🚶‍♂️🚋"
    ttk.Label(result_frame, text="→ " + transport).pack(anchor="w")

    ttk.Label(result_frame, text=f"\n{texts[lang]['activities']}:", font=("Helvetica", 13, "bold")).pack(anchor="w")
    if data['rain']:
        ttk.Button(result_frame, text=texts[lang]['see_cinemas'], command=show_cinemas).pack(anchor="w", padx=10, pady=2)
        ttk.Button(result_frame, text=texts[lang]['see_museums'], command=show_museums).pack(anchor="w", padx=10, pady=2)
        ttk.Button(result_frame, text=texts[lang]['see_malls'], command=show_shopping).pack(anchor="w", padx=10, pady=2)
    else:
        ttk.Button(result_frame, text="Cathédrale de Strasbourg", command=lambda: open_url("https://www.visitstrasbourg.fr/en/fiche-sit/F223007269_the-cathedral-of-notre-dame-strasbourg/")).pack(anchor="w", padx=10, pady=2)
        ttk.Button(result_frame, text="Balade en bateau - Batorama", command=lambda: open_url("https://www.batorama.com")).pack(anchor="w", padx=10, pady=2)
        ttk.Button(result_frame, text="Quartier de la Petite France", command=lambda: open_url("https://www.visit.alsace/223007616-la-petite-france/")).pack(anchor="w", padx=10, pady=2)

# --- LANGUE ---
def switch_lang():
    global lang
    lang = "en" if lang == "fr" else "fr"
    title_label.config(text=texts[lang]["title"])
    date_label.config(text=texts[lang]["choose_date"])
    show_button.config(text=texts[lang]["show"])
    lang_button.config(text=texts[lang]["lang_button"])
    show_recommendations()

# --- INTERFACE ---
root = tk.Tk()
root.title("Guide Strasbourg")
root.geometry("750x600")

style = ttk.Style()
style.theme_use("default")

title_label = ttk.Label(root, text=texts[lang]["title"], font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

date_label = ttk.Label(root, text=texts[lang]["choose_date"])
date_label.pack()
date_var = tk.StringVar(value=get_dates()[0])
date_box = ttk.Combobox(root, textvariable=date_var, values=get_dates(), state="readonly")
date_box.pack(pady=5)

show_button = ttk.Button(root, text=texts[lang]["show"], command=show_recommendations)
show_button.pack(pady=5)

lang_button = ttk.Button(root, text=texts[lang]["lang_button"], command=switch_lang)
lang_button.pack(pady=5)

result_frame = tk.Frame(root)
result_frame.pack(fill="both", expand=True, padx=20, pady=10)

root.mainloop()
