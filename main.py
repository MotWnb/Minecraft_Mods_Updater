import tkinter as tk
from tkinter import filedialog, messagebox
from mod_updater import select_folder, confirm_folder

# 创建GUI
root = tk.Tk()
root.title("Mod版本升级工具")
root.iconbitmap("res/Anvil_1.ico")
root.geometry("800x450")
root.minsize(400, 225)
root.resizable(True, True)

# 创建GUI组件
frame = tk.Frame(root)
frame.pack(pady=10)
text_box = tk.Text(frame, height=1, width=50)
text_box.pack(side=tk.LEFT)
isolation_var = tk.BooleanVar(value=False)
isolation_checkbox = tk.Checkbutton(frame, text="是否开启版本隔离", variable=isolation_var)
tk.Button(frame, text="选择.minecraft文件夹", width=20, height=2, command=lambda: select_folder(text_box, confirm_button, isolation_checkbox)).pack(side=tk.LEFT, padx=10)
confirm_button = tk.Button(frame, text="确认", width=10, height=2, state=tk.DISABLED, command=lambda: confirm_folder(text_box, isolation_var, frame))
confirm_button.pack(side=tk.RIGHT, padx=10)

# 进入主循环
root.mainloop()
