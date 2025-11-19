#### Importation des modules
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import pandas as pd  # Importation de pandas


# --- Fonction de calcul ---
def coef2(notes):
    """
    Calcule les moyennes des UE en lisant les coefficients
    depuis le fichier 'Coef_Excel.xlsx'.
    """
    alistR = notes
    nom_fichier_excel = "Coef_Excel.xlsx"

    try:
        df = pd.read_excel(
            nom_fichier_excel,
            sheet_name="Feuil1",
            header=None,
            names=["Label", "CoefUE1", "CoefUE2", "CoefUE3"],
        )

        coefUE1 = df["CoefUE1"].tolist()
        coefUE2 = df["CoefUE2"].tolist()
        coefUE3 = df["CoefUE3"].tolist()

    except FileNotFoundError:
        print(f"Erreur: Le fichier {nom_fichier_excel} est introuvable.")
        return None, None, None
    except Exception as e:
        print(f"Erreur lors de la lecture du Excel : {e}")
        return None, None, None

    # --- Calcul des moyennes pondérées ---
    S1 = np.average(alistR, weights=coefUE1)
    S2 = np.average(alistR, weights=coefUE2)
    S3 = np.average(alistR, weights=coefUE3)

    # --- Création du graphique ---
    def get_color(value):
        if value >= 10:
            return "green"
        elif value >= 8:
            return "orange"
        else:
            return "red"

    colors = [get_color(value) for value in [S1, S2, S3]]

    fig, ax = plt.subplots(figsize=(3.6, 2.4), facecolor="white") 
    ax.bar(["UE1", "UE2", "UE3"], [S1, S2, S3], width=0.5, color=colors)
    ax.set_title("Diagramme des UE", fontsize=9)
    ax.set_ylim(0, 20)

    plt.tight_layout()
    fig.savefig("Diagrame.jpg", dpi=120, bbox_inches="tight", pad_inches=0, facecolor="white")
    plt.close(fig)

    return S1, S2, S3


### Interface graphique ###
fenetre = tk.Tk()
fenetre.geometry("900x650")
fenetre.title("Fenêtre de calcul de UE")
fenetre.configure(bg="#dbe8f1")

# Titre
titre = tk.Label(
    fenetre,
    text="Veuillez entrer vos notes pour les ressources et SAE",
    font=("Arial", 12, "bold"),
    bg="#dbe8f1",
)
titre.place(x=250, y=10)

# Liste des ressources et SAE
ressources = ["R" + str(i) for i in range(101, 116)]
sae = ["SAE11", "SAE12", "SAE13", "SAE14", "SAE15", "SAE16"]
tous_les_labels = ressources + sae

# Entrées
entrees = []

# Colonne gauche → ressources
x_res, y_start = 50, 50
for i, res in enumerate(ressources):
    tk.Label(fenetre, text=res, width=6, bg="#dbe8f1").place(x=x_res, y=y_start + i * 30)
    entree = tk.Entry(fenetre, width=6)
    entree.place(x=x_res + 50, y=y_start + i * 30)
    entrees.append(entree)

# Colonne droite → SAE
x_sae = 200
for i, s in enumerate(sae):
    tk.Label(fenetre, text=s, width=6, bg="#dbe8f1").place(x=x_sae, y=y_start + i * 30)
    entree = tk.Entry(fenetre, width=6)
    entree.place(x=x_sae + 50, y=y_start + i * 30)
    entrees.append(entree)

# Encadré
canvas = tk.Canvas(fenetre, width=340, height=240, bg="white", highlightthickness=0) # Hauteur augmentée
# --- FIN MODIFIÉ ---
canvas.place(x=540, y=390)
image_on_canvas = None


# --- Fonction du bouton Valider ---
def recuperer_infos():
    global image_on_canvas
    try:
        notes = [float(e.get()) for e in entrees]
        S1, S2, S3 = coef2(notes)
        
        # Gestion de l'erreur si Excel n'est pas trouvé
        if S1 is None:
            resultat_label.config(
                text="Erreur : Impossible de lire 'Coef_Excel.xlsx'.\n"
                     "Vérifiez sa présence ou le nom de l'onglet 'Feuil1'.",
                fg="red"
            )
            return

        # Enregistrer les notes
        nom_fichier = "Notes.txt"
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            fichier.write("=== Sauvegarde des notes ===\n\n")
            for k, note in zip(tous_les_labels, notes):
                fichier.write(f"{k}: {note}\n")

        # --- Afficher le graphique ---
        canvas.delete("all")
        img = Image.open("Diagrame.jpg")

        # --- MODIFIÉ ICI (hauteur) ---
        img = img.resize((340, 240), Image.Resampling.LANCZOS) # Hauteur augmentée
        # --- FIN MODIFIÉ ---
        photo = ImageTk.PhotoImage(img)

        canvas.image = photo
        canvas.create_image(0, 0, image=photo, anchor="nw")

        # Affichage du résultat
        resultat_label.config(
            text=(
                f"Résultats :\nUE1 → {S1:.2f}/20\nUE2 → {S2:.2f}/20\nUE3 → {S3:.2f}/20"
                f"\n\nNotes enregistrées dans '{nom_fichier}'"
            ),
            fg="green",
        )

    except ValueError:
        resultat_label.config(
            text="Erreur : veuillez entrer uniquement des nombres valides.", fg="red"
        )
    except FileNotFoundError:
        resultat_label.config(
            text="Erreur : Fichier 'Diagrame.jpg' non trouvé.\nValidez une première fois.",
            fg="red",
        )
    except Exception as e:
        resultat_label.config(text=f"Une erreur est survenue : {e}", fg="red")


# --- Bouton Valider ---
tk.Button(
    fenetre, text="Valider", command=recuperer_infos, bg="lightgreen", font=("Arial", 11)
).place(x=200, y=550)

# --- Zone de résultat ---
resultat_label = tk.Label(
    fenetre, text="", font=("Arial", 12), bg="#dbe8f1", justify="left", anchor="nw"
)
resultat_label.place(x=200, y=250, width=320, height=200) # Largeur réduite

fenetre.mainloop()