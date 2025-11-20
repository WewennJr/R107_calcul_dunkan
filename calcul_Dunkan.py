#### Importation des modules
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
from openpyxl import load_workbook
import os
import sys

# --- CONFIGURATION DES POLICES ---
FONT_TEXTE = ("Arial", 14)
FONT_GRAS = ("Arial", 14, "bold")
FONT_TITRE = ("Arial", 22, "bold")
FONT_BOUTON = ("Arial", 16, "bold")

# --- Utilitaire pour le chemin du fichier ---
def get_excel_path():
    dossier_courant = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dossier_courant, "Coef_Excel.xlsx")

#NOUVELLE FONCTION : Chargement des labels (R101, SAE...)
def charger_labels_depuis_excel():
    fichier = get_excel_path()
    liste_res = []
    liste_sae = []
    
    try:
        wb = load_workbook(fichier, data_only=True)
        ws = wb["Feuil1"]
        
        # On parcourt les lignes pour trouver les noms (Colonne A / index 0) + Fais le meme nombre d'itération que de matières
        for row in ws.iter_rows(values_only=True):
            # On vérifie qu'il y a bien des coefs associés (pour éviter les lignes vides)
            if row and len(row) >= 4 and isinstance(row[1], (int, float)):
                label = str(row[0]) # Le nom (ex: R101)
                
                # Tri automatique Ressources vs SAE
                if label.upper().startswith("R"):
                    liste_res.append(label)
                elif label.upper().startswith("S"): # Pour SAE
                    liste_sae.append(label)
                else:
                    # Si c'est un autre nom, on le met par défaut dans ressources car SAE situation spécifique
                    liste_res.append(label)
                    
        wb.close()
        return liste_res, liste_sae

    except FileNotFoundError:
        print(f"ERREUR CRITIQUE : Le fichier {fichier} est introuvable au démarrage.")
        return [], [] # Retourne des listes vides en cas d'erreur
    except Exception as e:
        print(f"Erreur lecture labels : {e}")
        return [], []

