import tkinter as tk
from PIL import Image, ImageTk
import os
import datetime
import random
today = datetime.date.today().isoformat()


image_cache = {}

def build_landing_page(
    root, frames, show_frame, BASE_DIR, clickable_card,
    macro_targets, workout_splits, exercises,
    build_macro_page, build_workout_page,
    open_edit_mode, 
    logout_callback, update_landing_dashboard,
    foods=None, images=None, calendar_plan=None, user_info=None 
):

    if images is None:
        images = {}
    if foods is None:
        foods = {}
    if user_info is None:
        user_info = {}

    landing = tk.Frame(root, bg="#0b0f14")
    frames["landing"] = landing

    macro_targets.setdefault("meals", {
        "Breakfast": [],
        "Lunch": [],
        "Dinner": [],
        "Snack": []
    })


    top_bar = tk.Frame(
        landing,
        bg="#111821",
        height=95,
        highlightbackground="#00ffcc",
        highlightthickness=2
    )
    top_bar.pack(fill="x")
    top_bar.pack_propagate(False)

    glow_line = tk.Frame(top_bar, bg="#00ffcc", height=2)
    glow_line.pack(fill="x", side="bottom")

    profile_frame = tk.Frame(top_bar, bg="#111821")
    profile_frame.pack(side="left", padx=30)

    canvas_icon = tk.Canvas(profile_frame, width=60, height=60,
                            bg="#111821", highlightthickness=0)
    canvas_icon.pack(pady=12)

    canvas_icon.create_oval(5, 5, 55, 55, fill="#00ffcc", outline="")

    initial = user_info.get("name", "U")[0].upper()
    canvas_icon.create_text(30, 30,
                            text=initial,
                            font=("Segoe UI", 20, "bold"),
                            fill="black")
    menu = tk.Menu(
        root,
        tearoff=0,
        bg="#1a1f27",
        fg="white",
        activebackground="#00ffcc",
        activeforeground="black",
        bd=0
    )

    menu.add_command(
        label="👤 Edit Profile",
        command=lambda: (show_frame("user_profile"), open_edit_mode())
    )

    menu.add_separator()


    menu.add_command(
        label="🚪 Logout",
        command=logout_callback
    )
    def open_menu(event):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    canvas_icon.bind("<Button-1>", open_menu)
    tk.Label(top_bar,
             text="💪 FITNESS DASHBOARD 🚀",
             fg="#00ffcc",
             bg="#111821",
             font=("Segoe UI", 24, "bold")
             ).place(relx=0.5, rely=0.5, anchor="center")


    if macro_targets.get("last_date") != today:
        macro_targets["meals"] = {
            "Breakfast": [],
            "Lunch": [],
            "Dinner": [],
            "Snack": []
        }
        macro_targets["last_date"] = today
    content = tk.Frame(landing, bg="#0b0f14")
    content.pack(fill="both", expand=True, padx=40, pady=30)

    content.grid_columnconfigure(0, weight=3)
    content.grid_columnconfigure(1, weight=2)
    content.grid_rowconfigure(0, weight=1)

    def add_hover_effect(frame):
        def on_enter(e):
            frame.config(highlightthickness=2, highlightbackground="#00ffaa")
        def on_leave(e):
            frame.config(highlightthickness=1, highlightbackground="#00ffcc")
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

    meals_frame = tk.Frame(content, bg="#1a1f27",
                           highlightbackground="#00ffcc",
                           highlightthickness=1)
    meals_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    add_hover_effect(meals_frame)

    tk.Label(meals_frame,
             text="🍽️ TODAY'S MEALS 🍳🥗🍗",
             fg="#00ffcc",
             bg="#1a1f27",
             font=("Segoe UI", 20, "bold")
             ).pack(pady=18)

    meals_container = tk.Frame(meals_frame, bg="#1a1f27")
    meals_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    landing.image_refs = []

    def update_meal_display():

        for widget in meals_container.winfo_children():
            widget.destroy()

        landing.image_refs = []
        meal_types = ["Breakfast", "Lunch", "Dinner", "Snack"]

        meal_icons = {
            "Breakfast": "🌅 Breakfast 🍳",
            "Lunch": "☀️ Lunch 🍛",
            "Dinner": "🌙 Dinner 🍽️",
            "Snack": "⚡ Snack 🍎"
        }

        meals_container.grid_columnconfigure(0, weight=1)
        meals_container.grid_columnconfigure(1, weight=1)

        for index, meal in enumerate(meal_types):

            row_pos = index // 2
            col_pos = index % 2

            frame = tk.Frame(meals_container,
                             bg="#222831",
                             padx=15,
                             pady=15,
                             highlightbackground="#00ffcc",
                             highlightthickness=1)
            frame.grid(row=row_pos, column=col_pos,
                       padx=15, pady=15, sticky="nsew")

            tk.Label(frame,
                     text=meal_icons.get(meal, meal),
                     fg="#ffaa00",
                     bg="#222831",
                     font=("Segoe UI", 13, "bold")
                     ).pack(anchor="w")

            foods_list = macro_targets["meals"].get(meal, [])
            food_counter = {}

            for item in foods_list:
                name = item.get("name")
                if name not in food_counter:
                    food_counter[name] = {"count": 1, "data": item}
                else:
                    food_counter[name]["count"] += 1

            image_row = tk.Frame(frame, bg="#222831")
            image_row.pack(fill="x", pady=8)

            col = 0
            max_cols = 4

            for food_name, info in food_counter.items():

                data = info["data"]
                count = info["count"]

                img_frame = tk.Frame(image_row, bg="#222831")
                img_frame.grid(row=0, column=col, padx=8, pady=6)

                image_name = data.get("img")

                if image_name:
                    img_path = os.path.join(BASE_DIR, image_name)

                    if os.path.isfile(img_path):
                        try:
                            img = Image.open(img_path)
                            img = img.resize((60, 60), Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(img)
                            landing.image_refs.append(photo)

                            img_label = tk.Label(img_frame,
                                                 image=photo,
                                                 bg="#222831")
                            img_label.pack()

                            calories = data.get("calories", 0)
                            protein = data.get("protein", 0)
                            carbs = data.get("carbs", 0)
                            fats = data.get("fats", 0)

                            tk.Label(img_frame,
                                     text=f"{calories} kcal",
                                     fg="#cccccc",
                                     bg="#222831",
                                     font=("Segoe UI", 8)
                                     ).pack(pady=(4, 0))

                            tk.Label(img_frame,
                                     text=f"P{protein}/C{carbs}/F{fats}",
                                     fg="#888888",
                                     bg="#222831",
                                     font=("Segoe UI", 7)
                                     ).pack()

                            if count > 1:
                                badge = tk.Label(img_frame,
                                                 text=f"x{count}",
                                                 bg="#ff3b3b",
                                                 fg="white",
                                                 font=("Segoe UI", 8, "bold"))
                                badge.place(x=2, y=2)

                        except Exception as e:
                            print("Image error:", e)

                col += 1
                if col >= max_cols:
                    col = 0

    landing.update_meal_display = update_meal_display


    workout_frame = tk.Frame(content, bg="#1a1f27",
                             highlightbackground="#00ffcc",
                             highlightthickness=1)
    workout_frame.grid(row=0, column=1, sticky="nsew")
    add_hover_effect(workout_frame)

    tk.Label(workout_frame,
             text="🏋️ TODAY'S WORKOUT 🔥",
             fg="#00ffcc",
             bg="#1a1f27",
             font=("Segoe UI", 20, "bold")
             ).pack(pady=18)

    workout_container = tk.Frame(workout_frame, bg="#1a1f27")
    workout_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def update_workout_display():

        for widget in workout_container.winfo_children():
            widget.destroy()

        current_plan = workout_splits.get("current_plan", "PPL")
        current_day = workout_splits.get("current_day", "Push")
        difficulty = workout_splits.get("current_difficulty", "Beginner")

        tk.Label(workout_container,
                text=f"📋 {current_plan} Split • 🎯 {difficulty}",
                fg="#ffaa00",
                bg="#1a1f27",
                font=("Segoe UI", 12, "bold")
                ).pack(anchor="w")

        tk.Label(workout_container,
                text=f"💪 Today: {current_day} Day",
                fg="#00ffcc",
                bg="#1a1f27",
                font=("Segoe UI", 15, "bold")
                ).pack(anchor="w", pady=5)

        if current_day == "Push":
            exercises_today = (
                exercises.get("Chest", []) +
                exercises.get("Shoulders", []) +
                exercises.get("Arms", [])
            )

        elif current_day == "Pull":
            exercises_today = (
                exercises.get("Back", []) +
                exercises.get("Arms", [])
            )

        elif current_day == "Upper":
            exercises_today = (
                exercises.get("Chest", []) +
                exercises.get("Back", []) +
                exercises.get("Shoulders", []) +
                exercises.get("Arms", [])
            )

        elif current_day == "Lower":
            exercises_today = exercises.get("Legs", [])

        elif current_day == "Full":
            exercises_today = []
            for m in exercises:
                exercises_today += exercises[m]

        elif current_day == "Chest/Back":
            exercises_today = (
                exercises.get("Chest", []) +
                exercises.get("Back", [])
            )

        elif current_day == "Shoulders/Arms":
            exercises_today = (
                exercises.get("Shoulders", []) +
                exercises.get("Arms", [])
            )

        else:
            exercises_today = exercises.get(current_day, [])

        # ✅ GRID CONTAINER (2x2 layout)
        grid_container = tk.Frame(workout_container, bg="#1a1f27")
        grid_container.pack(fill="both", expand=True, pady=10)

        grid_container.grid_columnconfigure(0, weight=1)
        grid_container.grid_columnconfigure(1, weight=1)
        total_calories = 0

        preview_exercises = random.sample(exercises_today, min(4, len(exercises_today)))

        for index, ex in enumerate(preview_exercises):

            name = ex.get("name", "")
            sets = ex.get("sets", 0)
            reps = ex.get("reps", 0)
            muscle = ex.get("muscle", "Main Muscle")
            rest = ex.get("rest", "60s")
            tempo = ex.get("tempo", "2-1-2")
            calories = ex.get("calories", ex.get("cal", 0))

            total_calories += calories

            row = index // 2
            col = index % 2

            ex_frame = tk.Frame(grid_container, bg="#222831",
                                highlightbackground="#00ffcc",
                                highlightthickness=1,
                                padx=12, pady=10)

            ex_frame.grid(row=row, column=col,
                        padx=10, pady=10,
                        sticky="nsew")

            tk.Label(ex_frame,
                    text=f"🏋️ {name}",
                    fg="white",
                    bg="#222831",
                    font=("Segoe UI", 12, "bold")
                    ).pack(anchor="w")

            tk.Label(ex_frame,
                    text=f"📊 {sets} sets x {reps} reps",
                    fg="#cccccc",
                    bg="#222831",
                    font=("Segoe UI", 10)
                    ).pack(anchor="w", pady=2)

            tk.Label(ex_frame,
                    text=f"💪 {muscle}",
                    fg="#aaaaaa",
                    bg="#222831",
                    font=("Segoe UI", 9)
                    ).pack(anchor="w")

            tk.Label(ex_frame,
                    text=f"🔥 {calories} kcal",
                    fg="#ff4d4d",
                    bg="#222831",
                    font=("Segoe UI", 9, "bold")
                    ).pack(anchor="w", pady=4)

        tk.Label(workout_container,
                text=f"🔥 TOTAL ESTIMATED BURN: {total_calories} kcal",
                fg="#ff4d4d",
                bg="#1a1f27",
                font=("Segoe UI", 13, "bold")
                ).pack(pady=10)
    landing.update_workout_display = update_workout_display

    bottom_section = tk.Frame(landing, bg="#0b0f14")
    bottom_section.pack(pady=30)

    clickable_card(
        bottom_section,
        "🍎 Macro Counter 📊",
        "Track calories, protein, carbs & fats.",
        os.path.join(BASE_DIR, "images/macro.png"),
        lambda: show_frame("macro")
    ).pack(side="left", padx=50)

    clickable_card(
        bottom_section,
        "🏋️ Workout Planner 📅",
        "Plan and track workouts.",
        os.path.join(BASE_DIR, "images/workout.png"),
        lambda: show_frame("workout")
    ).pack(side="left", padx=50)


    build_macro_page(root, frames, show_frame,
                     foods, images, BASE_DIR, user_info,
                     macro_targets, update_landing_dashboard)

    build_workout_page(root, frames, show_frame,
                       workout_splits, exercises, BASE_DIR)

    return landing