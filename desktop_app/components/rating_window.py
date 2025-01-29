import tkinter as tk
from tkinter import messagebox
import json

class RatingWindow(tk.Toplevel):
    def __init__(self, parent, user_story, predicted_domain, features):
        super().__init__(parent)
        self.title("Rate the Analysis")
        self.geometry("300x200")
        self.user_story = user_story
        self.predicted_domain = predicted_domain
        self.features = features

        tk.Label(self, text="How would you rate this result?").pack(pady=10)

        self.rating_var = tk.IntVar(value=0)
        for i in range(1, 6):
            tk.Radiobutton(self, text=str(i), variable=self.rating_var, value=i).pack()

        tk.Button(self, text="Submit", command=self.submit_rating).pack(pady=10)

    def submit_rating(self):
        rating = self.rating_var.get()
        if rating == 0:
            messagebox.showwarning("Warning", "Please select a rating before submitting.")
            return

        # Salva il rating in un file JSON (o invialo a un server)
        feedback = {
            "user_story": self.user_story,
            "predicted_domain": self.predicted_domain,
            "features": self.features,
            "rating": rating
        }

        with open("ratings.json", "a") as file:
            json.dump(feedback, file)
            file.write("\n")

        messagebox.showinfo("Success", "Thank you for your feedback!")
        self.destroy()
