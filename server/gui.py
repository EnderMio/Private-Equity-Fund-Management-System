import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"  # 后端API的基础URL

def create_main_window(root):
    root.resizable(True, True)  # 允许主窗口调整大小
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, expand=True, fill='both')

    label = tk.Label(frame, text="Welcome to the Tkinter App")
    label.pack(pady=5)

    choice_label = tk.Label(frame, text="Choose an option:")
    choice_label.pack(pady=5)

    login_button = tk.Button(frame, text="Login", command=lambda: switch_to_login(root))
    login_button.pack(pady=5)

    register_button = tk.Button(frame, text="Register", command=lambda: switch_to_register(root))
    register_button.pack(pady=5)

    exit_button = tk.Button(frame, text="Exit", command=root.quit)
    exit_button.pack(pady=5)

    # 初始化内容窗口
    root.content_frame = tk.Frame(root)
    root.content_frame.pack(padx=10, pady=10, expand=True, fill='both')

def clear_content_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def switch_to_login(root):
    clear_content_frame(root.content_frame)

    login_win = root.content_frame
    login_win.title = "Login"

    tk.Label(login_win, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_win)
    username_entry.pack(pady=5)

    tk.Label(login_win, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_win, text="Login", command=lambda: handle_login(username_entry.get(), password_entry.get())).pack(pady=5)

def switch_to_register(root):
    clear_content_frame(root.content_frame)

    register_win = root.content_frame
    register_win.title = "Register"

    tk.Label(register_win, text="Username").pack(pady=5)
    username_entry = tk.Entry(register_win)
    username_entry.pack(pady=5)

    tk.Label(register_win, text="Password").pack(pady=5)
    password_entry = tk.Entry(register_win, show="*")
    password_entry.pack(pady=5)

    tk.Button(register_win, text="Register", command=lambda: handle_register(username_entry.get(), password_entry.get())).pack(pady=5)

def handle_login(username, password):
    url = f"{BASE_URL}/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Invalid credentials!")

def handle_register(username, password):
    url = f"{BASE_URL}/register"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    
    print(response.content)
    if response.status_code == 201:
        messagebox.showinfo("Register", "User registered successfully!")
    else:
        messagebox.showerror("Register", "Registration failed!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("My Tkinter App")
    create_main_window(root)
    root.mainloop()  # 启动Tkinter主循环
