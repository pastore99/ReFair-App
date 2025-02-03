import tkinter as tk
from tkinter import messagebox
import json
import requests
from datetime import datetime

class RatingWindow(tk.Toplevel):
    def __init__(self, parent, user_story, predicted_domain, features):
        super().__init__(parent)
        self.title("Rate the Analysis")
        self.geometry("350x300")
        self.transient(parent)  # La finestra è figlia della principale
        self.grab_set()         # Blocca l'interazione con la finestra principale

        self.user_story = user_story
        self.predicted_domain = predicted_domain
        self.features = features

        # Titolo della finestra
        tk.Label(self, text="Rate the accuracy of the predictions", font=("Arial", 12, "bold")).pack(pady=5)

        # Rating per la predizione del dominio
        tk.Label(self, text="How accurate is the domain prediction?").pack()
        self.domain_rating_var = tk.IntVar(value=0)
        self.add_rating_options(self.domain_rating_var)

        # Rating per la predizione dei tasks
        tk.Label(self, text="How accurate is the ML tasks prediction?").pack()
        self.tasks_rating_var = tk.IntVar(value=0)
        self.add_rating_options(self.tasks_rating_var)

        # Campo per eventuale feedback aggiuntivo
        tk.Label(self, text="Additional feedback (optional):").pack(pady=(10, 0))
        self.feedback_entry = tk.Entry(self, width=40)
        self.feedback_entry.pack(pady=5)

        # Pulsanti di submit e chiusura
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        submit_button = tk.Button(button_frame, text="Submit", command=self.submit_rating)
        submit_button.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(button_frame, text="Close", command=self.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)

    def add_rating_options(self, variable):
        """Aggiunge i radiobutton per la valutazione da 1 a 5."""
        rating_frame = tk.Frame(self)
        rating_frame.pack()
        for i in range(1, 6):
            tk.Radiobutton(rating_frame, text=str(i), variable=variable, value=i).pack(side=tk.LEFT, padx=5)

    def submit_rating(self):
        """Invia il feedback ai due endpoint e chiude la finestra se il tutto va a buon fine."""
        domain_rating = self.domain_rating_var.get()
        tasks_rating = self.tasks_rating_var.get()
        additional_feedback = self.feedback_entry.get().strip()  # Recupera il testo di feedback aggiuntivo

        # Verifica che entrambi i rating siano stati selezionati
        if domain_rating == 0 or tasks_rating == 0:
            messagebox.showwarning("Warning", "Please rate both predictions before submitting.")
            return

        # Costruisci il payload per il feedback del dominio
        const_domain_payload = {
            "user_story": self.user_story,
            "predicted_domain": self.predicted_domain,
            "feedback_value": domain_rating
        }

        # Costruisci il payload per il feedback dei tasks
        const_tasks_payload = {
            "user_story": self.user_story,
            "domain": self.predicted_domain,
            "predicted_tasks": self.features,
            "feedback_value": tasks_rating
        }

        try:
            # Invia la richiesta POST per il feedback del dominio
            r1 = requests.post("http://127.0.0.1:8080/feedback/domain", json=const_domain_payload)
            r1.raise_for_status()  # Solleva un'eccezione se la risposta non è OK

            # Invia la richiesta POST per il feedback dei tasks
            r2 = requests.post("http://127.0.0.1:8080/feedback/tasks", json=const_tasks_payload)
            r2.raise_for_status()

            messagebox.showinfo("Success", "Thank you for your feedback!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while submitting the rating: {e}")