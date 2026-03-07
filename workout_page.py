import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import date, datetime, timedelta
from PIL import Image, ImageTk
import os
import random


def build_workout_page(
        root,
        frames,
        show_frame,
        workout_splits,
        exercises,
        BASE_DIR,
        macro_targets=None):

    workout = tk.Frame(root, bg="#0e0e0e")
    frames["workout"] = workout

    CYAN = "#00ffcc"
    DARK = "#1a1a1a"


    tk.Button(workout, text="← BACK",
              bg=CYAN,
              fg="black",
              font=("Arial", 11, "bold"),
              command=lambda: show_frame("landing")
              ).place(x=20, y=20)

    tk.Label(workout,
             text="ELITE WORKOUT PLANNER",
             fg=CYAN,
             bg="#0e0e0e",
             font=("Arial", 26, "bold")).pack(pady=15)


    ICONS = {
        "Push": "💪",
        "Pull": "🦾",
        "Legs": "🦵",
        "Upper": "🏋️",
        "Lower": "🦿",
        "Full": "🔥",
        "Chest": "🏆",
        "Back": "🛡",
        "Shoulders": "⚡",
        "Arms": "💥",
        "Chest/Back": "🏆🛡",
        "Shoulders/Arms": "⚡💥",
        "Rest": "🛌"
    }

    SPLITS = {
        "PPL": ["Push", "Pull", "Legs", "Push", "Pull", "Legs", "Rest"],
        "Arnold": ["Chest/Back", "Shoulders/Arms", "Legs",
                   "Chest/Back", "Shoulders/Arms", "Legs", "Rest"],
        "Upper/Lower": ["Upper", "Lower", "Rest",
                        "Upper", "Lower", "Rest", "Rest"],
        "PPL x Arnold": ["Push", "Pull", "Legs",
                         "Chest/Back", "Shoulders/Arms", "Legs", "Rest"]
    }

    def get_cal(ex):
        return ex.get("cal", ex.get("calories", 0))

 
    DEFAULT_EXERCISES = {
        "Chest": [
            {"name": "Bench Press", "sets": 3, "reps": 10, "rest": "90s", "cal": 100, "image": os.path.join(BASE_DIR, "images", "bench_press.jpg")},
            {"name": "Incline Dumbbell Press", "sets": 3, "reps": 12, "rest": "90s", "cal": 80, "image": os.path.join(BASE_DIR, "images", "incline_dumbbell_press.jpg")}
        ],
        "Back": [
            {"name": "Pull-ups", "sets": 3, "reps": 8, "rest": "90s", "cal": 90, "image": os.path.join(BASE_DIR, "images", "pull_ups.jpg")},
            {"name": "Bent-over Rows", "sets": 3, "reps": 10, "rest": "90s", "cal": 85, "image": os.path.join(BASE_DIR, "images", "bent_over_rows.jpg")}
        ],
        "Shoulders": [
            {"name": "Overhead Press", "sets": 3, "reps": 10, "rest": "60s", "cal": 70, "image": os.path.join(BASE_DIR, "images", "overhead_press.jpg")},
            {"name": "Lateral Raises", "sets": 3, "reps": 12, "rest": "60s", "cal": 50, "image": os.path.join(BASE_DIR, "images", "lateral_raises.jpg")}
        ],
        "Arms": [
            {"name": "Bicep Curls", "sets": 3, "reps": 12, "rest": "45s", "cal": 40, "image": os.path.join(BASE_DIR, "images", "bicep_curls.jpg")},
            {"name": "Tricep Dips", "sets": 3, "reps": 10, "rest": "60s", "cal": 50, "image": os.path.join(BASE_DIR, "images", "tricep_dips.jpg")}
        ],
        "Legs": [
            {"name": "Squats", "sets": 3, "reps": 12, "rest": "90s", "cal": 100, "image": os.path.join(BASE_DIR, "images", "squats.jpg")},
            {"name": "Leg Press", "sets": 3, "reps": 12, "rest": "90s", "cal": 90, "image": os.path.join(BASE_DIR, "images", "leg_press.jpg")},
            {"name": "Lunges", "sets": 3, "reps": 12, "rest": "60s", "cal": 80, "image": os.path.join(BASE_DIR, "images", "lunges.jpg")}
        ]
    }

    for muscle, default_list in DEFAULT_EXERCISES.items():
        if muscle not in exercises or not exercises[muscle]:
            exercises[muscle] = default_list

    TARGET_GROUPS = {
        "Push": exercises["Chest"] + exercises["Shoulders"] + exercises["Arms"],
        "Pull": exercises["Back"] + exercises["Arms"],
        "Legs": exercises["Legs"],
        "Upper": exercises["Chest"] + exercises["Back"] + exercises["Shoulders"] + exercises["Arms"],
        "Lower": exercises["Legs"],
        "Full": sum(exercises.values(), []),
        "Chest/Back": exercises["Chest"] + exercises["Back"],
        "Shoulders/Arms": exercises["Shoulders"] + exercises["Arms"]
    }

    def scale_workout(base_list, set_add=0, rep_add=0, cal_mult=1.0):
        scaled = []
        for ex in base_list:
            scaled.append({
                "name": ex["name"],
                "sets": ex["sets"] + set_add,
                "reps": ex["reps"] + rep_add,
                "rest": ex["rest"],
                "cal": int(get_cal(ex) * cal_mult),
                "image": ex.get("image", "")
            })
        return scaled

    EXERCISES_SCALED = {"Beginner": {}, "Intermediate": {}, "Advanced": {}}

    for group in TARGET_GROUPS:
        base = TARGET_GROUPS[group]
        EXERCISES_SCALED["Beginner"][group] = base
        EXERCISES_SCALED["Intermediate"][group] = scale_workout(base, 1, 2, 1.2)
        EXERCISES_SCALED["Advanced"][group] = scale_workout(base, 2, 4, 1.4)

    plan_var = tk.StringVar(value="PPL")
    difficulty_var = tk.StringVar(value="Beginner")


    controls = tk.Frame(workout, bg="#0e0e0e")
    controls.pack(pady=10)

    ttk.Combobox(controls, textvariable=plan_var,
                 values=list(SPLITS.keys()),
                 state="readonly", width=22).pack(side="left", padx=10)

    ttk.Combobox(controls, textvariable=difficulty_var,
                 values=["Beginner", "Intermediate", "Advanced"],
                 state="readonly", width=18).pack(side="left", padx=10)

 
    main_frame = tk.Frame(workout, bg="#0e0e0e")
    main_frame.pack(pady=20)

    calendar = Calendar(main_frame,
                        selectmode="day",
                        date_pattern="yyyy-mm-dd",
                        font=("Arial", 14),
                        headersbackground=CYAN,
                        normalbackground=DARK,
                        weekendbackground="#141414",
                        foreground="white")

    calendar.grid(row=0, column=0, padx=30, ipadx=20, ipady=20)

    container = tk.Frame(main_frame, bg=DARK, width=600, height=550)
    container.grid(row=0, column=1, padx=20)
    container.grid_propagate(False)

    canvas = tk.Canvas(container,
                       bg=DARK,
                       highlightthickness=0,
                       width=600,
                       height=550)

    scrollbar = ttk.Scrollbar(container,
                              orient="vertical",
                              command=canvas.yview)

    scroll_frame = tk.Frame(canvas, bg=DARK)

    scroll_frame.bind("<Configure>",
                      lambda e: canvas.configure(
                          scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0),
                         window=scroll_frame,
                         anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_linux_scroll(event):
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    def bind_scroll(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_linux_scroll)
        canvas.bind_all("<Button-5>", _on_linux_scroll)

    def unbind_scroll(event):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", bind_scroll)
    canvas.bind("<Leave>", unbind_scroll)

    def open_image_popup(img_path):
        popup = tk.Toplevel(workout)
        popup.title("Exercise Demo")
        popup.configure(bg="#0e0e0e")

        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((400, 400))
            photo = ImageTk.PhotoImage(img)
        else:
            img = Image.new("RGB", (400, 400), color=(50, 50, 50))
            photo = ImageTk.PhotoImage(img)

        lbl = tk.Label(popup, image=photo, bg="#0e0e0e")
        lbl.image = photo
        lbl.pack(padx=20, pady=20)


    def add_hover(widget):
        def enter(e):
            widget.config(bg="#242424")

        def leave(e):
            widget.config(bg=DARK)

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def update_calendar_colors():
        calendar.calevent_remove('all')
        today = date.today()

        calendar.tag_config("workout_day", background="green", foreground="white")
        calendar.tag_config("rest_day", background="red", foreground="white")

        for i in range(60):
            d = today + timedelta(days=i)
            weekday = d.weekday()
            split = SPLITS[plan_var.get()][weekday]

            if split == "Rest":
                calendar.calevent_create(d, "Rest", "rest_day")
            else:
                calendar.calevent_create(d, "Workout", "workout_day")

    def show_exercises(*args):

        for w in scroll_frame.winfo_children():
            w.destroy()

        selected = calendar.get_date()
        dt = datetime.strptime(selected, "%Y-%m-%d")
        weekday = dt.weekday()

        split_today = SPLITS[plan_var.get()][weekday]

        workout_splits["current_plan"] = plan_var.get()
        workout_splits["current_difficulty"] = difficulty_var.get()
        workout_splits["current_day"] = split_today

        if split_today == "Rest":

            tk.Label(scroll_frame,
                     text="🛌 REST DAY",
                     fg="red",
                     bg=DARK,
                     font=("Arial", 22, "bold")).pack()

            tk.Label(scroll_frame,
                     text="Recovery is where growth happens.",
                     fg="#bbbbbb",
                     bg=DARK,
                     font=("Arial", 11)).pack(pady=5)
            return

        tk.Label(scroll_frame,
                 text=f"{ICONS.get(split_today,'🏋️')} {split_today}",
                 fg=CYAN,
                 bg=DARK,
                 font=("Arial", 18, "bold")).pack(pady=10)

        level = difficulty_var.get()
        ex_list = EXERCISES_SCALED[level].get(split_today, []).copy()

        total_cal = 0

        for ex in ex_list:

            total_cal += get_cal(ex)

            row = tk.Frame(scroll_frame, bg=DARK)
            row.pack(fill="x", pady=6, padx=10)

            add_hover(row)

            text = tk.Frame(row, bg=DARK)
            text.pack(side="left")

            tk.Label(text,
                     text=ex["name"],
                     fg="white",
                     bg=DARK,
                     font=("Arial", 13, "bold")).pack(anchor="w")

            tk.Label(text,
                     text=f"{ex['sets']} sets | {ex['reps']} reps | Rest {ex['rest']} | 🔥 {get_cal(ex)} cal",
                     fg="#bbbbbb",
                     bg=DARK,
                     font=("Arial", 11)).pack(anchor="w")

            if ex.get("image") and os.path.exists(ex["image"]):

                img = Image.open(ex["image"])
                img = img.resize((40, 40))

                photo = ImageTk.PhotoImage(img)

                icon = tk.Label(row,
                                image=photo,
                                bg=DARK,
                                cursor="hand2")

                icon.image = photo
                icon.pack(side="right", padx=5)

                icon.bind("<Button-1>",
                          lambda e, img=ex["image"]: open_image_popup(img))

        tk.Label(scroll_frame,
                 text=f"Total Calories: {total_cal} kcal",
                 fg=CYAN,
                 bg=DARK,
                 font=("Arial", 14, "bold")).pack(pady=10)

    calendar.bind("<<CalendarSelected>>", show_exercises)

    plan_var.trace_add(
        "write",
        lambda *args: (update_calendar_colors(), show_exercises())
    )

    difficulty_var.trace_add("write", show_exercises)

    update_calendar_colors()
    show_exercises()

    return workout