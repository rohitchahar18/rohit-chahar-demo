
from tkinter import *
from PIL import Image, ImageTk
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

DARK = False

LIGHT_BG = "#f5f5f5"
DARK_BG = "#1e1e1e"

LIGHT_CARD = "white"
DARK_CARD = "#2c2c2c"

LIGHT_TEXT = "black"
DARK_TEXT = "white"





root = Tk()

main = Frame(root, bg="#f5f5f5")
main.pack(side=LEFT, fill=BOTH, expand=True)   # ✅ ye hona chahiye

top = Frame(main, bg="white")
top.pack(fill=X)
# ===== CANVAS (FULL PAGE SCROLL) =====
canvas = Canvas(main, bg="#f5f5f5", highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(main, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)

# ===== SCROLLABLE FRAME =====
scroll_frame = Frame(canvas, bg="#f5f5f5")
canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=1400)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scroll_frame.bind("<Configure>", on_configure)



from PIL import Image, ImageTk

# ===== SLIDER IMAGES =====
images = [
    r"C:\Users\LENOVO\Desktop\Its-a-complete-value-meal-1.png",
    r"C:\Users\LENOVO\Desktop\BK.jpg",
    r"C:\Users\LENOVO\Desktop\2x_ms_20240527134930729095_60_Banner_750x400gif.jpeg",
    r"C:\Users\LENOVO\Desktop\Screenshot 2026-04-14 194925.png",
    r"C:\Users\LENOVO\Desktop\Screenshot 2026-04-14 195433.png"
]

slider_imgs = []
for img in images:
    im = Image.open(img)
    im = im.resize((1360, 420))
    slider_imgs.append(ImageTk.PhotoImage(im))

slider_label = Label(scroll_frame)
slider_label.pack(pady=5)

slider_label = Label(scroll_frame, anchor="w")
slider_label.pack(fill=X)

index = 0

def slide():
    global index
    slider_label.config(image=slider_imgs[index])
    index = (index + 1) % len(slider_imgs)
    root.after(2000, slide)

slide()





root.title("Food Dashboard")
root.geometry("1200x700")
root.config(bg="#f5f5f5")





ttop = Frame(scroll_frame, bg="white", height=60)
top.pack(fill=X)






search_var = StringVar()

search_entry = Entry(top, textvariable=search_var, width=40)
search_entry.pack(side=LEFT, padx=20, pady=10)

search_var.trace_add("write", lambda *args: search_items())

Button(top, text="Search",
       command=lambda: search_items()).pack(side=LEFT)



Label(scroll_frame, text="OUR MENU",
      font=("Segoe UI", 16, "bold"),
      bg="#f5f5f5").pack(anchor="w", padx=20, pady=10)


menu_frame = Frame(scroll_frame, bg="#f5f5f5")
menu_frame.pack(fill=X)

categories = ["All", "Burger", "Pizza", "Shake", "fries", "rolls"]

for cat in categories:
    Button(menu_frame,
           text=cat,
           padx=15, pady=5,
           command=lambda c=cat: show_items(c)
    ).pack(side=LEFT, padx=10)


# ================= DATA =================
cart = {}
favorites = []

food_data = {
    "All": [
        ("Burger", 150, r"C:\Users\LENOVO\Desktop\Secret-Veg-Cheeseburgers-c981dd6.jpg"),
        ("Pizza", 250, r"C:\Users\LENOVO\Desktop\images (1).jpeg"),
        ("Shake", 120, r"C:\Users\LENOVO\Desktop\Chocolate-Shake-4.jpg"),
        ("chees pizza",300, r"C:\Users\LENOVO\Desktop\Types-of-Pizza-Around-The-World-Must-try.jpg")
    ],
    "Burger": [
        ("aalu tikki Burger", 150, r"C:\Users\LENOVO\Desktop\Secret-Veg-Cheeseburgers-c981dd6.jpg"),
        ("dubble tikki",100,r"C:\Users\LENOVO\Desktop\images (6).jpeg"),
        ("chees burger",150,r"C:\Users\LENOVO\Desktop\91e241_5dd1ff99c86847e194fb905615f3a9c6~mv2.avif"),
        ("smash burger",160,r"C:\Users\LENOVO\Desktop\Image-6_-smash-burger-1024x538.png"),
        ("chees loded",120,r"C:\Users\LENOVO\Desktop\Image-1_-cheese-burger-1024x538.png"),
        ("extra vegies",110,r"C:\Users\LENOVO\Desktop\images (2).jpeg")
    ],
    "Pizza": [
        ("pepperoni Pizza", 250, r"C:\Users\LENOVO\Desktop\images (1).jpeg"),
        ("chees pizza",300, r"C:\Users\LENOVO\Desktop\Types-of-Pizza-Around-The-World-Must-try.jpg"),
        ("golden corn",250,r"C:\Users\LENOVO\Desktop\images (4).jpeg"),
        ("sicilian pizza",300,r"C:\Users\LENOVO\Desktop\Image-2_margherita-pizza-1024x538.png"),
        ("margarita chees",250,r"C:\Users\LENOVO\Desktop\images (5).jpeg")

    ],
    "Shake": [
        ("Shake", 120, r"C:\Users\LENOVO\Desktop\Chocolate-Shake-4.jpg")
    ],
    "fries":[
        ("chees loded",80,r"C:\Users\LENOVO\Desktop\Loaded-French-Fries.jpg"),
        ("french fries",50,r"C:\Users\LENOVO\Desktop\French-Fries_EXPS_FT23_40268_ST_0719_4.jpg"),
        ("ketchup fries",70,r"C:\Users\LENOVO\Desktop\IMG_8514-22.jpg")
    ],
    "rolls":[
        ("onion roll",100,r"C:\Users\LENOVO\Desktop\47825147783b1100a81d360a95b521fa.avif"),
        ("paneer roll",120,r"C:\Users\LENOVO\Desktop\fried-spring-rolls-cutting-board_1150-17010.avif"),
        ("mix vagie roll",150,r"C:\Users\LENOVO\Desktop\close-up-delicious-asian-food_23-2150535886.avif"),
        ("carrout,capsicum roll",200,r"C:\Users\LENOVO\Desktop\images (7).jpeg")
    ]
}



