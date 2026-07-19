import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime
import matplotlib.pyplot as plt

# --- DATABASE SETUP & ERROR HANDLING ---
DB_NAME = "bmi_records.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

init_db()

# --- BMI LOGIC & UTILITIES ---
def get_category_and_color(bmi):
    if bmi < 18.5:
        return "Underweight", "#3498db"  # Light Blue
    elif 18.5 <= bmi <= 24.9:
        return "Normal", "#2ecc71"       # Safe Green
    elif 25 <= bmi <= 29.9:
        return "Overweight", "#f39c12"   # Warning Orange
    else:
        return "Obese", "#e74c3c"        # Alert Red

# --- CORE APP CONTROLLER ---
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Analytics Suite")
        self.root.geometry("450x550")
        self.root.configure(bg="#f5f6fa")
        
        # UI Styling Elements
        style = ttk.Style()
        style.theme_use("clam")
        
        # App Header
        header = tk.Label(root, text="BMI Health Tracker", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f5f6fa")
        header.pack(pady=15)
        
        # User Configuration Frame
        user_frame = tk.LabelFrame(root, text=" User Account Profiles ", bg="#f5f6fa", font=("Arial", 10, "bold"))
        user_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(user_frame, text="Username:", bg="#f5f6fa", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.user_entry = ttk.Entry(user_frame, width=25)
        self.user_entry.insert(0, "Adwaidh")  # Pre-fill for ease of use
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Calculation Metrics Frame
        metrics_frame = tk.LabelFrame(root, text=" Biometric Metrics Input ", bg="#f5f6fa", font=("Arial", 10, "bold"))
        metrics_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(metrics_frame, text="Weight (kg):", bg="#f5f6fa", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.weight_entry = ttk.Entry(metrics_frame, width=20)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(metrics_frame, text="Height (meters):", bg="#f5f6fa", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.height_entry = ttk.Entry(metrics_frame, width=20)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Operational Buttons
        btn_frame = tk.Frame(root, bg="#f5f6fa")
        btn_frame.pack(pady=15)
        
        self.calc_btn = tk.Button(btn_frame, text="Calculate & Save", command=self.calculate_bmi, bg="#2c3e50", fg="white", font=("Arial", 11, "bold"), width=18, relief="flat")
        self.calc_btn.grid(row=0, column=0, padx=5)
        
        self.graph_btn = tk.Button(btn_frame, text="View Trends", command=self.show_trends, bg="#7f8c8d", fg="white", font=("Arial", 11, "bold"), width=15, relief="flat")
        self.graph_btn.grid(row=0, column=1, padx=5)
        
        # Results Readout Panel
        self.result_card = tk.Frame(root, bg="white", bd=1, relief="solid")
        self.result_card.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.bmi_lbl = tk.Label(self.result_card, text="BMI: --", font=("Arial", 22, "bold"), bg="white", fg="#7f8c8d")
        self.bmi_lbl.pack(pady=10)
        
        self.cat_lbl = tk.Label(self.result_card, text="Category: Waiting for Input", font=("Arial", 12, "bold"), bg="white", fg="#7f8c8d")
        self.cat_lbl.pack(pady=5)

    # --- ADVANCED CALCULATION ENGINE ---
    def calculate_bmi(self):
        username = self.user_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        height_str = self.height_entry.get().strip()
        
        # Strict Multi-level Input Validation
        if not username:
            messagebox.showerror("Validation Error", "Please provide a valid Profile Username.")
            return
            
        try:
            weight = float(weight_str)
            height = float(height_str)
            
            if weight <= 0 or height <= 0:
                raise ValueError("Metrics values must strictly be positive numbers.")
                
            # SMART CONVERSION: If user types centimeters (e.g., 170 instead of 1.7)
            if height > 3.0:
                height = height / 100.0  # Convert cm to meters automatically
                
        except ValueError:
            messagebox.showerror("Input Validation Failure", "Please check your values. Weight and Height must be positive numeric figures.")
            return
            
        # Core Formula Computation
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)
        category, color = get_category_and_color(bmi)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Push To Local Storage With Error Handling Catch
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO records (username, weight, height, bmi, category, date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, weight, height, bmi, category, current_date))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Save Failure", f"Could not preserve log entry: {e}")
            return
            
        # Dynamically Update UI Visuals Natively
        self.bmi_lbl.config(text=f"BMI: {bmi}", fg=color)
        self.cat_lbl.config(text=f"Category: {category}", fg=color)
        self.result_card.config(highlightbackground=color, highlightcolor=color, bd=2)
        
        # Quick informational success pop
        messagebox.showinfo("Success", f"Data entry logged safely for user profile: '{username}'!")
    # --- VISUAL TREND GENERATION FRAMEWORK ---
    def show_trends(self):
        username = self.user_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Enter a user profile identity name to query track metrics.")
            return
            
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT date, bmi FROM records 
                WHERE username = ? 
                ORDER BY datetime(date) ASC
            ''', (username,))
            data = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Extraction Failure", f"Could not load tracking timelines: {e}")
            return
            
        if len(data) < 1:
            messagebox.showwarning("Empty Log Context", f"No records detected under profile '{username}' yet. Calculate a couple records first!")
            return
            
        # Separate timestamps and values for plot mapping
        dates = [row[0] for row in data]
        bmis = [row[1] for row in data]
        
        # Generate the Matplotlib Visualization Window
        plt.figure(figsize=(8, 4.5))
        plt.plot(dates, bmis, marker='o', color='#2c3e50', linewidth=2, label="Calculated BMI Trend")
        
        # Color Zone Highlights for Interactive Evaluation Reference
        plt.axhspan(0, 18.5, color='#3498db', alpha=0.15, label="Underweight (<18.5)")
        plt.axhspan(18.5, 24.9, color='#2ecc71', alpha=0.15, label="Normal Zone (18.5-24.9)")
        plt.axhspan(24.9, 29.9, color='#f39c12', alpha=0.15, label="Overweight Zone (25-29.9)")
        plt.axhspan(29.9, 50, color='#e74c3c', alpha=0.15, label="Obese Zone (≥30)")
        
        plt.title(f"Biometric Progression Roadmap — User: {username}", fontsize=12, fontweight='bold', pad=15)
        plt.xlabel("Recording Timestamp Sequence", fontsize=10)
        plt.ylabel("Body Mass Index Score Values", fontsize=10)
        plt.xticks(rotation=20, ha='right')
        plt.ylim(min(bmis) - 3, max(bmis) + 3)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()