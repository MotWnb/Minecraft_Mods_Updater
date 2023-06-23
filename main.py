import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

def select_folder():
    folder_path = filedialog.askdirectory()
    if os.path.basename(folder_path) == ".minecraft":
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, folder_path)
        confirm_button.config(state=tk.NORMAL)
        print("进度：完成.minecraft文件夹选择")
    else:
        messagebox.showwarning("警告", "请选择名为'.minecraft'的文件夹！")
        confirm_button.config(state=tk.DISABLED)

def confirm_folder():
    if os.path.basename(text_box.get("1.0", tk.END).strip()) == ".minecraft":
        print("进度：确认完成")
        for widget in [select_button, confirm_button, text_box]:
            widget.pack_forget()
    else:
        messagebox.showerror("错误", "你选择的文件夹不正确！")

root = tk.Tk()
root.title("Mod版本升级工具")
root.iconbitmap("res/Anvil_1.ico")
root.geometry("800x450")
root.minsize(400, 225)
root.maxsize(1600, 900)
root.resizable(True, True)

frame = tk.Frame(root)
frame.pack(pady=10)

text_box = tk.Text(frame, height=1, width=50)
text_box.pack(side=tk.LEFT)

select_button = tk.Button(frame, text="选择.minecraft文件夹", width=20, height=2, command=select_folder)
select_button.pack(side=tk.LEFT, padx=10)

confirm_button = tk.Button(frame, text="确认", width=10, height=2, state=tk.DISABLED, command=confirm_folder)
confirm_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()
