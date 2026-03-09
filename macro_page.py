import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os



def add_button_effect(btn, normal_bg, press_bg):

    def on_press(e):
        btn.config(bg=press_bg)

    def on_release(e):
        btn.config(bg=normal_bg)

    btn.bind("<ButtonPress-1>", on_press)
    btn.bind("<ButtonRelease-1>", on_release)


def build_macro_page(root, frames, show_frame, foods, images, BASE_DIR, user_info, macro_targets, update_landing_dashboard):

    macro = tk.Frame(root, bg="#0e0e0e")
    frames["macro"] = macro

 
    macro_targets.setdefault("p_current", 0)
    macro_targets.setdefault("c_current", 0)
    macro_targets.setdefault("f_current", 0)
    macro_targets.setdefault("cal_current", 0)
    macro_targets.setdefault("meals", {"Breakfast": [], "Lunch": [], "Dinner": [], "Snack": []})

    current_meal = tk.StringVar(value="Breakfast")

    last_added = {"meal": None, "food": None}

 
    def calculate_user_macros(user_info):

        weight = float(user_info.get("weight", 70))
        goal = str(user_info.get("goal", "Maintain"))
        gender = str(user_info.get("gender", "Male"))
        body_type = str(user_info.get("body_type", "Mesomorph"))

        protein_mult = 2.0 if gender == "Male" else 1.8
        carb_mult = 4.0 if gender == "Male" else 3.5

        if goal == "Bulk":
            protein_mult += 0.2
            carb_mult += 1
        elif goal == "Cut":
            protein_mult += 0.5
            carb_mult -= 1.5

        if body_type == "Ectomorph":
            carb_mult += 1.5
            protein_mult -= 0.2
        elif body_type == "Endomorph":
            carb_mult -= 1.5
            protein_mult += 0.2

        protein = round(weight * protein_mult)
        carbs = round(weight * carb_mult)
        fat = round((protein*4 + carbs*4) * 0.25 / 9)
        calories = protein*4 + carbs*4 + fat*9

        return {"p": protein, "c": carbs, "f": fat, "cal": calories}

    goals = calculate_user_macros(user_info)

    macro_targets["p"] = goals["p"]
    macro_targets["c"] = goals["c"]
    macro_targets["f"] = goals["f"]
    macro_targets["cal"] = goals["cal"]


    header = tk.Frame(macro, bg="#0e0e0e")
    header.pack(fill="x", padx=20, pady=10)

    back_btn = tk.Button(header, text="⬅ BACK", font=("Arial",12,"bold"),
              bg="#0e0e0e", fg="#00ff99", bd=0,
              command=lambda: show_frame("landing"))

    back_btn.pack(side="left")
    add_button_effect(back_btn, "#0e0e0e", "#1a1a1a")

    tk.Label(header, text="🍽 MACRO TRACKER",
             font=("Arial",26,"bold"),
             fg="#00ff99", bg="#0e0e0e").pack(pady=5)


    top_container = tk.Frame(macro, bg="#0e0e0e")
    top_container.pack(pady=10)


    gauge_frame = tk.Frame(top_container, bg="#1c1c1c", padx=20, pady=10,
                           highlightbackground="#00ffcc", highlightthickness=1)
    gauge_frame.pack(side="left", padx=20)

    def make_gauge(title, icon, col, key, max_key, color):

        frame = tk.Frame(gauge_frame, bg="#1c1c1c")
        frame.grid(row=0, column=col, padx=20)

        tk.Label(frame, text=f"{icon} {title}", fg=color,
                 bg="#1c1c1c",
                 font=("Arial",12,"bold")).pack()

        canvas = tk.Canvas(frame, width=160, height=160,
                           bg="#1c1c1c", highlightthickness=0)
        canvas.pack()

        def draw():

            canvas.delete("all")

            current = macro_targets.get(key,0)
            max_val = max(macro_targets.get(max_key,1),1)

            percent = min(current/max_val,1)

            canvas.create_oval(20,20,140,140,
                               outline="#333", width=12)

            if percent > 0:
                extent = -360*percent if percent < 1 else -359
                canvas.create_arc(20,20,140,140,
                                  start=90, extent=extent,
                                  outline=color, width=12,
                                  style="arc")

            canvas.create_text(80,80,
                               text=f"{int(current)}/{int(max_val)}",
                               fill="white",
                               font=("Arial",11,"bold"))

        return draw

    draw_cal = make_gauge("Calories","🔥",0,"cal_current","cal","#ffaa00")
    draw_p   = make_gauge("Protein","🥩",1,"p_current","p","#00aaff")
    draw_c   = make_gauge("Carbs","🍞",2,"c_current","c","#00ff99")
    draw_f   = make_gauge("Fat","🥑",3,"f_current","f","#ff4444")

 
    history_frame = tk.Frame(top_container, bg="#1c1c1c", padx=15, pady=10,
                             highlightbackground="#00ffcc", highlightthickness=1)
    history_frame.pack(side="left", padx=20)

    tk.Label(history_frame, text="📜 MEAL HISTORY",
             font=("Arial",14,"bold"),
             fg="#00ff99", bg="#1c1c1c").pack(anchor="w")

    history_list = tk.Frame(history_frame, bg="#1c1c1c")
    history_list.pack(pady=5)

    def remove_food(item, meal):

        macro_targets["p_current"] -= item["p"]
        macro_targets["c_current"] -= item["c"]
        macro_targets["f_current"] -= item["f"]
        macro_targets["cal_current"] -= item["cal"]

        macro_targets["meals"][meal].remove(item)

        refresh()

    def update_history():

        for widget in history_list.winfo_children():
            widget.destroy()

        meal = current_meal.get()

        for item in macro_targets["meals"][meal]:

            row = tk.Frame(history_list, bg="#1c1c1c")
            row.pack(anchor="w", pady=2)

            text = f"{item['name']} ({item['cal']} kcal)"

            tk.Label(row, text=text,
                     fg="white", bg="#1c1c1c",
                     font=("Arial",10)).pack(side="left")

            remove_btn = tk.Button(row, text="✕",
                      bg="#ff4444", fg="white",
                      font=("Arial",8,"bold"),
                      command=lambda i=item,m=meal: remove_food(i,m))
            remove_btn.pack(side="left", padx=5)

            add_button_effect(remove_btn, "#ff4444", "#cc3333")


    def refresh():
        draw_cal()
        draw_p()
        draw_c()
        draw_f()
        update_history()
        update_landing_dashboard()


    def add_food(food_name, vals):

        meal = current_meal.get()

        macro_targets["p_current"] += vals["p"]
        macro_targets["c_current"] += vals["c"]
        macro_targets["f_current"] += vals["f"]
        macro_targets["cal_current"] += vals["cal"]

        item = {
            "name": food_name,
            "img": vals["img"],
            "p": vals["p"],
            "c": vals["c"],
            "f": vals["f"],
            "cal": vals["cal"]
        }

        macro_targets["meals"][meal].append(item)

        last_added["meal"] = meal
        last_added["food"] = item

        refresh()

  
    def undo_last():

        meal = last_added["meal"]
        item = last_added["food"]

        if not meal or not item:
            return

        if item in macro_targets["meals"][meal]:

            macro_targets["meals"][meal].remove(item)

            macro_targets["p_current"] -= item["p"]
            macro_targets["c_current"] -= item["c"]
            macro_targets["f_current"] -= item["f"]
            macro_targets["cal_current"] -= item["cal"]

        last_added["meal"] = None
        last_added["food"] = None

        refresh()


    meal_frame = tk.Frame(macro, bg="#0e0e0e")
    meal_frame.pack(pady=10)

    for meal in ["Breakfast","Lunch","Dinner","Snack"]:

        rb = tk.Radiobutton(
            meal_frame,
            text=meal,
            variable=current_meal,
            value=meal,
            bg="#0e0e0e",
            fg="#00ff99",
            selectcolor="#1c1c1c",
            indicatoron=0,
            width=12,
            command=refresh
        )
        rb.pack(side="left", padx=5)


    tk.Label(macro, text="🍱 FOOD LIBRARY",
             font=("Arial",20,"bold"),
             fg="#00ff99",
             bg="#0e0e0e").pack(pady=15)

    food_frame = tk.Frame(macro, bg="#1c1c1c",
                          highlightbackground="#00ffcc",
                          highlightthickness=1)
    food_frame.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(food_frame, bg="#1c1c1c", highlightthickness=0)
    scroll = ttk.Scrollbar(food_frame, command=canvas.yview)

    inner = tk.Frame(canvas, bg="#1c1c1c")

    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0,0), window=inner, anchor="nw")

    canvas.configure(yscrollcommand=scroll.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")


    # ==========================================================
    # FIXED SCROLL FUNCTION
    # ==========================================================

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _bind_scroll(e):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind_scroll(e):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", _bind_scroll)
    canvas.bind("<Leave>", _unbind_scroll)


    max_cols = 8
    row = col = 0

    for i in range(max_cols):
        inner.grid_columnconfigure(i, weight=1)

    for food_name, vals in foods.items():

        card = tk.Frame(inner, bg="#262626", bd=1,
                        relief="ridge", padx=10, pady=10,
                        highlightbackground="#00ffcc",
                        highlightthickness=1)

        card.grid(row=row, column=col,
                  padx=11, pady=11, sticky="nsew")

        try:
            img_path = os.path.join(BASE_DIR, vals["img"])
            img = Image.open(img_path).resize((130,130))
            photo = ImageTk.PhotoImage(img)

            images[food_name] = photo

            tk.Label(card, image=photo,
                     bg="#262626").pack(pady=5)

        except:
            tk.Label(card, text="No Img",
                     fg="white", bg="#262626").pack()

        txt = f"{food_name}\nP:{vals['p']} C:{vals['c']} F:{vals['f']}\n{vals['cal']} kcal"

        tk.Label(card, text=txt,
                 fg="white", bg="#262626",
                 justify="center",
                 font=("Arial",10,"bold")).pack(pady=5)

        btns = tk.Frame(card, bg="#262626")
        btns.pack(pady=5)

        add_btn = tk.Button(btns, text="+ ADD",
                  bg="#00ff99", width=8,
                  command=lambda n=food_name,v=vals: add_food(n,v))
        add_btn.pack(side="left", padx=2)

        add_button_effect(add_btn, "#00ff99", "#00cc77")

        undo_btn = tk.Button(btns, text="UNDO",
                  bg="#ff4444", fg="white", width=8,
                  command=undo_last)
        undo_btn.pack(side="left", padx=2)

        add_button_effect(undo_btn, "#ff4444", "#cc3333")

        col += 1
        if col >= max_cols:
            col = 0
            row += 1


    def save_meals():
        messagebox.showinfo("Saved","Meals saved!")

    save_btn = tk.Button(macro, text="SAVE MEALS",
              bg="#00ff99", fg="black",
              font=("Arial",12,"bold"),
              width=20,
              command=save_meals)

    save_btn.pack(pady=10)

    add_button_effect(save_btn, "#00ff99", "#00cc77")

    refresh()

    return macro