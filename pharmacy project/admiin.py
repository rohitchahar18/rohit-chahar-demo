from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
top = Tk()
top.geometry("600x500")



tree = ttk.Treeview(top, columns=(
    'Name',
    'Brand',
    'Price',
    'Quantity',
    'MFD',
    'EXPD',
    'Discount',
    'Discount Expiry',
    'Final Price',
    'Status'
), show='headings')



# ===== BACKGROUND IMAGE =====
bg_img = Image.open(r"C:\Users\LENOVO\Desktop\pngtree-pharmacy-drugstore-shop-interior-blur-background-image_15660282.jpg")   # <-- put your path here
bg_img = bg_img.resize((1500, 1000))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = Label(top, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

bg_label.image = bg_photo

selected_item = None

def on_select(event):
    global selected_item
    selected_item = tree.focus()



Label(top, text="Admin Panel", font=('Arial 20 bold')).grid(row=0, column=0, columnspan=2, pady=20)

# ===== LABEL + ENTRY (FORM STYLE) =====

Label(top, text="Medicine Name", font=('Arial 12 bold')).grid(row=1, column=0, padx=20, pady=5, sticky="w")
e1 = Entry(top, width=30, font=('Arial 12'))
e1.grid(row=1, column=1, pady=5)

Label(top, text="Brand", font=('Arial 12 bold')).grid(row=2, column=0, padx=20, pady=5, sticky="w")
e2 = Entry(top, width=30, font=('Arial 12'))
e2.grid(row=2, column=1, pady=5)

Label(top, text="Price", font=('Arial 12 bold')).grid(row=3, column=0, padx=20, pady=5, sticky="w")
e3 = Entry(top, width=30, font=('Arial 12'))
e3.grid(row=3, column=1, pady=5)

Label(top, text="Quantity", font=('Arial 12 bold')).grid(row=4, column=0, padx=20, pady=5, sticky="w")
e4 = Entry(top, width=30, font=('Arial 12'))
e4.grid(row=4, column=1, pady=5)



Label(top, text="MFD (YYYY-MM-DD)", font=('Arial 12 bold')).grid(row=6, column=0, padx=20, pady=5, sticky="w")
e5 = Entry(top, width=30, font=('Arial 12'))
e5.grid(row=6, column=1, pady=5)

Label(top, text="EXPIRY (YYYY-MM-DD)", font=('Arial 12 bold')).grid(row=7, column=0, padx=20, pady=5, sticky="w")
e6= Entry(top, width=30, font=('Arial 12'))
e6.grid(row=7, column=1, pady=5)

Label(top, text="Discount (%)", font=('Arial 12 bold')).grid(row=8, column=0, padx=20, pady=5, sticky="w")
e7 = Entry(top, width=30, font=('Arial 12'))
e7.grid(row=8, column=1, pady=5)

Label(top, text="Discount Expiry", font=('Arial 12 bold')).grid(row=9, column=0, padx=20, pady=5, sticky="w")
e8 = Entry(top, width=30, font=('Arial 12'))
e8.grid(row=9, column=1, pady=5)



def add_medicine():
    import pymysql as sql
    from tkinter import messagebox

    name = e1.get()
    brand = e2.get()
    price = e3.get()
    quantity = e4.get()
    mfd = e5.get()
    expd = e6.get()
    discount = e7.get()
    dis_exp = e8.get()

    # 👉 validation
    if name == "" or brand == "" or price == "" or quantity == "":
        messagebox.showerror("Error", "Fill required fields")
        return

    try:
        db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
        cursor = db.cursor()

        query = """
        INSERT INTO medicine 
        (name, brand, price, quantity, mfd, expd, discount, discount_expiry)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query, (
            name,
            brand,
            int(price),
            int(quantity),
            mfd,
            expd,
            int(discount) if discount else 0,
            dis_exp if dis_exp else None
        ))

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Medicine Added ✅")

        # 👉 clear fields
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)
        e8.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", str(e))



def view_data():
    import pymysql as sql

    db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
    cursor = db.cursor()

    cursor.execute("SELECT name, brand, price, quantity, mfd, expd, discount, discount_expiry FROM medicine")
    rows = cursor.fetchall()

    # clear old data
    for i in tree.get_children():
        tree.delete(i)

    # insert new data
    for row in rows:
        tree.insert('', END, values=row)

    db.close()




def get_data(event):
    selected = tree.focus()

    if selected == "":
        return

    data = tree.item(selected, 'values')

    e1.delete(0, END)
    e1.insert(0, data[0])

    e2.delete(0, END)
    e2.insert(0, data[1])

    e3.delete(0, END)
    e3.insert(0, data[2])

    e4.delete(0, END)
    e4.insert(0, data[3])

    e5.delete(0, END)
    e5.insert(0, data[4])

    e6.delete(0, END)
    e6.insert(0, data[5])

    e7.delete(0, END)
    e7.insert(0, data[6])

    e8.delete(0, END)
    e8.insert(0, data[7])






def update_data():
    import pymysql as sql
    from tkinter import messagebox

    selected = tree.focus()

    if selected == "":
        messagebox.showerror("Error", "Select a record")
        return

    name = e1.get()
    brand = e2.get()
    price = e3.get()
    quantity = e4.get()
    mfd = e5.get()
    expd = e6.get()
    discount = e7.get()
    dis_exp = e8.get()

    try:
        db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
        cursor = db.cursor()

        query = """
        UPDATE medicine 
        SET brand=%s, price=%s, quantity=%s, mfd=%s, expd=%s, discount=%s, discount_expiry=%s
        WHERE name=%s
        """

        cursor.execute(query, (
            brand,
            int(price),
            int(quantity),
            mfd,
            expd,
            int(discount) if discount else 0,
            dis_exp if dis_exp else None,
            name
        ))

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Updated ✅")
        view_data()

    except Exception as e:
        messagebox.showerror("Error", str(e))



def delete_data():
    import pymysql as sql
    from tkinter import messagebox

    selected = tree.focus()

    if selected == "":
        messagebox.showerror("Error", "Select a record")
        return

    data = tree.item(selected, 'values')
    name = data[0]

    try:
        db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
        cursor = db.cursor()

        cursor.execute("DELETE FROM medicine WHERE name=%s", (name,))

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Deleted ❌")
        view_data()

    except Exception as e:
        messagebox.showerror("Error", str(e))





def search_data():
    import pymysql as sql

    value = search_entry.get()

    if value == "":
        view_data()
        return

    db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
    cursor = db.cursor()

    query = """
    SELECT name, brand, price, quantity, mfd, expd, discount, discount_expiry 
    FROM medicine 
    WHERE name LIKE %s OR brand LIKE %s
    """

    cursor.execute(query, ('%' + value + '%', '%' + value + '%'))
    rows = cursor.fetchall()

    # clear table
    for i in tree.get_children():
        tree.delete(i)

    # insert filtered data
    for row in rows:
        tree.insert('', END, values=row)

    db.close()




def increase_stock():
    if not selected_item:
        return

    data = tree.item(selected_item, 'values')
    name = data[0]

    import pymysql as sql
    db = sql.connect(host='localhost', user='root',
                     password='7983675531', database='test')
    cursor = db.cursor()

    cursor.execute("""
        UPDATE medicine
        SET quantity = quantity + 1
        WHERE name = %s
    """, (name,))

    db.commit()
    db.close()

    view_data()

def decrease_stock():
    if not selected_item:
        return

    data = tree.item(selected_item, 'values')
    name = data[0]

    import pymysql as sql
    db = sql.connect(host='localhost', user='root',
                     password='7983675531', database='test')
    cursor = db.cursor()

    cursor.execute("""
        UPDATE medicine
        SET quantity = quantity - 1
        WHERE name = %s AND quantity > 0
    """, (name,))

    db.commit()
    db.close()

    view_data()



selected_item = None

def toggle_select(event):
    global selected_item

    item = tree.identify_row(event.y)

    if not item:
        return

    if item in tree.selection():
        tree.selection_remove(item)
        selected_item = None
    else:
        tree.selection_set(item)
        selected_item = item











search_entry = Entry(top, font=('Arial 12'), width=25)
search_entry.place(x=960, y=400)

search_entry.bind("<KeyRelease>", lambda event: search_data())



# ===== BUTTON =====
Button(top, text="Add Medicine", command=add_medicine,
       font=('Arial 12 bold'), width=15, bg='green', fg='white').place(x=150, y=400)


Button(top, text="Show Data", command=view_data,
       font=('Arial 12 bold'), width=15, bg='green', fg='white').place(x=1345, y=400)


Button(top, text="Update", command=update_data,
       font=('Arial 12 bold'), width=15, bg='blue', fg='white').place(x=320, y=400)

Button(top, text="Delete", command=delete_data,
       font=('Arial 12 bold'), width=15, bg='red', fg='white').place(x=490, y=400)


Button(top,height=0,text="Search", command=search_data,
       font=('Arial 8 bold')).place(x=1200, y=400)




#--------------------------------------------------------------------------------------------------------------------
## tree for grid box


from tkinter import ttk

tree = ttk.Treeview(top, columns=(
    'Name','Brand','Price','Qty','MFD','EXP','Discount','Dis Exp'
), show='headings')

# headings
for col in ('Name','Brand','Price','Qty','MFD','EXP','Discount','Dis Exp'):
    tree.heading(col, text=col)

    tree.column('Name', width=100)
    tree.column('Brand', width=100)
    tree.column('Price', width=80)
    tree.column('Qty', width=80)
    tree.column('MFD', width=100)
    tree.column('EXP', width=100)
    tree.column('Discount', width=80)
    tree.column('Dis Exp', width=120)

tree.place(x=15, y=460, width=1490, height=300)
tree.bind("<ButtonRelease-1>", get_data)

tree.bind("<<TreeviewSelect>>", on_select)

tree.bind("<Button-1>", toggle_select)

Button(top, text="➕",
       bg="silver", fg="white",
       command=increase_stock,
       font=('Arial', 8, 'bold')).place(x=48, y=760)

Button(top, text="➖",
       bg="sky blue", fg="white",
       command=decrease_stock,
       font=('Arial', 8, 'bold')).place(x=14, y=760)


top.mainloop()