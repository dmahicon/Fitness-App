import tkinter as tk 
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import date, timedelta
from intro_page import build_intro_page
from user_page import build_user_page
from landing_page import build_landing_page
from macro_page import build_macro_page
from workout_page import build_workout_page
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTRO_FLAG_FILE = os.path.join(BASE_DIR, "intro_seen.txt")
USERS_FILE = os.path.join(BASE_DIR, "users.json")
users = {}

# ---------------- USER SAVE / LOAD ----------------
def load_users():
    global users
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
        except:
            users = {}
    else:
        users = {}

def save_users():
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        messagebox.showerror("Save Error", str(e))
   
load_users()
# ---------------- UI SETUP ----------------
root = tk.Tk()
root.title("Fitness Dashboard")
root.state("zoomed")
root.configure(bg="#0e0e0e")
root.attributes("-alpha", 0.0)


frames = {}
images = {}
user_profile = {}
name_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
height_var = tk.StringVar()
weight_var = tk.StringVar()
body_var = tk.StringVar()
goal_var = tk.StringVar()
email_var = tk.StringVar()
password_var = tk.StringVar()
labels_user = [
    "Email",
    "Password",
    "Name",
    "Age",
    "Gender",
    "Height (cm)",
    "Weight (kg)",
    "Body Type",
    "Goal"
]

vars_user = [
    email_var,
    password_var,
    name_var,
    age_var,
    gender_var,
    height_var,
    weight_var,
    body_var,
    goal_var
]
# ---------------- UPDATE LANDING DASHBOARD ----------------
def update_landing_dashboard():

    if "landing" in frames:

        landing = frames["landing"]

        if hasattr(landing, "update_meal_display"):
            landing.update_meal_display()

        if hasattr(landing, "update_workout_display"):
            landing.update_workout_display()
# ---------------- DATA ----------------
foods = {
    "Chicken": {"p": 31, "c": 0, "f": 3, "cal": 165, "vitA": 5, "vitC": 0, "ca": 15, "fe": 1.3, "vitD": 0, "img": "images/chicken.png", "cat": "Protein"},
    "Rice": {"p": 2, "c": 28, "f": 0, "cal": 130, "vitA": 0, "vitC": 0, "ca": 10, "fe": 0.2, "vitD": 0, "img": "images/rice.png", "cat": "Carbs"},
    "Egg": {"p": 13, "c": 1, "f": 11, "cal": 155, "vitA": 140, "vitC": 0, "ca": 50, "fe": 1.2, "vitD": 1, "img": "images/eggs.png", "cat": "Protein"},
    "Oats": {"p": 17, "c": 66, "f": 7, "cal": 389, "vitA": 0, "vitC": 0, "ca": 50, "fe": 4.7, "vitD": 0, "img": "images/oats.png", "cat": "Carbs"},
    "Banana": {"p": 1, "c": 23, "f": 0, "cal": 96, "vitA": 64, "vitC": 10, "ca": 5, "fe": 0.3, "vitD": 0, "img": "images/banana.png", "cat": "Fruits"},
    "Apple": {"p": 0, "c": 14, "f": 0, "cal": 52, "vitA": 54, "vitC": 4.6, "ca": 6, "fe": 0.1, "vitD": 0, "img": "images/apple.png", "cat": "Fruits"},
    "Milk": {"p": 3, "c": 5, "f": 3, "cal": 60, "vitA": 150, "vitC": 0, "ca": 120, "fe": 0, "vitD": 2, "img": "images/milk.png", "cat": "Dairy"},
    "Peanut Butter": {"p": 25, "c": 20, "f": 50, "cal": 588, "vitA": 0, "vitC": 0, "ca": 45, "fe": 1.9, "vitD": 0, "img": "images/pb.png", "cat": "Fats"},
    "Salmon": {"p": 20, "c": 0, "f": 13, "cal": 208, "vitA": 50, "vitC": 0, "ca": 15, "fe": 0.5, "vitD": 10, "img": "images/salmon.png", "cat": "Protein"},
    "Broccoli": {"p": 3, "c": 7, "f": 0, "cal": 34, "vitA": 623, "vitC": 89, "ca": 47, "fe": 0.7, "vitD": 0, "img": "images/broccoli.png", "cat": "Vegetables"},
    "Almonds": {"p": 21, "c": 22, "f": 50, "cal": 579, "vitA": 1, "vitC": 0, "ca": 269, "fe": 3.7, "vitD": 0, "img": "images/almonds.png", "cat": "Fats"},
    "Spinach": {"p": 3, "c": 4, "f": 0, "cal": 23, "vitA": 469, "vitC": 28, "ca": 99, "fe": 2.7, "vitD": 0, "img": "images/spinach.png", "cat": "Vegetables"},
}

