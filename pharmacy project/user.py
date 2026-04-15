from tkinter import *
from tkinter import ttk
import pymysql as sql
from PIL import Image, ImageTk
from datetime import date
from datetime import date

import qty
cart = {}   # key = medicine name, value = [price, quantity]
top = Tk()
top.geometry("900x500")

header = Frame(top, bg="#2c3e50", height=60)
header.place(x=0, y=0, relwidth=1)

Label(header, text="🧑‍⚕️ User Pharmacy Panel",
      bg="#2c3e50", fg="white",
      font=('Arial', 18, 'bold')).place(x=20, y=10)



def search_data(event):
    value = search_entry.get().lower()

    tree.delete(*tree.get_children())

    db = sql.connect(host='localhost', user='root',
                     password='7983675531', database='test')
    cursor = db.cursor()

    cursor.execute("""
        SELECT name, brand, price, quantity, mfd, expd, discount, discount_expiry 
        FROM medicine
    """)
    rows = cursor.fetchall()

    for row in rows:
        name, brand, price, qty, mfd, expd, discount, dis_exp = row

        if value not in name.lower() and value not in brand.lower():
            continue

        if discount and discount > 0:
            final_price = price - (price * discount / 100)
        else:
            final_price = price

        status = "Out of Stock ❌" if qty <= 0 else "Available ✔"

        tree.insert('', END, values=(
            name, brand, price, qty, mfd, expd,
            discount, dis_exp, int(final_price), status
        ))

    db.close()

