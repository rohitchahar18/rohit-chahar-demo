from tkinter import *
from tkinter import messagebox
import pymysql as sql
from PIL import Image, ImageTk

top = Tk()
top.geometry("450x350")
top.title("Login System")

# ===== BACKGROUND IMAGE =====
bg_img = Image.open(r"C:\Users\LENOVO\Desktop\pngtree-composition-of-medicine-bottles-and-pills-with-pharmacy-store-shelves-background-image_15651656.jpg")   # <-- put your path here
bg_img = bg_img.resize((1500, 1000))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = Label(top, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

bg_label.image = bg_photo


# ================= TITLE =================
# ================= TITLE =================
Label(top, text="LOGIN PANEL",
      font=('Arial', 24, 'bold'),
      fg="#222222",
      bg=top.cget("bg")).pack(pady=25)


# ================= USERNAME =================
Label(top, text="Username",
      font=('Arial', 12, 'bold'),
      fg="#444444",
      bg=top.cget("bg")).pack(pady=(10, 5))

e1 = Entry(top,
           font=('Arial', 15),
           width=28,
           bd=2,
           relief="flat",
           highlightthickness=2,
           highlightbackground="#cccccc",
           highlightcolor="#4CAF50")
e1.pack(pady=5)


# ================= PASSWORD =================
Label(top, text="Password",
      font=('Arial', 12, 'bold'),
      fg="#444444",
      bg=top.cget("bg")).pack(pady=(15, 5))

e2 = Entry(top,
           show="*",
           font=('Arial', 15),
           width=28,
           bd=2,
           relief="flat",
           highlightthickness=2,
           highlightbackground="#cccccc",
           highlightcolor="#4CAF50")
e2.pack(pady=5)

# ================= LOGIN FUNCTION =================
def login(role_type):
    user = e1.get()
    pas = e2.get()

    try:
        db = sql.connect(host='localhost', user='root', password='7983675531', database='test')
        cursor = db.cursor()

        cursor.execute("""
            SELECT * FROM login
            WHERE username=%s AND password=%s AND role=%s
        """, (user, pas, role_type))

        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", f"{role_type.capitalize()} login successful")
            top.destroy()

            if role_type == "admin":
                import admin
            else:
                import user
        else:
            messagebox.showerror("Error", f"Invalid {role_type} login")

        db.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= BUTTON FRAME (CENTER) =================
btn_frame = Frame(top)
btn_frame.pack(pady=20)

Button(btn_frame, text="User Login", font=('Arial', 14, 'bold'),
       width=12, command=lambda: login("user")).grid(row=0, column=0, padx=10)

Button(btn_frame, text="Admin Login", font=('Arial', 14, 'bold'),
       width=12, command=lambda: login("admin")).grid(row=0, column=1, padx=10)
#
top.mainloop()