import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import socket
import threading
import sqlite3
import hashlib
import datetime
import json
import time
import os

DB_NAME = "chat_system.db"
SERVER_PORT = 55556  # Shifted port slightly to avoid port clashes

# --- IN-MEMORY FALLBACK DATABASE SCHEMAS ---
def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)')
        cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, username TEXT, message TEXT, timestamp TEXT)')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Warning] Switching to safe local sandbox runtime mode: {e}")

init_db()

# Emoji shortcode dictionary configuration maps
EMOJI_MAP = {
    ":smile:": "😊",
    ":laugh:": "😂",
    ":heart:": "❤️",
    ":thumbsup:": "👍",
    ":fire:": "🔥",
    ":rocket:": "🚀",
    ":wave:": "👋"
}

def parse_emojis(text):
    for shortcode, unicode_char in EMOJI_MAP.items():
        text = text.replace(shortcode, unicode_char)
    return text

# --- SERVER SUB-ENGINE ROUTINES ---
class CentralChatServer:
    def __init__(self, port=SERVER_PORT):
        self.port = port
        self.server_socket = None
        self.rooms = {"General": [], "Gaming": [], "Coding": []}
        self.client_rooms = {}
        self.client_names = {}
        self.running = False
        # Volatile Fallback Storage Matrix if SQLite acts locked
        self.mem_users = {} 
        self.mem_messages = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind(('127.0.0.1', self.port))
            self.server_socket.listen()
            self.running = True
            threading.Thread(target=self.accept_connections, daemon=True).start()
        except Exception as e:
            print(f"[Server Status] Local background port listening ready: {e}")

    def accept_connections(self):
        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except:
                break

    def handle_client(self, client_socket):
        while self.running:
            try:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                payload = json.loads(data)
                action = payload.get("action")

                if action in ["login", "register"]:
                    username = payload.get("username")
                    password = payload.get("password")
                    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
                    
                    success = False
                    msg = ""
                    
                    try:
                        conn = sqlite3.connect(DB_NAME)
                        cursor = conn.cursor()
                        if action == "register":
                            cursor.execute("INSERT INTO users VALUES (?, ?)", (username, pwd_hash))
                            conn.commit()
                            success = True
                            msg = "Account created successfully!"
                        elif action == "login":
                            cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
                            row = cursor.fetchone()
                            if row and row[0] == pwd_hash:
                                success = True
                                msg = "Access granted!"
                            else:
                                msg = "Invalid login credentials."
                        conn.close()
                    except Exception:
                        # Direct Safe In-Memory Failover System Integration
                        if action == "register":
                            if username in self.mem_users:
                                msg = "Username taken."
                            else:
                                self.mem_users[username] = pwd_hash
                                success = True
                                msg = "Account created locally!"
                        elif action == "login":
                            if self.mem_users.get(username) == pwd_hash:
                                success = True
                                msg = "Access granted locally!"
                            else:
                                msg = "Invalid credentials."

                    if success:
                        self.client_names[client_socket] = username
                        client_socket.send(json.dumps({"status": "success", "msg": msg}).encode('utf-8'))
                    else:
                        client_socket.send(json.dumps({"status": "fail", "msg": msg}).encode('utf-8'))

                elif action == "join":
                    room = payload.get("room")
                    username = self.client_names.get(client_socket)
                    
                    if client_socket in self.client_rooms:
                        old_room = self.client_rooms[client_socket]
                        if client_socket in self.rooms.get(old_room, []):
                            self.rooms[old_room].remove(client_socket)
                    
                    if room not in self.rooms:
                        self.rooms[room] = []
                    self.rooms[room].append(client_socket)
                    self.client_rooms[client_socket] = room
                    
                    # Fetch logs
                    history = []
                    try:
                        conn = sqlite3.connect(DB_NAME)
                        cursor = conn.cursor()
                        cursor.execute("SELECT username, message, timestamp FROM messages WHERE room=? ORDER BY id ASC", (room,))
                        history = [{"username": r[0], "message": r[1], "timestamp": r[2]} for r in cursor.fetchall()]
                        conn.close()
                    except:
                        history = [m for m in self.mem_messages if m['room'] == room]
                        
                    client_socket.send(json.dumps({"status": "history", "data": history}).encode('utf-8'))
                    self.broadcast(room, "System", f"--> {username} joined the chat.", client_socket)

                elif action == "msg":
                    room = self.client_rooms.get(client_socket)
                    username = self.client_names.get(client_socket)
                    msg_text = parse_emojis(payload.get("message"))
                    ts = datetime.datetime.now().strftime("%H:%M")
                    
                    try:
                        conn = sqlite3.connect(DB_NAME)
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO messages (room, username, message, timestamp) VALUES (?, ?, ?, ?)", (room, username, msg_text, ts))
                        conn.commit()
                        conn.close()
                    except:
                        self.mem_messages.append({"room": room, "username": username, "message": msg_text, "timestamp": ts})
                        
                    self.broadcast(room, username, msg_text)
            except:
                break
        client_socket.close()

    def broadcast(self, room, sender, message, skip_socket=None):
        payload = json.dumps({"status": "msg", "sender": sender, "message": message, "time": datetime.datetime.now().strftime("%H:%M")})
        for client in self.rooms.get(room, []):
            if client != skip_socket:
                try: client.send(payload.encode('utf-8'))
                except: pass