food_frame = Frame(scroll_frame, bg="#f5f5f5")
food_frame.pack(fill=BOTH, expand=True)


# ================= FUNCTIONS =================
def add_to_cart(name, price):
    if name in cart:
        cart[name]["qty"] += 1
    else:
        cart[name] = {"price": price, "qty": 1}
    update_cart()

def remove_from_cart(name):
    if name in cart:
        cart[name]["qty"] -= 1
        if cart[name]["qty"] <= 0:
            del cart[name]
    update_cart()

def update_cart():
    for w in right.winfo_children():
        w.destroy()

    Label(right, text="My Order",
          font=("Segoe UI", 16, "bold"),
          bg="white").pack(pady=20)

    total = 0

    for name, info in cart.items():
        price = info["price"] * info["qty"]
        total += price

        row = Frame(right, bg="white")
        row.pack(pady=5)

        Label(row, text=f"{name} x{info['qty']}",
              bg="white").pack(side=LEFT)

        Button(row, text="+", command=lambda n=name, p=info["price"]: add_to_cart(n, p)).pack(side=LEFT)
        Button(row, text="-", command=lambda n=name: remove_from_cart(n)).pack(side=LEFT)

        Label(row, text=f"₹{price}",
              bg="white").pack(side=RIGHT)

    Label(right, text="----------------", bg="white").pack()

    Label(right, text=f"Total ₹{total}",
          font=("Segoe UI", 14, "bold"),
          bg="white").pack(pady=10)

    Button(right, text="Checkout",
           bg="#1abc9c", fg="white",
           font=("Segoe UI", 12, "bold"),
           padx=20, pady=10,
           command=show_bill_section).pack(pady=20)


# ================= BILL SECTION =================
def show_bill_section():
    main.pack_forget()
    bill_frame.pack(fill=BOTH, expand=True)

    for w in bill_frame.winfo_children():
        w.destroy()

    Label(bill_frame, text="🧾 Bill",
          font=("Segoe UI", 20, "bold"),
          bg="white").pack(pady=20)

    total = 0

    for name, info in cart.items():
        price = info["price"] * info["qty"]
        total += price

        Label(bill_frame,
              text=f"{name} x{info['qty']} = ₹{price}",
              bg="white",
              font=("Segoe UI", 12)).pack()

    Label(bill_frame, text="----------------", bg="white").pack()

    Label(bill_frame,
          text=f"Total ₹{total}",
          font=("Segoe UI", 16, "bold"),
          fg="green",
          bg="white").pack(pady=10)

    Button(bill_frame,
           text="⬅ Back",
           bg="black", fg="white",
           command=back_to_main).pack(pady=10)

    Button(bill_frame,
           text="Download PDF",
           bg="#ff6b00", fg="white",
           command=generate_pdf).pack(pady=10)

    cart.clear()
    update_cart()


def back_to_main():
    bill_frame.pack_forget()
    main.pack(fill=BOTH, expand=True)


def generate_pdf():
    doc = SimpleDocTemplate("bill.pdf")
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Cafe Bill", styles['Title']))
    elements.append(Spacer(1, 10))

    total = 0

    for name, info in cart.items():
        price = info["price"] * info["qty"]
        total += price
        elements.append(Paragraph(f"{name} x{info['qty']} = ₹{price}", styles['Normal']))
        elements.append(Spacer(1, 5))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Total: ₹{total}", styles['Heading2']))

    doc.build(elements)


# ================= MAIN =================

dark_mode = False

def toggle_dark_mode():
    global dark_mode

    if not dark_mode:
        root.config(bg="#2c2c2c")
        main.config(bg="#2c2c2c")
        food_frame.config(bg="#2c2c2c")
        top.config(bg="#2c2c2c")
        right.config(bg="#1e1e1e")
        dark_mode = True
    else:
        root.config(bg="#f5f5f5")
        main.config(bg="#f5f5f5")
        food_frame.config(bg="#f5f5f5")
        top.config(bg="#f5f5f5")
        right.config(bg="white")
        dark_mode = False