# --- Fonction de calcul (Calcul des moyennes)
def coef2(notes):
    alistR = notes
    nom_fichier_excel = get_excel_path()
    
    coefUE1, coefUE2, coefUE3 = [], [], []

    try:
        wb = load_workbook(nom_fichier_excel, data_only=True)
        ws = wb["Feuil1"] 
        for row in ws.iter_rows(values_only=True):
            if row and len(row) >= 4 and isinstance(row[1], (int, float)):
                coefUE1.append(row[1])
                coefUE2.append(row[2])
                coefUE3.append(row[3])
        wb.close()
    except Exception as e:
        print(f"Erreur Excel lors du calcul : {e}")
        return None, None, None, None

    try:
        S1 = np.average(alistR, weights=coefUE1)
        S2 = np.average(alistR, weights=coefUE2)
        S3 = np.average(alistR, weights=coefUE3)
    except Exception as e:
        print(f"Erreur de calcul numpy : {e}")
        return None, None, None, None

    # Graphique
    def get_color(value):
        if value >= 10: return "#4CAF50"
        elif value >= 8: return "#FF9800"
        else: return "#F44336"

    colors = [get_color(value) for value in [S1, S2, S3]]
    
    fig, ax = plt.subplots(figsize=(5, 4), facecolor="white")
    bars = ax.bar(["UE1", "UE2", "UE3"], [S1, S2, S3], width=0.5, color=colors)
    
    ax.set_title("Moyennes par UE", fontsize=14, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_ylim(0, 20)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.2, round(yval, 2), 
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    dossier_courant = os.path.dirname(os.path.abspath(__file__))
    chemin_graphique = os.path.join(dossier_courant, "Diagrame.jpg")
    plt.tight_layout()
    fig.savefig(chemin_graphique, dpi=100, bbox_inches="tight") 
    plt.close(fig)

    return S1, S2, S3, chemin_graphique

# --- INITIALISATION DES DONNÉES ---
ressources, sae = charger_labels_depuis_excel()

# Si le fichier n'est pas trouvé ou vide
if not ressources and not sae:
    print("Attention : Aucune donnée trouvée dans Excel. Vérifiez le fichier.")
    ressources = ["Erreur"]
    sae = ["Fichier?"]

# --- INTERFACE GRAPHIQUE ---
fenetre = tk.Tk()
fenetre.title("Calculateur de Moyennes R&T")
fenetre.configure(bg="#f0f4f8")
fenetre.geometry("1300x900") 

fenetre.columnconfigure(0, weight=1)
fenetre.columnconfigure(1, weight=1)
fenetre.rowconfigure(1, weight=1)

# Titre
tk.Label(fenetre, text="Calcul des Moyennes UE (Via Excel)", 
         font=FONT_TITRE, bg="#f0f4f8", fg="#333").grid(row=0, column=0, columnspan=2, pady=30)

# --- CADRE GAUCHE : LES NOTES ---
frame_gauche = tk.Frame(fenetre, bg="#f0f4f8")
frame_gauche.grid(row=1, column=0, sticky="nsew", padx=40)

entrees = [] 

# 1. Affichage des Ressources
tk.Label(frame_gauche, text="Ressources", font=FONT_BOUTON, bg="#f0f4f8", fg="#0056b3").grid(row=0, column=0, pady=15)

for i, res in enumerate(ressources):
    tk.Label(frame_gauche, text=res, font=FONT_GRAS, bg="#f0f4f8").grid(row=i+1, column=0, padx=10, pady=4, sticky="e")
    entree = tk.Entry(frame_gauche, width=8, font=FONT_TEXTE, justify="center")
    entree.grid(row=i+1, column=1, padx=10, pady=4)
    entrees.append(entree)

# 2. Affichage des SAE
tk.Label(frame_gauche, text="SAE", font=FONT_BOUTON, bg="#f0f4f8", fg="#0056b3").grid(row=0, column=2, pady=15, padx=(50,0))

for i, s in enumerate(sae):
    tk.Label(frame_gauche, text=s, font=FONT_GRAS, bg="#f0f4f8").grid(row=i+1, column=2, padx=(50,10), pady=4, sticky="e")
    entree = tk.Entry(frame_gauche, width=8, font=FONT_TEXTE, justify="center")
    entree.grid(row=i+1, column=3, padx=10, pady=4)
    entrees.append(entree)


# --- CADRE DROIT : RÉSULTATS ---
frame_droit = tk.Frame(fenetre, bg="white", bd=2, relief="groove")
frame_droit.grid(row=1, column=1, sticky="nsew", padx=40, pady=40)
frame_droit.columnconfigure(0, weight=1)

resultat_label = tk.Label(frame_droit, text="En attente de validation...", 
                          font=FONT_TEXTE, bg="white", justify="left")
resultat_label.grid(row=0, column=0, pady=30, sticky="w", padx=30)

canvas = tk.Canvas(frame_droit, bg="white", highlightthickness=0)
canvas.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

btn_valider = tk.Button(frame_droit, text="VALIDER LES NOTES", 
                        font=FONT_BOUTON, bg="#4CAF50", fg="white", 
                        activebackground="green", relief="flat", padx=20, pady=10)
btn_valider.grid(row=2, column=0, pady=30)


# --- FONCTION LOGIQUE ---
def recuperer_infos():
    try:
        notes = []
        for e in entrees:
            val = e.get().replace(',', '.') 
            if val == "": val = "0"
            notes.append(float(val))
            
        result = coef2(notes)
        
        if result[0] is None:
            resultat_label.config(text="Erreur: Vérifiez le fichier Excel 'Coef_Excel.xlsx'.", fg="red")
            return
            
        S1, S2, S3, chemin_img = result

        # --- MODIFICATION ICI : Remplacement du point par un tiret simple ---
        resultat_label.config(
            text=f"CALCUL RÉUSSI :\n\n"
                 f"- UE 1 : {S1:.2f} / 20\n"
                 f"- UE 2 : {S2:.2f} / 20\n"
                 f"- UE 3 : {S3:.2f} / 20",
            fg="#333"
        )

        # Affichage Image
        canvas.delete("all")
        try:
            img = Image.open(chemin_img)
            img = img.resize((600, 450), Image.Resampling.LANCZOS) 
            photo = ImageTk.PhotoImage(img)
            canvas.image = photo
            
            canvas.config(width=600, height=450)
            canvas.create_image(300, 225, image=photo)
        except Exception as e:
            print(f"Erreur image: {e}")

    except ValueError:
        resultat_label.config(text="Erreur : Entrez seulement des chiffres.", fg="red")

btn_valider.config(command=recuperer_infos)

fenetre.mainloop()