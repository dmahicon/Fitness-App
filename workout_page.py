# ==========================================================
# ELITE WORKOUT PLANNER PAGE
# ==========================================================

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import date, datetime, timedelta
import random


def build_workout_page(
        root,
        frames,
        show_frame,
        workout_splits,
        exercises,
        BASE_DIR,
        macro_targets,
        generated_today_workout,
        generated_today_info,
        update_landing_dashboard):
# ==========================================================
# THEME COLORS (MATCHED)
# ==========================================================

    BG = "#0e0e0e"
    PANEL = "#1a1a1a"
    CYAN = "#00ffcc"
    TEXT = "#e6e6e6"

    workout = tk.Frame(root, bg=BG)
    frames["workout"] = workout


# ==========================================================
# HEADER
# ==========================================================

    tk.Button(workout, text="← BACK",
              bg=CYAN,
              fg="black",
              font=("Arial", 12, "bold"),
              command=lambda: show_frame("landing")
              ).place(x=20, y=20)

    tk.Label(workout,
             text="ELITE WORKOUT PLANNER",
             fg=CYAN,
             bg=BG,
             font=("Arial", 28, "bold")).pack(pady=15)


# ==========================================================
# ICONS
# ==========================================================

    ICONS = {
        "Push": "💪",
        "Pull": "🦾",
        "Legs": "🦵",
        "Upper": "🏋️",
        "Lower": "🦿",
        "Chest/Back": "🏆",
        "Shoulders/Arms": "⚡",
        "Full": "🔥",
        "Rest": "🛌"
    }


# ==========================================================
# WORKOUT SPLITS
# ==========================================================

    SPLITS = {
        "PPL": ["Push", "Pull", "Legs", "Push", "Pull", "Legs", "Rest"],
        "Upper/Lower": ["Upper", "Lower", "Rest", "Upper", "Lower", "Rest", "Rest"],
        "Arnold": ["Chest/Back", "Shoulders/Arms", "Legs",
                   "Chest/Back", "Shoulders/Arms", "Legs", "Rest"],
        "Full Body": ["Full", "Rest", "Full", "Rest", "Full", "Rest", "Rest"]
    }


# ==========================================================
# LARGE EXERCISE POOL (NO REPETITION)
# ==========================================================

    EXERCISE_POOL = {

        "Push": [
            ("Bench Press",8,90),
            ("Incline Dumbbell Press",10,90),
            ("Decline Press",10,90),
            ("Dumbbell Shoulder Press",10,75),
            ("Arnold Press",10,75),
            ("Chest Fly",12,60),
            ("Cable Fly",12,60),
            ("Tricep Pushdown",12,60),
            ("Overhead Tricep Extension",12,60),
            ("Close Grip Bench",8,90)
        ],

        "Pull": [
            ("Pull Ups",8,90),
            ("Chin Ups",8,90),
            ("Lat Pulldown",10,90),
            ("Barbell Row",8,90),
            ("T-Bar Row",10,90),
            ("Face Pull",12,60),
            ("Rear Delt Fly",12,60),
            ("Hammer Curl",12,60),
            ("EZ Bar Curl",10,60),
            ("Preacher Curl",10,60)
        ],

        "Legs": [
            ("Squat",8,120),
            ("Front Squat",8,120),
            ("Leg Press",10,90),
            ("Romanian Deadlift",10,90),
            ("Bulgarian Split Squat",10,90),
            ("Walking Lunges",12,75),
            ("Leg Curl",12,60),
            ("Leg Extension",12,60),
            ("Calf Raises",15,45),
            ("Seated Calf Raise",15,45)
        ],

        "Full": [
            ("Squat",8,120),
            ("Bench Press",8,90),
            ("Deadlift",6,120),
            ("Pull Ups",8,90),
            ("Shoulder Press",10,75),
            ("Barbell Row",8,90),
            ("Plank",40,45)
        ],

        "Upper": [
            ("Bench Press",8,90),
            ("Pull Ups",8,90),
            ("Barbell Row",8,90),
            ("Shoulder Press",10,75),
            ("Incline Dumbbell Press",10,90),
            ("Lat Pulldown",10,90),
            ("Face Pull",12,60),
            ("EZ Bar Curl",10,60)
        ],

        "Lower": [
            ("Squat",8,120),
            ("Deadlift",6,120),
            ("Leg Press",10,90),
            ("Romanian Deadlift",10,90),
            ("Bulgarian Split Squat",10,90),
            ("Walking Lunges",12,75),
            ("Leg Curl",12,60),
            ("Calf Raises",15,45)
        ],

        "Chest/Back": [
            ("Bench Press",8,90),
            ("Incline Dumbbell Press",10,90),
            ("Chest Fly",12,60),
            ("Pull Ups",8,90),
            ("Lat Pulldown",10,90),
            ("Barbell Row",8,90),
            ("T-Bar Row",10,90)
        ],

        "Shoulders/Arms": [
            ("Shoulder Press",10,75),
            ("Arnold Press",10,75),
            ("Lateral Raise",12,60),
            ("Rear Delt Fly",12,60),
            ("EZ Bar Curl",10,60),
            ("Hammer Curl",12,60),
            ("Tricep Pushdown",12,60),
            ("Overhead Tricep Extension",12,60)
        ]
    }