# ---------------- WORKOUT SPLITS AND EXERCISES ----------------
workout_splits = {
    "PPL": {
        "description": "Push-Pull-Legs (3 days). Focus: Strength & Hypertrophy. ~60-75 min per session.",
        "days": ["Push", "Pull", "Legs"]
    },
    "Upper/Lower": {
        "description": "Upper-Lower split (4 days). Focus: Full body balance. ~60 min per session.",
        "days": ["Upper", "Lower"]
    },
    "Whole Body": {
        "description": "Full body workouts (3 days). Focus: Strength & conditioning. ~60-70 min per session.",
        "days": ["Full Body"]
    },
    "Upper/Lower x PPL": {
        "description": "Combination of Upper/Lower + PPL for 6 days. Focus: Intensity & volume. ~60-90 min per session.",
        "days": ["Upper", "Lower", "Push", "Pull", "Legs"]
    },
    "Bro Split": {
        "description": "Bro split (5 days). Focus: Muscle isolation. ~60 min per session.",
        "days": ["Chest", "Back", "Shoulders", "Arms", "Legs"]
    },
    "Arnold Split": {
        "description": "Arnold split (6 days). Focus: Advanced hypertrophy. ~70-90 min per session.",
        "days": ["Chest & Back", "Shoulders & Arms", "Legs", "Chest & Back", "Shoulders & Arms", "Legs"]
    },
    "PPL x Arnold Split": {
        "description": "Hybrid of PPL and Arnold split (6 days). Focus: Strength + Hypertrophy. ~70-90 min per session.",
        "days": ["Push", "Pull", "Legs", "Push", "Pull", "Legs"]
    }
}

exercises = {
    "Push": [
        {"name": "Bench Press", "sets": 4, "reps": 10, "rest": "90s", "calories": 50},
        {"name": "Shoulder Press", "sets": 3, "reps": 12, "rest": "90s", "calories": 40}
    ],
    "Pull": [
        {"name": "Deadlift", "sets": 3, "reps": 6, "rest": "120s", "calories": 80},
        {"name": "Pull Ups", "sets": 4, "reps": 10, "rest": "90s", "calories": 50},
        {"name": "Barbell Rows", "sets": 3, "reps": 12, "rest": "90s", "calories": 45},
        {"name": "Face Pulls", "sets": 3, "reps": 15, "rest": "60s", "calories": 20}
    ],
    "Legs": [
        {"name": "Squat", "sets": 4, "reps": 8, "rest": "120s", "calories": 70},
        {"name": "Leg Press", "sets": 3, "reps": 12, "rest": "90s", "calories": 50}
    ],
    "Back": [
        {"name": "Pull Ups", "sets": 4, "reps": 8, "rest": "90s", "calories": 50},
        {"name": "Deadlift", "sets": 3, "reps": 6, "rest": "120s", "calories": 80},
        {"name": "Barbell Rows", "sets": 3, "reps": 10, "rest": "90s", "calories": 45},
        {"name": "Face Pulls", "sets": 3, "reps": 12, "rest": "60s", "calories": 20},
        {"name": "Lat Pulldown", "sets": 3, "reps": 12, "rest": "90s", "calories": 35}
    ],
    "Rest": []
}

# Calendar to store workouts per date
calendar_plan = {}
macro_targets = {
    "p": 0, "c": 0, "f": 0, "cal": 0,
    "p_current": 0,
    "c_current": 0,
    "f_current": 0,
    "cal_current": 0,
    "meals": {
        "Breakfast": [],
        "Lunch": [],
        "Dinner": [],
        "Snack": []
    }
}
# ---------------- SHARED GENERATED WORKOUT ----------------

generated_today_workout = []
generated_today_info = {
    "split": "",
    "day": "",
    "difficulty": ""
}

def fade_in(alpha=0.0):
    alpha += 0.05
    if alpha <= 1.0:
        root.attributes("-alpha", alpha)
        root.after(30, fade_in, alpha)

def show_frame(name):
    for f in frames.values():
        f.place_forget()

    frames[name].place(relwidth=1, relheight=1)

    # Clear password safely when user page is shown
    if name == "user_profile":
        password_var.set("")

    if name == "macro" and "update_targets" in globals():
        update_targets()

    if name == "landing":
        update_landing_dashboard()
        if hasattr(frames["landing"], "update_meal_display"):
            frames["landing"].update_meal_display()
        if hasattr(frames["landing"], "update_workout_display"):
            frames["landing"].update_workout_display()

