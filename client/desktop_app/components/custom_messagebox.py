import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class CustomMessageBox:
    def __init__(self, parent, title, user_story, domain, results):

                # Verifica se results è vuoto
        if not results or all(len(features) == 0 for features in results.values()):
            message_output = f"""User Story: {user_story}\n
Story Domain: {domain}\n
No sensitive features have been found"""
            messagebox.showinfo(title=title, message=message_output)
            return  # Esci dal costruttore se non ci sono risultati
        
        
        # Creazione della finestra Toplevel
        self.window = tk.Toplevel(parent)
        self.window.title(title)

        # Crea un Frame per contenere le etichette
        info_frame = ttk.Frame(self.window)
        info_frame.pack(padx=10, pady=10, fill='x')

        # Aggiungi la User Story come etichetta
        us_label = ttk.Label(info_frame, text=f"User Story: {user_story}", wraplength=400)
        us_label.pack(pady=(10, 0), anchor="w")

        # Aggiungi il Story Domain come etichetta
        domain_label = ttk.Label(info_frame, text=f"Story Domain: {domain}", wraplength=400)
        domain_label.pack(pady=(0, 10), anchor="w")

        # Aggiungi la label per le "Sensitive Features Found"
        label = ttk.Label(self.window, text="Sensitive Features Found", font=("Arial", 14))
        label.pack(pady=10)

        # Creazione della Treeview
        self.tree = ttk.Treeview(self.window, columns=("task", "sensitive_features"), show='headings', height=10)
        self.tree.heading("task", text="Task")
        self.tree.heading("sensitive_features", text="Sensitive Features")
        self.tree.column("task", anchor=tk.CENTER, width=150)
        self.tree.column("sensitive_features", anchor=tk.CENTER, width=300)

        for task, features in results.items():
            # Le features vengono concatenate in una singola stringa separata da virgole
            features_str = ", ".join(features)
            self.tree.insert("", tk.END, values=(task, features_str))

        self.tree.pack(pady=10, fill='x')

        # Bottone di chiusura
        close_button = ttk.Button(self.window, text="Close", command=self.window.destroy)
        close_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Bottone di download
        download_button = ttk.Button(self.window, text="Download", command=lambda: self.download_results(user_story, domain, results))
        download_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Centra il custom messagebox sullo schermo
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

        self.window.grab_set()

    def download_results(self, user_story, domain, results):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json"),
                                                            ("All files", "*.*")])
        if file_path:
            # Organizza i dati per seguire la struttura richiesta
            data = {
                "story": user_story,  # Cambia 'user_story' in 'story'
                "domain": domain,  # Cambia 'story_domain' in 'domain'
                "tasks": list(results.keys()),  # Aggiungi i task come lista
                "features": results  # Cambia 'sensitive_features' in 'features'
            }

            # Salva i dati nel file JSON
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            messagebox.showinfo("Success", "Results have been downloaded successfully!")