# ==========================================================
# BMI CALCULATION
# ==========================================================

    def calculate_bmi():

        if not macro_targets:
            return 22

        weight = macro_targets.get("weight",70)
        height = macro_targets.get("height",170)

        return weight / ((height/100)**2)


    def bmi_category(bmi):

        if bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal"
        else:
            return "overweight"


# ==========================================================
# PERIODIZATION
# ==========================================================

    def get_training_week():

        start = date(2025,1,1)
        weeks = (date.today()-start).days // 7

        return (weeks % 4)+1


    def get_training_phase():

        week = get_training_week()

        if week == 1:
            return "Hypertrophy"

        if week == 2:
            return "Strength"

        if week == 3:
            return "Endurance"

        return "Deload"


# ==========================================================
# WORKOUT GENERATOR (NO DUPLICATES)
# ==========================================================

    def generate_workout(split_today,difficulty):

        bmi = calculate_bmi()
        bmi_cat = bmi_category(bmi)

        pool = EXERCISE_POOL.get(split_today,[])

        chosen = random.sample(pool, min(4,len(pool)))

        remaining = [x for x in pool if x not in chosen]

        extra = random.sample(remaining, min(random.randint(1,2), len(remaining)))

        chosen.extend(extra)

        workout_list = []

        phase = get_training_phase()

        for name,reps,rest in chosen:

            sets = 3

            if phase == "Hypertrophy":
                reps += 2

            elif phase == "Strength":
                sets += 1
                reps = max(5,reps-2)

            elif phase == "Endurance":
                reps += 6

            elif phase == "Deload":
                sets = 2

            if difficulty == "Beginner":
                reps += 3

            elif difficulty == "Advanced":
                sets += 1
                rest += 30

            workout_list.append({
                "name":name,
                "sets":sets,
                "reps":reps,
                "rest":f"{rest}s",
                "cal":random.randint(70,150)
            })

        return workout_list,bmi,bmi_cat


# ==========================================================
# STATS PANEL
# ==========================================================

    stats_frame = tk.Frame(workout,bg=BG)
    stats_frame.pack(pady=5)

    bmi_label = tk.Label(stats_frame,text="BMI: --",fg=CYAN,bg=BG,font=("Arial",14,"bold"))
    bmi_label.pack()

    phase_label = tk.Label(stats_frame,text="Phase: --",fg=TEXT,bg=BG,font=("Arial",13))
    phase_label.pack()

    calorie_label = tk.Label(stats_frame,text="Calories Burn: --",fg="#ffaa00",bg=BG,font=("Arial",13,"bold"))
    calorie_label.pack(pady=4)


# ==========================================================
# CONTROLS
# ==========================================================

    plan_var = tk.StringVar(value="PPL")
    difficulty_var = tk.StringVar(value="Beginner")

    controls = tk.Frame(workout,bg=BG)
    controls.pack(pady=10)

    ttk.Combobox(controls,textvariable=plan_var,
                 values=list(SPLITS.keys()),
                 state="readonly",width=18).pack(side="left",padx=10)

    ttk.Combobox(controls,textvariable=difficulty_var,
                 values=["Beginner","Intermediate","Advanced"],
                 state="readonly",width=18).pack(side="left",padx=10)


# ==========================================================
# MAIN LAYOUT
# ==========================================================

    main_frame = tk.Frame(workout,bg=BG)
    main_frame.pack(pady=20)

    calendar = Calendar(
        main_frame,
        selectmode="day",
        date_pattern="yyyy-mm-dd",
        font=("Arial",12),
        width=22,
        height=12,
        background=PANEL,
        foreground="white"
    )

    calendar.grid(row=0,column=0,padx=30)


