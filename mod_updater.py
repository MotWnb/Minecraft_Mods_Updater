import tkinter as tk
from tkinter import filedialog, messagebox

def select_folder(text_box, confirm_button, isolation_checkbox):
    folder_path = filedialog.askdirectory()
    if folder_path.endswith(".minecraft"):
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, folder_path)
        confirm_button.config(state=tk.NORMAL)
        isolation_checkbox.pack(side=tk.LEFT, padx=10)
    else:
        messagebox.showwarning("警告", "请选择名为'.minecraft'的文件夹！")
        confirm_button.config(state=tk.DISABLED)
        isolation_checkbox.pack_forget()

def confirm_folder(text_box, isolation_var):
    if text_box.get("1.0", tk.END).strip().endswith(".minecraft"):
        print("进度：确认完成")
        print("版本隔离已开启" if isolation_var.get() else "版本隔离未开启")
    else:
        messagebox.showerror("错误", "你选择的文件夹不正确！")
