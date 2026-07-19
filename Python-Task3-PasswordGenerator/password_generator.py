import tkinter as tk
from tkinter import messagebox, ttk
import secrets
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Architect")
        self.root.geometry("480x620")
        self.root.configure(bg="#f8f9fa")
        
        # Session Memory: Holds last 5 passwords (not saved to disk for security)
        self.history = []
        
        # --- UI LAYOUT & STYLING ---
        header = tk.Label(root, text="Password Generator", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f8f9fa")
        header.pack(pady=15)
        
        # 1. Length Control Frame
        length_frame = tk.LabelFrame(root, text=" Password Length ", bg="#f8f9fa", font=("Arial", 10, "bold"))
        length_frame.pack(fill="x", padx=20, pady=5)
        
        self.length_var = tk.IntVar(value=12)
        self.length_slider = tk.Scale(length_frame, from_=8, to=64, orient="horizontal", variable=self.length_var, bg="#f8f9fa", bd=0, highlightbackground="#f8f9fa", font=("Arial", 10))
        self.length_slider.pack(fill="x", padx=15, pady=5)
        
        # 2. Parameters Configuration Frame
        opts_frame = tk.LabelFrame(root, text=" Character Set Parameters ", bg="#f8f9fa", font=("Arial", 10, "bold"))
        opts_frame.pack(fill="x", padx=20, pady=5)
        
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)
        self.exclude_ambig_var = tk.BooleanVar(value=False)
        
        tk.Checkbutton(opts_frame, text="Uppercase Letters (A-Z)", variable=self.upper_var, bg="#f8f9fa", font=("Arial", 10), anchor="w").pack(fill="x", padx=15, pady=2)
        tk.Checkbutton(opts_frame, text="Lowercase Letters (a-z)", variable=self.lower_var, bg="#f8f9fa", font=("Arial", 10), anchor="w").pack(fill="x", padx=15, pady=2)
        tk.Checkbutton(opts_frame, text="Numerical Digits (0-9)", variable=self.digits_var, bg="#f8f9fa", font=("Arial", 10), anchor="w").pack(fill="x", padx=15, pady=2)
        tk.Checkbutton(opts_frame, text="Special Symbols (!@#$...)", variable=self.symbols_var, bg="#f8f9fa", font=("Arial", 10), anchor="w").pack(fill="x", padx=15, pady=2)
        
        # Separator line
        ttk.Separator(opts_frame, orient='horizontal').pack(fill='x', padx=15, pady=5)
        
        tk.Checkbutton(opts_frame, text="Exclude Ambiguous Characters (e.g., 0, O, l, 1)", variable=self.exclude_ambig_var, bg="#f8f9fa", font=("Arial", 9, "italic"), fg="#7f8c8d", anchor="w").pack(fill="x", padx=15, pady=2)
        
        # 3. Execution Action Button
        self.gen_btn = tk.Button(root, text="Generate & Copy", command=self.generate_password, bg="#2c3e50", fg="white", font=("Arial", 11, "bold"), relief="flat", height=2)
        self.gen_btn.pack(fill="x", padx=20, pady=15)
        
        # 4. Interactive Display Dashboard
        self.result_card = tk.Frame(root, bg="white", bd=1, relief="solid")
        self.result_card.pack(fill="x", padx=20, pady=5)
        
        self.pwd_display = tk.Entry(self.result_card, font=("Consolas", 14, "bold"), bd=0, bg="white", justify="center", fg="#2c3e50")
        self.pwd_display.pack(fill="x", padx=10, pady=10)
        
        # Real-time Metrics Layer
        metrics_bar = tk.Frame(self.result_card, bg="white")
        metrics_bar.pack(fill="x", padx=10, pady=5)
        
        self.strength_lbl = tk.Label(metrics_bar, text="STRENGTH: NONE", font=("Arial", 9, "bold"), bg="white", fg="#7f8c8d")
        self.strength_lbl.pack(side="left")
        
        self.strength_bar = ttk.Progressbar(metrics_bar, orient="horizontal", length=200, mode="determinate")
        self.strength_bar.pack(side="right", pady=2)
        
        # 5. Volatile Session History Pane
        history_frame = tk.LabelFrame(root, text=" Volatile Session History (Last 5 Logs) ", bg="#f8f9fa", font=("Arial", 10, "bold"))
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.history_box = tk.Listbox(history_frame, font=("Consolas", 10), bg="#ffffff", bd=0, highlightthickness=0)
        self.history_box.pack(fill="both", expand=True, padx=10, pady=5)

    # --- ENHANCED CRYPTOGRAPHIC COMPUTATION ENGINE ---
    def generate_password(self):
        length = self.length_var.get()
        
        # Collect chosen configurations
        pools = []
        guaranteed_chars = []
        
        # Define base character libraries
        upper_pool = string.ascii_uppercase
        lower_pool = string.ascii_lowercase
        digits_pool = string.digits
        symbols_pool = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Enforce rule: Exclude ambiguous characters if user flagged checkbox
        if self.exclude_ambig_var.get():
            ambiguous = "0O1lI|"
            upper_pool = "".join(c for c in upper_pool if c not in ambiguous)
            lower_pool = "".join(c for c in lower_pool if c not in ambiguous)
            digits_pool = "".join(c for c in digits_pool if c not in ambiguous)
            symbols_pool = "".join(c for c in symbols_pool if c not in ambiguous)
            
        # Compile dynamic pool combinations
        if self.upper_var.get():
            pools.append(upper_pool)
            guaranteed_chars.append(secrets.choice(upper_pool))
        if self.lower_var.get():
            pools.append(lower_pool)
            guaranteed_chars.append(secrets.choice(lower_pool))
        if self.digits_var.get():
            pools.append(digits_pool)
            guaranteed_chars.append(secrets.choice(digits_pool))
        if self.symbols_var.get():
            pools.append(symbols_pool)
            guaranteed_chars.append(secrets.choice(symbols_pool))
            
        # Validation Checkpoint: Must pick at least 2 pools to protect baseline diversity
        if len(pools) < 2:
            messagebox.showerror("Configuration Guard", "Security Threshold Broken! You must select at least 2 active character sets.")
            return
            
        # Master assembly pool
        full_pool = "".join(pools)
        
        # Fill remaining slots with secure random choices
        remaining_length = length - len(guaranteed_chars)
        random_fill = [secrets.choice(full_pool) for _ in range(remaining_length)]
        
        # Combine and securely shuffle the composition string
        final_password_list = guaranteed_chars + random_fill
        secrets.SystemRandom().shuffle(final_password_list)
        final_password = "".join(final_password_list)
        
        # Display password out to UI panel and force dispatch to system clipboard
        self.pwd_display.delete(0, tk.END)
        self.pwd_display.insert(0, final_password)
        pyperclip.copy(final_password)
        
        # Evaluate entropy tier
        self.evaluate_strength(final_password, len(pools))
        
        # Append trace directly onto cache tracking ring
        self.update_history_log(final_password)

    def evaluate_strength(self, pwd, active_pools_count):
        length = len(pwd)
        
        # Metric scoring algorithm
        if length < 10 or active_pools_count < 3:
            self.strength_lbl.config(text="STRENGTH: WEAK", fg="#e74c3c")
            self.strength_bar['value'] = 25
            self.result_card.config(highlightbackground="#e74c3c", highlightcolor="#e74c3c", bd=2)
        elif 10 <= length <= 14 and active_pools_count >= 3:
            self.strength_lbl.config(text="STRENGTH: MEDIUM", fg="#f39c12")
            self.strength_bar['value'] = 60
            self.result_card.config(highlightbackground="#f39c12", highlightcolor="#f39c12", bd=2)
        else: # Length > 14 and solid character coverage
            self.strength_lbl.config(text="STRENGTH: STRONG", fg="#2ecc71")
            self.strength_bar['value'] = 100
            self.result_card.config(highlightbackground="#2ecc71", highlightcolor="#2ecc71", bd=2)

    def update_history_log(self, new_pwd):
        # Insert current password token onto index 0
        self.history.insert(0, new_pwd)
        if len(self.history) > 5:
            self.history.pop() # Evict oldest historical row entry
            
        # Sync visualization panel box list
        self.history_box.delete(0, tk.END)
        for idx, item in enumerate(self.history, start=1):
            self.history_box.insert(tk.END, f" #{idx}  {item}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()