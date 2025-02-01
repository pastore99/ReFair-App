import tkinter as tk
from tkinter import messagebox
import json

class RatingWindow(tk.Toplevel):
    def __init__(self, parent, user_story, predicted_domain, features):
        super().__init__(parent)
        self.title("Rate the Analysis")
        self.geometry("350x300")
        self.transient(parent)  # La finestra è figlia della principale
        self.grab_set()  # Blocca l'interazione con la finestra principale

        self.user_story = user_story
        self.predicted_domain = predicted_domain
        self.features = features

        # **Titolo della finestra**
        tk.Label(self, text="Rate the accuracy of the predictions", font=("Arial", 12, "bold")).pack(pady=5)

        # **Rating per la predizione del dominio**
        tk.Label(self, text="How accurate is the domain prediction?").pack()
        self.domain_rating_var = tk.IntVar(value=0)
        self.add_rating_options(self.domain_rating_var)

        # **Rating per la predizione dei tasks**
        tk.Label(self, text="How accurate is the ML tasks prediction?").pack()
        self.tasks_rating_var = tk.IntVar(value=0)
        self.add_rating_options(self.tasks_rating_var)

        # **Pulsanti di submit e chiusura**
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        submit_button = tk.Button(button_frame, text="Submit", command=self.submit_rating)
        submit_button.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(button_frame, text="Close", command=self.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)

    def add_rating_options(self, variable):
        """ Aggiunge i radiobutton per la valutazione da 1 a 5 """
        rating_frame = tk.Frame(self)
        rating_frame.pack()
        for i in range(1, 6):
            tk.Radiobutton(rating_frame, text=str(i), variable=variable, value=i).pack(side=tk.LEFT, padx=5)

    def submit_rating(self):
        """ Salva il feedback e chiude la finestra """
        domain_rating = self.domain_rating_var.get()
        tasks_rating = self.tasks_rating_var.get()
        feedback_text = self.feedback_entry.get().strip()

        if domain_rating == 0 or tasks_rating == 0:
            messagebox.showwarning("Warning", "Please rate both predictions before submitting.")
            return

        feedback = {
            "user_story": self.user_story,
            "predicted_domain": self.predicted_domain,
            "features": self.features,
            "domain_rating": domain_rating,
            "tasks_rating": tasks_rating,
            "additional_feedback": feedback_text
        }

        # **Salvataggio su JSON**
        with open("ratings.json", "a") as file:
            json.dump(feedback, file)
            file.write("\n")

        messagebox.showinfo("Success", "Thank you for your feedback!")
        self.destroy()
