import tkinter as tk
from PIL import Image, ImageTk
import os


def build_intro_page(root, frames, BASE_DIR, INTRO_FLAG_FILE, show_frame):

    intro = tk.Frame(root, bg="#0e0e0e")
    frames["intro"] = intro

  
    try:
        bg_img = Image.open(
            os.path.join(BASE_DIR, "images/intro_bg.png")
        ).resize((1600, 900), Image.Resampling.LANCZOS)

        bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = tk.Label(intro, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relwidth=1, relheight=1)

    except:
        pass

   
    intro_box = tk.Frame(
        intro,
        bg="#1c1c1c",
        bd=2,
        relief="ridge",
        padx=40,
        pady=35
    )
    intro_box.place(relx=0.5, rely=0.5, anchor="center")

   
    try:
        logo_img = Image.open(
            os.path.join(BASE_DIR, "images/logo.png")
        ).resize((140, 140), Image.Resampling.LANCZOS)

        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_lbl = tk.Label(intro_box, image=logo_photo, bg="#1c1c1c")
        logo_lbl.image = logo_photo
        logo_lbl.pack(pady=10)

    except:
        pass

    tk.Label(
        intro_box,
        text="WELCOME TO",
        fg="#cccccc",
        bg="#1c1c1c",
        font=("Arial", 18)
    ).pack(pady=5)

    tk.Label(
        intro_box,
        text="FITNESS DASHBOARD",
        fg="#00ff99",
        bg="#1c1c1c",
        font=("Arial", 28, "bold")
    ).pack(pady=10)

    tk.Label(
        intro_box,
        text="Track your macros, plan workouts,\nand reach your fitness goals.",
        fg="white",
        bg="#1c1c1c",
        font=("Arial", 12),
        justify="center"
    ).pack(pady=15)

    def start_app():
        with open(INTRO_FLAG_FILE, "w") as f:
            f.write("seen")

        show_frame("user_profile")

    tk.Button(
        intro_box,
        text="GET STARTED",
        bg="#00ff99",
        fg="black",
        font=("Arial", 13, "bold"),
        width=20,
        height=2,
        command=start_app
    ).pack(pady=20)

    return intro