# ==========================================================
# WORKOUT DISPLAY (TALLER)
# ==========================================================

    container = tk.Frame(main_frame,bg=PANEL,width=720,height=640)
    container.grid(row=0,column=1,padx=20)
    container.grid_propagate(False)

    canvas = tk.Canvas(container,bg=PANEL)
    scrollbar = ttk.Scrollbar(container,orient="vertical",command=canvas.yview)

    scroll_frame = tk.Frame(canvas,bg=PANEL)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0,0),window=scroll_frame,anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left",fill="both",expand=True)
    scrollbar.pack(side="right",fill="y")


# ==========================================================
# MOUSE SCROLL (FIXED)
# ==========================================================

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)),"units")

    def _bind_scroll(e):
        canvas.bind_all("<MouseWheel>",_on_mousewheel)

    def _unbind_scroll(e):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>",_bind_scroll)
    canvas.bind("<Leave>",_unbind_scroll)


# ==========================================================
# CALENDAR COLORS
# ==========================================================

    def update_calendar_colors():

        calendar.calevent_remove('all')
        today = date.today()

        calendar.tag_config("workout_day",background="#1faa59")
        calendar.tag_config("rest_day",background="#d64545")
        calendar.tag_config("past_day",background="#555555")

        for i in range(-60,60):

            d = today + timedelta(days=i)
            weekday = d.weekday()

            split = SPLITS[plan_var.get()][weekday]

            if d < today:
                calendar.calevent_create(d,"Past","past_day")

            else:

                if split == "Rest":
                    calendar.calevent_create(d,"Rest","rest_day")

                else:
                    calendar.calevent_create(d,"Workout","workout_day")


# ==========================================================
# DISPLAY WORKOUT
# ==========================================================

    def show_exercises(*args):

        for w in scroll_frame.winfo_children():
            w.destroy()

        selected = calendar.get_date()
        dt = datetime.strptime(selected,"%Y-%m-%d")

        weekday = dt.weekday()
        split_today = SPLITS[plan_var.get()][weekday]

        if split_today == "Rest":

            tk.Label(scroll_frame,
                     text="🛌 REST DAY",
                     fg="#ff5c5c",
                     bg=PANEL,
                     font=("Arial",24,"bold")).pack()

            return

        tk.Label(scroll_frame,
                 text=f"{ICONS.get(split_today)} {split_today}",
                 fg=CYAN,
                 bg=PANEL,
                 font=("Arial",22,"bold")).pack(pady=10)

        difficulty = difficulty_var.get()

        ex_list,bmi,bmi_cat = generate_workout(split_today,difficulty)
        generated_today_workout.clear()
        generated_today_workout.extend(ex_list)

        phase = get_training_phase()
        week = get_training_week()

        generated_today_info["split"] = split_today
        generated_today_info["day"] = split_today
        generated_today_info["difficulty"] = difficulty
        generated_today_info["bmi"] = round(bmi,1)
        generated_today_info["phase"] = phase
        generated_today_info["week"] = week
        bmi_label.config(text=f"BMI: {round(bmi,1)} ({bmi_cat})")
        phase_label.config(text=f"Phase: {phase} | Week {week}")

        total_cal = 0

        for ex in ex_list:

            total_cal += ex["cal"]

            row = tk.Frame(scroll_frame,bg=PANEL)
            row.pack(fill="x",pady=6,padx=10)

            tk.Label(row,text=ex["name"],
                     fg="white",bg=PANEL,
                     font=("Arial",15,"bold")).pack(anchor="w")

            tk.Label(row,
                     text=f"{ex['sets']} sets | {ex['reps']} reps | Rest {ex['rest']} | 🔥 {ex['cal']} cal",
                     fg="#bbbbbb",bg=PANEL).pack(anchor="w")

        calorie_label.config(text=f"Calories Burn: {total_cal} kcal")


# ==========================================================
# EVENTS
# ==========================================================

    calendar.bind("<<CalendarSelected>>",show_exercises)

    plan_var.trace_add(
        "write",
        lambda *args:(update_calendar_colors(),show_exercises())
    )

    difficulty_var.trace_add("write",show_exercises)


# ==========================================================
# INITIAL LOAD
# ==========================================================

    update_landing_dashboard()
    update_calendar_colors()
    show_exercises()

    return workout