menu_frame = Frame(scroll_frame, bg="#f5f5f5")
menu_frame.pack(fill=X)




Button(top,
       text="❤️",
       font=("Segoe UI", 16),
       bg="#f5f5f5",
       bd=0,
       cursor="hand2",
       command=lambda: show_items("Favorites")
).pack(side=RIGHT, padx=20)

Button(top,
       text="🌙 Dark Mode",
       command=toggle_dark_mode).pack(side=LEFT, padx=20)







def open_food_page(name, price, img_path):
    win = Toplevel(root)
    win.title(name)
    win.geometry("500x500")
    win.config(bg="white")

    try:
        img = Image.open(img_path)
    except:
        img = Image.new("RGB", (300, 250), "gray")

    img = img.resize((300, 250))
    img = ImageTk.PhotoImage(img)

    lbl = Label(win, image=img, bg="white")
    lbl.image = img
    lbl.pack(pady=20)

    Label(win, text=name,
          font=("Segoe UI", 18, "bold"),
          bg="white").pack()

    Label(win, text=f"₹{price}",
          font=("Segoe UI", 14),
          fg="green",
          bg="white").pack(pady=5)

    Button(win, text="Add to Cart",
           bg="#ff6b00", fg="white",
           font=("Segoe UI", 12, "bold"),
           command=lambda: add_to_cart(name, price)
           ).pack(pady=20)

    Button(win, text="Back",
           command=win.destroy).pack()

    favorites = []

    def toggle_favorite(name, price, img_path):
        item = (name, price, img_path)

        if item in favorites:
            favorites.remove(item)
        else:
            favorites.append(item)

        print("Favorites:", favorites)  # debug check



def create_food(name, price, img_path):
    card = Frame(food_frame,
                 bg=DARK_CARD if DARK else LIGHT_CARD,
                 bd=1, relief="solid")
    card.pack(side=LEFT, padx=10, pady=10)

    # 🔥 hover functions
    def on_enter(e):
        card.config(bg="#ffe0cc", bd=3)

    def on_leave(e):
        card.config(bg="white", bd=1)

    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)

    try:
        img = Image.open(img_path)
    except:
        img = Image.new("RGB", (150, 120), "gray")

    img = img.resize((150, 120))
    img = ImageTk.PhotoImage(img)

    lbl = Label(card, image=img, cursor="hand2")
    lbl.bind("<Button-1>", lambda e: open_food_page(name, price, img_path))
    lbl.image = img
    lbl.pack()

    lbl.bind("<Enter>", on_enter)
    lbl.bind("<Leave>", on_leave)

    name_lbl = Label(card, text=name, bg="white", cursor="hand2")
    name_lbl.pack()
    name_lbl.bind("<Button-1>", lambda e: open_food_page(name, price, img_path))

    Label(card,
          text=f"₹{price}",
          fg="green",
          bg=DARK_CARD if DARK else "white").pack()

    Button(card, text="Add",
           bg="#ff6b00", fg="white",
           command=lambda: add_to_cart(name, price)
           ).pack(pady=5)

    fav_btn = Button(card, text="🤍", bg="white", bd=0, font=("Segoe UI", 14))
    fav_btn.pack()

    def toggle():
        item = (name, price, img_path)

        if item in favorites:
            favorites.remove(item)
            fav_btn.config(text="🤍")  # empty heart
        else:
            favorites.append(item)
            fav_btn.config(text="❤️")  # filled heart

    fav_btn.config(command=toggle)




def show_items(category):
    for w in food_frame.winfo_children():
        w.destroy()

    if category == "Favorites":
        items = favorites
    else:
        items = food_data[category]

    for name, price, img in items:
        create_food(name, price, img)

def search_items():
    query = search_var.get().lower()

    for w in food_frame.winfo_children():
        w.destroy()

    if query == "":
        show_items("All")
        return

    shown = set()   # 🔥 duplicate rokne ke liye

    for category in food_data:
        for name, price, img in food_data[category]:
            if query in name.lower() and name not in shown:
                create_food(name, price, img)
                shown.add(name)


def toggle_dark_mode():
    global DARK
    DARK = not DARK

    if DARK:
        root.config(bg=DARK_BG)
        main.config(bg=DARK_BG)
        food_frame.config(bg=DARK_BG)
    else:
        root.config(bg=LIGHT_BG)
        main.config(bg=LIGHT_BG)
        food_frame.config(bg=LIGHT_BG)

    # refresh UI
    show_items("All")

    def toggle_favorite(name, price, img):
        item = (name, price, img)

        if item in favorites:
            favorites.remove(item)
        else:
            favorites.append(item)

        show_items("Favorites")

# ================= BILL FRAME =================
bill_frame = Frame(root, bg="white")

# ================= RIGHT =================
right = Frame(root, bg="white", width=150)
right.pack(side=RIGHT, fill=Y)

right.pack_propagate(False)

update_cart()
show_items("All")

root.mainloop()