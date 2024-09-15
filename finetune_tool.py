import tkinter as tk
from tkinter import ttk, messagebox
import json

class DNASequenceDatasetCreatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("DNA Sequence Dataset Creator for Fine-tuning")
        self.master.geometry("800x700")

        self.data = []
        self.current_row = {"user": "", "chatbot": ""}

        self.create_widgets()

    def create_widgets(self):
        # User Input
        ttk.Label(self.master, text="User Input:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.user_text = tk.Text(self.master, height=15, width=90)
        self.user_text.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.user_text.insert(tk.END, """Based on the #query, generate a DNA sequence string using only the characters A, T, C, and G. Adhere to these biological principles:

Include common genetic motifs like start codons (ATG), and stop codons (TAA, TAG, TGA).
Ensure the sequence consists of complete codons (divisible by 3).
Mimic natural codon bias and GC content typical of the specified organism or gene type.

Base your sequence on the characteristics specified in the query. Consider the organism, gene type, or specific features requested. Adjust the sequence length, structure, and composition to match the requirements given.
Output only the raw DNA string without any additional text, formatting, or explanation. The sequence should precisely follow the specifications provided in the query that follows:

#query
""")

        # Chatbot Response
        ttk.Label(self.master, text="Chatbot Response:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.chatbot_text = tk.Text(self.master, height=10, width=90)
        self.chatbot_text.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

        # Add row button
        ttk.Button(self.master, text="Add Row", command=self.add_row).grid(row=4, column=0, columnspan=2, pady=10)

        # Save button
        ttk.Button(self.master, text="Save", command=self.save_data).grid(row=5, column=0, columnspan=2, pady=10)

        # Row count label
        self.row_count_var = tk.StringVar(value="Current row count: 0")
        ttk.Label(self.master, textvariable=self.row_count_var).grid(row=6, column=0, columnspan=2, pady=10)

    def add_row(self):
        user_input = self.user_text.get("1.0", tk.END).strip()
        chatbot_response = self.chatbot_text.get("1.0", tk.END).strip()
        
        if not user_input or not chatbot_response:
            messagebox.showwarning("Warning", "Both fields must be filled.")
            return

        self.current_row = {
            "user": user_input,
            "chatbot": chatbot_response
        }
        self.data.append(self.current_row)
        self.update_row_count()
        self.clear_chatbot_field()
        messagebox.showinfo("Success", "Row added successfully")

    def clear_chatbot_field(self):
        self.chatbot_text.delete("1.0", tk.END)

    def save_data(self):
        if not self.data:
            messagebox.showwarning("Warning", "No data to save.")
            return

        with open("dna_sequence_dataset.jsonl", "w") as f:
            for item in self.data:
                f.write(json.dumps(item) + "\n")
        
        messagebox.showinfo("Success", f"Data saved to dna_sequence_dataset.jsonl with {len(self.data)} rows.")

    def update_row_count(self):
        self.row_count_var.set(f"Current row count: {len(self.data)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DNASequenceDatasetCreatorGUI(root)
    root.mainloop()