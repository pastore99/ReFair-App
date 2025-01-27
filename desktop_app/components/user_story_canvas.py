import tkinter as tk
from tkinter import Scrollbar, Canvas, Frame, Label, Button
from tkinter import messagebox

from components.custom_messagebox import CustomMessageBox

from domain_utils import getDomain, getMLTask


class UserStoryCanvas(Frame):
    def __init__(self, parent, user_stories, wrap_length=800, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Inizializza il Canvas e lo Scrollbar
        self.canvas = Canvas(self, bg="white")  # Sfondo bianco del Canvas
        self.scrollbar = Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Posiziona il Canvas e lo Scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crea il frame interno al Canvas
        self.content_frame = Frame(self.canvas, bg="white")  # Sfondo bianco del frame contenente le User Stories
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Inserisci le User Stories nel Canvas
        self.populate_user_stories(user_stories, wrap_length)
        
        # Aggiorna la regione scrollabile del Canvas
        self.content_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def populate_user_stories(self, user_stories, wrap_length):
        for us in user_stories:
            # Crea una riga per ogni User Story
            row_frame = Frame(self.content_frame, bg="#FFFFFF", pady=10)  # Padding di 10px intorno a ogni riga
            row_frame.pack(fill=tk.X, pady=2)

            # Etichetta per la User Story con wrapping del testo
            us_label = Label(row_frame, text=us, anchor="w", wraplength=wrap_length, justify="left", background="#FFFFFF")
            us_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            # Pulsante "Analyze"
            analyze_button = Button(row_frame, text="Analyze", command=lambda us=us: self.analyze(us))
            analyze_button.pack(side=tk.RIGHT, padx=5)
            
            # Linea di separazione nera
            separator = Frame(self.content_frame, height=1, bd=1, relief=tk.SUNKEN, bg="black")
            separator.pack(fill=tk.X, padx=5, pady=5)

    def analyze(self, user_story):
        # Chiama la funzione getDomain e aggiorna la label con il risultato
        predicted_domain = getDomain(user_story)
        results = getMLTask(user_story, predicted_domain)

        feauters_extracted = results["tasks_features"]

        CustomMessageBox(self, predicted_domain, user_story, predicted_domain, feauters_extracted)