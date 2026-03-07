import tkinter as tk
from tkinter import ttk, messagebox


def build_user_page(root, frames, show_frame, BASE_DIR, user_profile, users, save_users):

    frame = tk.Frame(root, bg="#0e0e0e")
    frames["user_profile"] = frame

    edit_mode = {"active": False}
    current_email = {"value": None}
    register_open = {"active": False}

    # ---------------- BUTTON PRESS EFFECT ----------------
    def add_press_effect(btn, normal, pressed):

        def press(e):
            btn.config(bg=pressed)

        def release(e):
            btn.config(bg=normal)

        btn.bind("<ButtonPress-1>", press)
        btn.bind("<ButtonRelease-1>", release)

    # ---------------- STYLE ----------------
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Neon.TButton",
        font=("Segoe UI", 13, "bold"),
        padding=10,
        background="#00ff99",
        foreground="black"
    )

    style.map(
        "Neon.TButton",
        background=[("active", "#00cc77")]
    )

    # ---------------- BACK BUTTON ----------------
    def back_action():

        if register_open["active"]:
            register_frame.pack_forget()
            login_frame.pack()
            title_lbl.config(text="USER PROFILE")
            register_open["active"] = False
            return

        if user_profile:
            show_frame("landing")
        else:
            show_frame("intro")

    back_btn = tk.Button(
        frame,
        text="← BACK",
        bg="#0e0e0e",
        fg="#00ff99",
        font=("Segoe UI", 13, "bold"),
        bd=0,
        activebackground="#0e0e0e",
        activeforeground="#00ff99",
        command=back_action
    )

    back_btn.place(x=20, y=20)
    add_press_effect(back_btn, "#0e0e0e", "#1a1a1a")

    # ================= MAIN DESIGN CONTAINER =================

    outer_container = tk.Frame(
        frame,
        bg="#00ff99",   # neon border color
        bd=0
    )

    outer_container.place(relx=0.5, rely=0.5, anchor="center")

    # inner container (actual panel)
    panel = tk.Frame(
        outer_container,
        bg="#141414",
        padx=60,
        pady=45
    )

    panel.pack(padx=2, pady=2)

    # ---------------- TITLE ----------------
    title_lbl = tk.Label(
        panel,
        text="USER PROFILE",
        font=("Segoe UI", 32, "bold"),
        fg="#00ff99",
        bg="#141414"
    )
    title_lbl.pack(pady=20)

    # ---------------- LOGIN FRAME ----------------
    login_frame = tk.Frame(panel, bg="#141414")
    login_frame.pack()

    email_var = tk.StringVar()
    password_var = tk.StringVar()

    entry_style = {
        "font": ("Segoe UI", 14),
        "bg": "#1f1f1f",
        "fg": "white",
        "insertbackground": "white",
        "bd": 0,
        "width": 22
    }

    label_style = {
        "fg": "white",
        "bg": "#141414",
        "font": ("Segoe UI", 15)
    }

    tk.Label(login_frame, text="Email", **label_style).grid(row=0, column=0, pady=8, sticky="e")
    tk.Entry(login_frame, textvariable=email_var, **entry_style).grid(row=0, column=1, pady=8, padx=10)

    tk.Label(login_frame, text="Password", **label_style).grid(row=1, column=0, pady=8, sticky="e")
    tk.Entry(login_frame, textvariable=password_var, show="*", **entry_style).grid(row=1, column=1, pady=8, padx=10)

    # ---------------- LOGIN FUNCTION ----------------
    def login_user():

        mail = email_var.get().strip().lower()
        pwd = password_var.get().strip()

        if mail in users and users[mail]["password"] == pwd:

            user_profile.clear()
            user_profile.update(users[mail]["profile"])

            current_email["value"] = mail

            email_var.set("")
            password_var.set("")

            show_frame("landing")

        else:
            messagebox.showerror("Error", "Invalid email or password.")

    # ---------------- OPEN REGISTER ----------------
    def open_register():

        edit_mode["active"] = False
        register_open["active"] = True

        login_frame.pack_forget()
        register_frame.pack()

        title_lbl.config(text="REGISTER")

    login_btn = ttk.Button(
        login_frame,
        text="Login",
        style="Neon.TButton",
        command=login_user
    )

    login_btn.grid(row=2, column=0, pady=20)

    register_btn = ttk.Button(
        login_frame,
        text="Register",
        style="Neon.TButton",
        command=open_register
    )

    register_btn.grid(row=2, column=1)

    # ---------------- REGISTER FRAME ----------------
    register_frame = tk.Frame(panel, bg="#141414")

    name_var = tk.StringVar()
    age_var = tk.StringVar()
    gender_var = tk.StringVar()
    height_var = tk.StringVar()
    weight_var = tk.StringVar()
    body_var = tk.StringVar()
    goal_var = tk.StringVar()

    fields = [
        ("Name", name_var),
        ("Age", age_var),
        ("Gender", gender_var),
        ("Height (cm)", height_var),
        ("Weight (kg)", weight_var),
        ("Body Type", body_var),
        ("Goal", goal_var),
    ]

    for i, (label, var) in enumerate(fields):

        tk.Label(register_frame, text=label, **label_style).grid(
            row=i, column=0, pady=8, sticky="e"
        )

        tk.Entry(register_frame, textvariable=var, **entry_style).grid(
            row=i, column=1, pady=8, padx=10
        )

    # ---------------- SAVE PROFILE ----------------
    def save_profile():

        data = {
            "name": name_var.get(),
            "age": age_var.get(),
            "gender": gender_var.get(),
            "height": height_var.get(),
            "weight": weight_var.get(),
            "body_type": body_var.get(),
            "goal": goal_var.get(),
        }

        if not all(data.values()):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            data["age"] = int(data["age"])
            data["height"] = float(data["height"])
            data["weight"] = float(data["weight"])
        except:
            messagebox.showerror("Error", "Invalid numeric values.")
            return

        if edit_mode["active"]:

            users[current_email["value"]]["profile"] = data
            save_users()

            user_profile.clear()
            user_profile.update(data)

            messagebox.showinfo("Updated", "Profile updated!")

            edit_mode["active"] = False
            register_open["active"] = False

            register_frame.pack_forget()
            login_frame.pack()

            title_lbl.config(text="USER PROFILE")

            show_frame("landing")
            return

        mail = email_var.get().strip().lower()
        pwd = password_var.get().strip()

        if not mail or not pwd:
            messagebox.showerror("Error", "Email and password required.")
            return

        users[mail] = {"password": pwd, "profile": data}

        save_users()

        messagebox.showinfo("Success", "Account created! Please login.")

        register_open["active"] = False

        register_frame.pack_forget()
        login_frame.pack()

        title_lbl.config(text="USER PROFILE")

    save_btn = ttk.Button(
        register_frame,
        text="Save",
        style="Neon.TButton",
        command=save_profile
    )

    save_btn.grid(row=8, column=0, columnspan=2, pady=25)

    # ---------------- EDIT FUNCTION ----------------
    def open_edit_mode():

        if not user_profile:
            return

        edit_mode["active"] = True
        register_open["active"] = True

        login_frame.pack_forget()
        register_frame.pack()

        title_lbl.config(text="EDIT PROFILE")

        profile = user_profile

        name_var.set(profile.get("name", ""))
        age_var.set(profile.get("age", ""))
        gender_var.set(profile.get("gender", ""))
        height_var.set(profile.get("height", ""))
        weight_var.set(profile.get("weight", ""))
        body_var.set(profile.get("body_type", ""))
        goal_var.set(profile.get("goal", ""))

    frame.open_edit_mode = open_edit_mode

    return frame, open_edit_mode