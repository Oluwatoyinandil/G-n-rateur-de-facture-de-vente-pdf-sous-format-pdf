# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 15:47:12 2025

@author: INFO
"""
#Ce mini projet a pour but de créer un générateur automatique de factures pdf en Python

import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
from datetime import datetime
import os

# Liste des produits ajoutés
produits = []

def ajouter_produit():
    desc = entry_description.get().strip()
    try:
        quantite = int(entry_quantite.get())
        prix = float(entry_prix.get())
    except ValueError:
        label_message.config(text="Quantité et Prix doivent être valides.", fg="red")
        return

    if not desc:
        label_message.config(text="La description est requise.", fg="red")
        return

    produits.append({
        "description": desc,
        "quantite": quantite,
        "prix": prix
    })

    listbox_produits.insert(tk.END, f"{desc} | Qté: {quantite} | PU: {prix:.2f} FCFA")
    entry_description.delete(0, tk.END)
    entry_quantite.delete(0, tk.END)
    entry_prix.delete(0, tk.END)
    label_message.config(text="Produit ajouté.", fg="green")

def generer_facture():
    nom = entry_nom.get().strip()
    adresse = entry_adresse.get().strip()

    if not nom or not produits:
        label_message.config(text="Nom du client et au moins un produit requis.", fg="red")
        return

    dossier = filedialog.askdirectory(title="Choisir un dossier de sauvegarde")
    if not dossier:
        label_message.config(text="Aucun dossier sélectionné.", fg="red")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    date_facture = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(200, 10, txt="FACTURE", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Date : {date_facture}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Nom du client : {nom}", ln=True)
    pdf.cell(200, 10, txt=f"Adresse : {adresse}", ln=True)
    pdf.ln(10)

    # En-tête du tableau
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(80, 10, "Description", border=1)
    pdf.cell(30, 10, "Quantité", border=1)
    pdf.cell(40, 10, "PU (FCFA)", border=1)
    pdf.cell(40, 10, "Total HT", border=1)
    pdf.ln()

    pdf.set_font("Arial", size=12)
    total_ht = 0
    for produit in produits:
        total_ligne = produit["quantite"] * produit["prix"]
        total_ht += total_ligne
        pdf.cell(80, 10, produit["description"], border=1)
        pdf.cell(30, 10, str(produit["quantite"]), border=1)
        pdf.cell(40, 10, f"{produit['prix']:.2f}", border=1)
        pdf.cell(40, 10, f"{total_ligne:.2f}", border=1)
        pdf.ln()

    tva = total_ht * 0.18
    total_ttc = total_ht + tva

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"TVA (18%) : {tva:.2f} FCFA", ln=True)
    pdf.cell(200, 10, txt=f"Total TTC : {total_ttc:.2f} FCFA", ln=True)

    # Création du chemin complet
    nom_fichier = f"facture_{nom.lower().replace(' ', '_')}.pdf"
    chemin_complet = os.path.join(dossier, nom_fichier)
    pdf.output(chemin_complet)

    label_message.config(text=f"Facture enregistrée dans :\n{chemin_complet}", fg="green")

# Interface
root = tk.Tk()
root.title("Générateur de Factures avec Tableau")

tk.Label(root, text="Nom du client").pack()
entry_nom = tk.Entry(root, width=40)
entry_nom.pack()

tk.Label(root, text="Adresse").pack()
entry_adresse = tk.Entry(root, width=40)
entry_adresse.pack()

tk.Label(root, text="Description du produit").pack()
entry_description = tk.Entry(root, width=40)
entry_description.pack()

tk.Label(root, text="Quantité").pack()
entry_quantite = tk.Entry(root, width=40)
entry_quantite.pack()

tk.Label(root, text="Prix unitaire (FCFA)").pack()
entry_prix = tk.Entry(root, width=40)
entry_prix.pack()

tk.Button(root, text="Ajouter un produit", command=ajouter_produit).pack(pady=5)

listbox_produits = tk.Listbox(root, width=60)
listbox_produits.pack()

tk.Button(root, text="Générer la facture", command=generer_facture).pack(pady=10)

label_message = tk.Label(root, text="", wraplength=400)
label_message.pack()

root.mainloop()






    
            

