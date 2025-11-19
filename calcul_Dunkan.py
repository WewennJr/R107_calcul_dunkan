#### Importation des modules
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk

# --- Fonction de calcul ---
def coef2(notes):
    alistR = notes
    coefUE1 = [10,10,7,7,0,5,0,6,0,5,4,2,5,5,0,20,20,0,0,0,7]
    coefUE2 = [4,0,2,8,6,0,0,0,0,5,5,2,9,9,3,0,0,29,0,0,7]
    coefUE3 = [4,0,2,0,0,5,15,6,4,5,5,2,0,0,3,0,0,0,20,20,7]

    S1 = np.average(alistR, weights=coefUE1)
    S2 = np.average(alistR, weights=coefUE2)
    S3 = np.average(alistR, weights=coefUE3)

    def get_color(value):
        if value >= 10:
            return 'green'
        elif value >=8 and value<10:
            return 'orange'
        else:
            return 'red'

    colors = [get_color(value) for value in [S1, S2, S3]]

    plt.bar(["UE1","UE2","UE3"], [S1,S2,S3], width = 0.5, color=colors )
    plt.title("Diagramme des UE")
    plt.xlabel("UE")
    plt.ylabel("Notes")
    plt.savefig("Diagrame.jpg")
    plt.close()  # Ferme le graphique pour éviter les superpositions invisibles quabd on rappuie sur valider par exemple


    return S1, S2, S3

### Interface graphique ###
fenetre = tk.Tk()
fenetre.geometry("900x650")
fenetre.title("Fenêtre de calcul de UE")
fenetre.configure(bg="#dbe8f1")

# Titre
titre = tk.Label(fenetre, text="Veuillez entrer vos notes pour les ressources et SAE",
                 font=("Arial", 12, "bold"), bg="#dbe8f1")
titre.place(x=250, y=10)

# Liste des ressources et SAE
ressources = ["R"+str(i) for i in range(101,116)]
sae = ["SAE11","SAE12","SAE13","SAE14","SAE15","SAE16"]

# Entrées
entrees = []

# Colonne gauche → ressources
x_res, y_start = 50, 50
for i, res in enumerate(ressources):
    tk.Label(fenetre, text=res, width=6, bg="#dbe8f1").place(x=x_res, y=y_start + i*30)
    entree = tk.Entry(fenetre, width=6)
    entree.place(x=x_res+50, y=y_start + i*30)
    entrees.append(entree)

# Colonne droite → SAE
x_sae = 200
for i, s in enumerate(sae):
    tk.Label(fenetre, text=s, width=6, bg="#dbe8f1").place(x=x_sae, y=y_start + i*30)
    entree = tk.Entry(fenetre, width=6)
    entree.place(x=x_sae+50, y=y_start + i*30)
    entrees.append(entree)

# Canvas pour l'image
canvas = tk.Canvas(fenetre, width=400, height=300)
canvas.place(x=500, y=300)
image_on_canvas = None  # Variable globale pour suivre l'image affichée

# Fonction du bouton Valider

# Fonction du bouton Valider
def recuperer_infos():
    global image_on_canvas
    try:
        notes = [float(e.get()) for e in entrees]
        S1, S2, S3 = coef2(notes)

        # Supprime l'image précédente du canvas
        canvas.delete("all")

        # Recharger l'image à chaque fois
        img = Image.open("Diagrame.jpg")
        img = img.resize((400, 300))  # Redimensionnement
        photo = ImageTk.PhotoImage(img)

        # Mettre à jour la référence pour éviter le "garbage collection"
        canvas.image = photo 
        image_on_canvas = canvas.create_image(0, 0, image=photo, anchor="nw")

        # Affichage du résultat
        resultat_label.config(
            text=f"Résultats :\nUE1 → {S1:.2f}/20\nUE2 → {S2:.2f}/20\nUE3 → {S3:.2f}/20",
            fg="green"
            
        )
    except ValueError:
        resultat_label.config(
            text="Attention Erreur : veuillez entrer uniquement des nombres valides.",
            fg="red"
        )



# Bouton Valider
tk.Button(fenetre, text="Valider", command=recuperer_infos, bg="lightgreen", font=("Arial", 11)).place(x=200, y=550)

# Zone de résultat
resultat_label = tk.Label(fenetre, text="", font=("Arial", 12), bg="#dbe8f1", justify="left", anchor="nw")
resultat_label.place(x=200, y=250, width=300, height=200)

fenetre.mainloop()
