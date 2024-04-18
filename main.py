import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

def carica_domande():
    try:
        with open('memory.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salva_domande(domande):
    with open('memory.json', 'w', encoding='utf-8') as f:
        json.dump(domande, f, ensure_ascii=False, indent=4)

class EconomicsQuizGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Economics Quiz")
        self.domande = carica_domande()
        self.question_ids = list(self.domande.keys())
        self.question_index = 0
        self.display_question()

    def display_question(self):
        if self.question_index < len(self.question_ids):
            question_id = self.question_ids[self.question_index]
            question_data = self.domande[question_id]
            lbl_question = tk.Label(self.master, text=question_data["question"], wraplength=400)
            lbl_question.pack(pady=(10, 20))
            for option in question_data["options"]:
                btn_option = tk.Button(self.master, text=option, command=lambda opt=option: self.check_answer(opt, question_id), width=50)
                btn_option.pack(pady=5)
        else:
            messagebox.showinfo("Quiz Finished", "Quiz completato!")
            self.master.destroy()

    def check_answer(self, selected_option, question_id):
        question_data = self.domande[question_id]
        if selected_option == question_data["correct_answer"]:
            self.domande[question_id]["correct_count"] += 1
            messagebox.showinfo("Risposta", "Corretta!")
        else:
            self.domande[question_id]["incorrect_count"] += 1
            if messagebox.askyesno("Risposta Sbagliata", "Vuoi vedere la risposta corretta?"):
                messagebox.showinfo("Risposta Corretta", "La risposta corretta era: " + question_data["correct_answer"])
        self.domande[question_id]["last_shown"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.question_index += 1
        self.refresh_quiz()

    def refresh_quiz(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        if self.question_index < len(self.question_ids):
            self.display_question()
        else:
            salva_domande(self.domande)

def main():
    root = tk.Tk()
    root.geometry("500x350")
    app = EconomicsQuizGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