# ===== BACKGROUND IMAGE =====
bg_img = Image.open(r"C:\Users\LENOVO\Desktop\bright-blurry-background-depicting-pharmaceutical-260nw-2687888209.webp")   # <-- put your path here
bg_img = bg_img.resize((1500, 1000))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = Label(top, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

bg_label.image = bg_photo
bg_label.lower()   # 👈 IMPORTANT FIXheader = Frame(top, bg="#2c3e50", height=60)




search_entry = Entry( width=30, font=('Arial', 12))
search_entry.place(x=113, y=70)
top.update()              # 👈 FORCE RENDER
search_entry.lift()       # 👈 bring to front
search_entry.bind("<KeyRelease>", search_data)

def open_cart():
    def open_cart():
        cart_win = Toplevel(top)
        cart_win.geometry("500x400")
        cart_win.title("Cart")

        Label(cart_win, text="Your Cart",
              font=('Arial 18 bold')).pack(pady=10)







def search_data(event):
    value = search_entry.get().lower()
    tree.delete(*tree.get_children())

    db = sql.connect(host='localhost', user='root',
                     password='7983675531', database='test')
    cursor = db.cursor()

    cursor.execute("SELECT name, brand, price, quantity FROM medicine")
    rows = cursor.fetchall()

    for row in rows:
        name, brand = row[0], row[1]

        if value not in name.lower() and value not in brand.lower():
            continue

        tree.insert('', END, values=row)

    db.close()








# ===== VIEW FUNCTION =====
def view_data():
    db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
    cursor = db.cursor()

    cursor.execute("SELECT name, brand, price, quantity, mfd, expd, discount, discount_expiry FROM medicine")
    rows = cursor.fetchall()

    tree.delete(*tree.get_children())  # clean table

    for row in rows:
        name, brand, price, qty, mfd, expd, discount, dis_exp = row

        # discount logic
        if discount and discount > 0:
            discount_text = f"{discount}% OFF"
            final_price = price - (price * discount / 100)
        else:
            discount_text = "No Discount"
            final_price = price

        # 🟢 EXPIRY LOGIC (IMPORTANT)
        today = date.today()

        exp_date = expd if isinstance(expd, date) else date.fromisoformat(str(expd))

        if exp_date < today:
            tag = "expired"
            status = "Expired ❌"
        elif (exp_date - today).days <= 7:
            tag = "soon"
            status = "Expiring Soon ⚠"
        elif qty <= 0:
            tag = ""
            status = "Out of Stock ❌"
        else:
            tag = ""
            status = "Available ✔"

        # insert
        tree.insert('', END, values=(
            name,
            brand,
            price,
            qty,
            mfd,
            expd,
            discount_text,
            dis_exp,
            int(final_price),
            status
        ), tags=(tag,))

    db.close()




    if qty <= 0:
        tree.insert('', END, values=(name, brand, price, discount_text, int(final_price), status), tags=('out',))
    else:
        tree.insert('', END, values=(name, brand, price, discount_text, int(final_price), status))

        tree.tag_configure('out', background='lightcoral')


# ===== SEARCH FUNCTION =====
def search_data(event):
    value = search_entry.get().lower()
    tree.delete(*tree.get_children())
    ...
    value = search_entry.get().lower()

    # clear table
    tree.delete(*tree.get_children())

    db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
    cursor = db.cursor()

    cursor.execute("""
        SELECT name, brand, price, quantity, mfd, expd, discount, discount_expiry 
        FROM medicine
    """)
    rows = cursor.fetchall()

    for row in rows:
        name, brand, price, qty, mfd, expd, discount, dis_exp = row

        # LIVE FILTER (IMPORTANT PART)
        if value not in name.lower() and value not in brand.lower():
            continue

        # discount logic
        if discount and discount > 0:
            discount_text = f"{discount}% OFF"
            final_price = price - (price * discount / 100)
        else:
            discount_text = "No Discount"
            final_price = price

        status = "Out of Stock" if qty <= 0 else "Available"

        tree.insert('', END, values=(
            name,
            brand,
            price,
            qty,
            str(mfd),
            str(expd),
            discount_text,
            str(dis_exp),
            int(final_price),
            status
        ))

    db.close()
def buy_medicine():
        from tkinter import messagebox
        import pymysql as sql

        selected = tree.focus()

        if selected == "":
            messagebox.showerror("Error", "Select a medicine")
            return

        data = tree.item(selected, 'values')
        name = data[0]

        db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
        cursor = db.cursor()

        # current quantity check
        cursor.execute("SELECT quantity FROM medicine WHERE name=%s", (name,))
        qty = cursor.fetchone()[0]

        if qty <= 0:
            messagebox.showerror("Error", "Out of Stock ❌")
            db.close()
            return

        # reduce quantity
        cursor.execute("UPDATE medicine SET quantity = quantity - 1 WHERE name=%s", (name,))
        db.commit()
        db.close()

        final_price = tree.item(selected, 'values')[4]

        messagebox.showinfo("Bill", f"Medicine Purchased ✅\nAmount: ₹{final_price}")

        view_data() # refresh table



def add_to_cart():
    from tkinter import messagebox

    selected = tree.focus()

    if selected == "":
        messagebox.showerror("Error", "Select a medicine")
        return

    data = tree.item(selected, 'values')

    name = data[0]
    price = int(data[8])   # final price column (important)

    # 👉 if already in cart → increase quantity
    if name in cart:
        cart[name][1] += 1
    else:
        cart[name] = [price, 1]

    messagebox.showinfo("Success", f"{name} added to cart 🛒")







def generate_bill(cart_win, total):
    from tkinter import messagebox
    import pymysql as sql

    db = sql.connect(host='localhost', user='root',
                     password='7983675531', database='test')
    cursor = db.cursor()

    # 👉 update quantity properly
    for name, value in cart.items():
        qty = value[1]

        cursor.execute("""
            UPDATE medicine
            SET quantity = quantity - %s
            WHERE name = %s
        """, (qty, name))

    db.commit()
    db.close()

    messagebox.showinfo("Bill", f"Purchase Successful ✅\nTotal: ₹{total}")

    cart.clear()
    cart_win.destroy()
    view_data()




def toggle_select(event):
    item = tree.identify_row(event.y)

    if not item:
        return

    # prevent default selection conflict
    tree.after(1, lambda: None)

    if item in tree.selection():
        tree.selection_remove(item)
    else:
        tree.selection_set(item)



def open_cart():
    cart_win = Toplevel(top)
    cart_win.geometry("500x400")
    cart_win.title("Cart")

    Label(cart_win, text="Your Cart",
          font=('Arial 18 bold')).pack(pady=10)

    listbox = Listbox(cart_win, width=50, height=10)
    listbox.pack()

    total = 0

    for name, value in cart.items():
        price = value[0]
        qty = value[1]

        item_total = price * qty
        total += item_total

        listbox.insert(END, f"{name} x{qty} - ₹{item_total}")

    Label(cart_win, text=f"Total: ₹{total}",
          font=('Arial 14 bold')).pack(pady=10)

    Button(cart_win, text="Buy All",
           bg="green", fg="white",
           command=lambda: generate_bill(cart_win, total)).pack(pady=10)

    Button(cart_win, text="Close",
           command=cart_win.destroy).pack()

    def increase_qty(name):
        cart[name][1] += 1
        open_cart()  # refresh cart window

    def decrease_qty(name):
        if name in cart:
            cart[name][1] -= 1

            if cart[name][1] <= 0:
                del cart[name]
        open_cart()  # refresh cart window








# ===== TREEVIEW =====

tree = ttk.Treeview(top, columns=(
    'Name','Brand','Price','Quantity','MFD','EXPD','Discount','Discount Expiry','Final Price','Status'
), show='headings')

# ✅ HEADING ADD KAR
for col in ('Name','Brand','Price','Quantity','MFD','EXPD','Discount','Discount Expiry','Final Price','Status'):
    tree.heading(col, text=col)

# ✅ WIDTH
tree.column('Name', width=120)
tree.column('Brand', width=120)
tree.column('Price', width=80)
tree.column('Quantity', width=80)
tree.column('MFD', width=100)
tree.column('EXPD', width=100)
tree.column('Discount', width=80)
tree.column('Discount Expiry', width=120)

tree.place(x=115, y=100, width=1000, height=300)



Button(top, text="Add to Cart", command=add_to_cart,
       font=('Arial 14 bold'), bg='blue', fg='white').place(x=993, y=420)

Button(text="🛒 Cart",
       command=open_cart,
       bg="#27ae60", fg="white",
       font=('Arial', 14, 'bold')).place(x=885, y=422)





tree.bind("<Button-1>", toggle_select)

# ===== LOAD DATA =====
view_data()

top.mainloop()