#-------------- Build Intro Page from external file---------
intro_page = build_intro_page(
    root=root,
    frames=frames,
    BASE_DIR=BASE_DIR,
    INTRO_FLAG_FILE=INTRO_FLAG_FILE,
    show_frame=show_frame
)

frames["intro"] = intro_page
def clickable_card(parent, title, desc, icon_path, command):
    card = tk.Frame(parent, bg="#1f1f1f", bd=2, relief="ridge",
                    padx=20, pady=20, cursor="hand2")

    def on_enter(e):
        card.configure(bg="#2a2a2a")

    def on_leave(e):
        card.configure(bg="#1f1f1f")

    def on_click(e):
        command()

    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    card.bind("<Button-1>", on_click)

    try:
        img = Image.open(icon_path).resize((64, 64), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        images[icon_path] = photo

        icon = tk.Label(card, image=photo, bg=card.cget("bg"))
        icon.pack(side="left", padx=10)
        icon.bind("<Button-1>", on_click)
    except:
        pass

    text_box = tk.Frame(card, bg=card.cget("bg"))
    text_box.pack(side="left", fill="both", expand=True)

    title_lbl = tk.Label(
        text_box, text=title, fg="#00ff99",
        bg=card.cget("bg"), font=("Arial", 14, "bold")
    )
    title_lbl.pack(anchor="w")

    desc_lbl = tk.Label(
        text_box, text=desc, fg="#cccccc",
        bg=card.cget("bg"), font=("Arial", 10),
        wraplength=260, justify="left"
    )
    desc_lbl.pack(anchor="w", pady=5)

    for w in (text_box, title_lbl, desc_lbl):
        w.bind("<Button-1>", on_click)

    return card

# ---------------- MACRO CALCULATION ----------------
def calculate_macros():
    # --- SAFETY CHECK ---
    if "weight" not in user_profile:
        return {"p": 160, "c": 260, "f": 65, "cal": 2300}

    w = user_profile.get("weight", 0)
    goal = user_profile.get("goal", "Maintain")
    gender = user_profile.get("gender", "Male")
    body_type = user_profile.get("body_type", "Mesomorph")

    if w <= 0:
        return {"p": 160, "c": 260, "f": 65, "cal": 2300}

    if gender == "Male":
        protein_mult = 2.0
        carb_mult = 4.0
    else:
        protein_mult = 1.8
        carb_mult = 3.5

    if goal == "Bulk":
        protein_mult += 0.2
        carb_mult += 1.0
    elif goal == "Cut":
        protein_mult += 0.5
        carb_mult -= 1.5

    if body_type == "Ectomorph":
        carb_mult += 1.5
        protein_mult -= 0.2
    elif body_type == "Endomorph":
        carb_mult -= 1.5
        protein_mult += 0.2

    protein = round(w * protein_mult)
    carbs = round(w * carb_mult)
    fat = round((protein * 4 + carbs * 4) * 0.25 / 9)
    calories = protein * 4 + carbs * 4 + fat * 9

    return {"p": protein, "c": carbs, "f": fat, "cal": calories}
# ---------------- DAILY MACRO RESET ----------------
def reset_daily_macros():
    global total_p, total_c, total_f, total_cal
    global vitA, vitC, calcium, iron, vitD

    total_p = 0
    total_c = 0
    total_f = 0
    total_cal = 0
    vitA = 0
    vitC = 0
    calcium = 0
    iron = 0
    vitD = 0
 
def open_profile_edit():
    show_frame("user_profile")
    open_edit_mode()
    
def logout_user():
    user_profile.clear()
    show_frame("user_profile")
# ---------------- BUILD USER PAGE ----------------
user_page, open_edit_mode = build_user_page(
    root=root,
    frames=frames,
    show_frame=show_frame,
    BASE_DIR=BASE_DIR,
    user_profile=user_profile,
    save_users=save_users,
    users=users
)

frames["user_profile"] = user_page
landing = build_landing_page(
    root=root,
    frames=frames,
    show_frame=show_frame,
    BASE_DIR=BASE_DIR,
    clickable_card=clickable_card,
    macro_targets=macro_targets,
    workout_splits=workout_splits,
    exercises=exercises,
    build_macro_page=build_macro_page,
    build_workout_page=build_workout_page,
    open_edit_mode=open_profile_edit,
    logout_callback=logout_user,
    update_landing_dashboard=update_landing_dashboard,
    foods=foods,
    images=images,
    user_info=user_profile,generated_today_workout=generated_today_workout,
    generated_today_info=generated_today_info 
)
frames["landing"] = landing
# ---------------- START ----------------
if os.path.exists(INTRO_FLAG_FILE):
    show_frame("intro")
else:
    show_frame("landing")

fade_in()
root.mainloop()