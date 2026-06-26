import tkinter as tk
import random
from tkinter import messagebox

def move_button(event):
    # الحصول على أبعاد الشاشة الحالية
    win_width = root.winfo_width()
    win_height = root.winfo_height()
    
    # الحصول على أبعاد زرار "لا"
    btn_width = btn_no.winfo_width()
    btn_height = btn_no.winfo_height()
    
    # حساب إحداثيات عشوائية جديدة للزرار
    new_x = random.randint(0, win_width - btn_width - 20)
    new_y = random.randint(0, win_height - btn_height - 20)
    
    # نقل الزرار للمكان الجديد
    btn_no.place(x=new_x, y=new_y)

def yes_clicked():
    # الرسالة اللي هتظهر لما توافق
    messagebox.showinfo("بحبك", "وأنا بموت فيكي يا ياسمين! ❤️\n- يوسف")
    root.destroy()

# إنشاء النافذة الرئيسية
root = tk.Tk()
root.title("طلب خاص جداً ❤️")
root.geometry("600x450")
root.configure(bg="#ffe6e6") # لون خلفية بمبي فاتح
root.resizable(False, False) # منع تغيير حجم الشاشة عشان الزرار ميهربش بره

# زينة القلوب
hearts_top = tk.Label(root, text="💖 💕 💖 💕 💖 💕 💖", bg="#ffe6e6", fg="#ff3366", font=("Helvetica", 24))
hearts_top.pack(pady=20)

# النص الرئيسي
question_text = "يا ياسمين، ممكن بوسة؟\n\n- حبيبك يوسف"
lbl_question = tk.Label(root, text=question_text, bg="#ffe6e6", fg="#cc0000", font=("Arial", 24, "bold"), justify="center")
lbl_question.pack(pady=30)

hearts_bottom = tk.Label(root, text="💞 💓 💞 💓 💞 💓 💞", bg="#ffe6e6", fg="#ff3366", font=("Helvetica", 24))
hearts_bottom.pack(pady=10)

# إنشاء زرار "أكيد"
btn_yes = tk.Button(root, text="أكيد ❤️", font=("Arial", 16, "bold"), bg="white", fg="red", width=10, command=yes_clicked)
btn_yes.place(x=150, y=300)

# إنشاء زرار "لا"
btn_no = tk.Button(root, text="لا 💔", font=("Arial", 16, "bold"), bg="white", fg="black", width=10)
btn_no.place(x=350, y=300)

# ربط حركة الماوس (Hover) بزرار "لا" عشان يهرب
btn_no.bind("<Enter>", move_button)

# تشغيل البرنامج
root.mainloop()