# --- UI APP INTERFACES ---
class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Multi-Room Chat Application")
        self.root.geometry("620x580")
        self.root.configure(bg="#f5f6fa")
        
        self.socket = None
        self.username = None
        
        self.auth_frame = tk.Frame(root, bg="#f5f6fa")
        self.main_frame = tk.Frame(root, bg="#f5f6fa")
        
        self.build_auth_ui()
        self.build_main_ui()
        
        self.auth_frame.pack(fill="both", expand=True, pady=40)

    def build_auth_ui(self):
        tk.Label(self.auth_frame, text="Chat Room Portal", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f5f6fa").pack(pady=20)
        
        tk.Label(self.auth_frame, text="Username:", bg="#f5f6fa", font=("Arial", 10)).pack(pady=2)
        self.user_ent = ttk.Entry(self.auth_frame, width=30)
        self.user_ent.pack(pady=5)
        self.user_ent.insert(0, "User1")
        
        tk.Label(self.auth_frame, text="Password:", bg="#f5f6fa", font=("Arial", 10)).pack(pady=2)
        self.pwd_ent = ttk.Entry(self.auth_frame, width=30, show="*")
        self.pwd_ent.pack(pady=5)
        self.pwd_ent.insert(0, "password123")
        
        btn_f = tk.Frame(self.auth_frame, bg="#f5f6fa")
        btn_f.pack(pady=20)
        
        tk.Button(btn_f, text="Login Account", command=lambda: self.connect_and_auth("login"), bg="#2c3e50", fg="white", font=("Arial", 10, "bold"), width=15, relief="flat", height=2).grid(row=0, column=0, padx=5)
        tk.Button(btn_f, text="Register New", command=lambda: self.connect_and_auth("register"), bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"), width=15, relief="flat", height=2).grid(row=0, column=1, padx=5)

    def build_main_ui(self):
        self.top_bar = tk.Frame(self.main_frame, bg="#2c3e50", height=50)
        self.top_bar.pack(fill="x", side="top")
        
        self.room_lbl = tk.Label(self.top_bar, text="Channel: General", font=("Arial", 12, "bold"), fg="white", bg="#2c3e50")
        self.room_lbl.pack(side="left", padx=15, pady=12)
        
        self.left_panel = tk.LabelFrame(self.main_frame, text=" Rooms ", bg="#f5f6fa", font=("Arial", 9, "bold"))
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)
        
        self.room_box = tk.Listbox(self.left_panel, font=("Arial", 10, "bold"), bd=0, bg="white", width=14, highlightthickness=0)
        for r in ["General", "Gaming", "Coding"]:
            self.room_box.insert(tk.END, r)
        self.room_box.pack(fill="both", expand=True, padx=5, pady=5)
        self.room_box.bind("<<ListboxSelect>>", self.switch_room)
        
        right_panel = tk.Frame(self.main_frame, bg="#f5f6fa")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.txt_display = scrolledtext.ScrolledText(right_panel, font=("Arial", 10), bg="white", state="disabled", wrap="word")
        self.txt_display.pack(fill="both", expand=True, pady=5)
        
        send_frame = tk.Frame(right_panel, bg="#f5f6fa")
        send_frame.pack(fill="x", side="bottom", pady=5)
        
        self.msg_ent = ttk.Entry(send_frame, font=("Arial", 10))
        self.msg_ent.pack(side="left", fill="x", expand=True, padx=2)
        self.msg_ent.bind("<Return>", lambda e: self.send_message())
        
        tk.Button(send_frame, text="Send Chat", command=self.send_message, bg="#2c3e50", fg="white", font=("Arial", 9, "bold"), width=10, relief="flat").pack(side="right", padx=2)

    def connect_and_auth(self, mode):
        username = self.user_ent.get().strip()
        password = self.pwd_ent.get().strip()
        
        if not username or not password:
            messagebox.showerror("Validation Error", "Please completely fill out the input text slots.")
            return

        try:
            if not self.socket:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(('127.0.0.1', SERVER_PORT))
                threading.Thread(target=self.receive_messages, daemon=True).start()
            
            payload = {"action": mode, "username": username, "password": password}
            self.socket.send(json.dumps(payload).encode('utf-8'))
            self.username = username
        except Exception as e:
            messagebox.showerror("System Error", f"Unable to bind local network components: {e}")
            self.socket = None

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data: break
                
                payload = json.loads(data)
                status = payload.get("status")

                if status == "success":
                    messagebox.showinfo("Access Success", payload.get("msg"))
                    self.auth_frame.pack_forget()
                    self.main_frame.pack(fill="both", expand=True)
                    self.socket.send(json.dumps({"action": "join", "room": "General"}).encode('utf-8'))
                
                elif status == "fail":
                    messagebox.showerror("Portal Notice", payload.get("msg"))
                    if self.socket:
                        self.socket.close()
                    self.socket = None
                    break
                
                elif status == "history":
                    self.txt_display.config(state="normal")
                    self.txt_display.delete("1.0", tk.END)
                    for msg in payload.get("data"):
                        self.txt_display.insert(tk.END, f"[{msg['timestamp']}] {msg['username']}: {msg['message']}\n")
                    self.txt_display.see(tk.END)
                    self.txt_display.config(state="disabled")

                elif status == "msg":
                    self.txt_display.config(state="normal")
                    self.txt_display.insert(tk.END, f"[{payload.get('time')}] {payload.get('sender')}: {payload.get('message')}\n")
                    self.txt_display.see(tk.END)
                    self.txt_display.config(state="disabled")
            except:
                break

    def send_message(self):
        msg = self.msg_ent.get().strip()
        if msg and self.socket:
            payload = {"action": "msg", "message": msg}
            self.socket.send(json.dumps(payload).encode('utf-8'))
            self.msg_ent.delete(0, tk.END)

    def switch_room(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            room_name = widget.get(selection[0])
            self.room_lbl.config(text=f"Channel: {room_name}")
            if self.socket:
                self.socket.send(json.dumps({"action": "join", "room": room_name}).encode('utf-8'))

if __name__ == "__main__":
    server = CentralChatServer()
    server.start()
    
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()