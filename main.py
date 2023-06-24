import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import scanversions
import setconfig
import mod_updater



def select_folder():
    global selected_folder, confirm_button, isolation_checkbox, folder_path, version_select_label
    folder_path = filedialog.askdirectory()
    if folder_path.endswith(".minecraft"):
        selected_folder = folder_path
        select_button.pack_forget()
        isolation_checkbox.pack(side=tk.LEFT, padx=10)
        confirm_button.config(state=tk.NORMAL)
    else:
        messagebox.showwarning("警告", "请选择名为'.minecraft'的文件夹！")
        confirm_button.config(state=tk.DISABLED)

def confirm_folder():
    global selected_folder, folder_path
    if folder_path is not None and folder_path.endswith(".minecraft"):
        setconfig.set_config("minecraft_folder", folder_path)
        setconfig.set_config("isolation_enabled", isolation_var.get())
        print("进度：确认完成")
        print("版本隔离已开启" if isolation_var.get() else "版本隔离未开启")
        versions = scanversions.get_versions(folder_path)
        combo_box.config(values=versions)
        for widget in [select_button, isolation_checkbox, confirm_button, version_select_label]:
            widget.pack_forget()
        version_label.config(text="")
        version_select_label.pack(side=tk.LEFT)
        combo_box.pack(side=tk.LEFT)

        wrapper_func = lambda path=folder_path: mod_updater.upgrade_mods(path)
        upgrade_button = tk.Button(frame, text="升级", command=wrapper_func)
        upgrade_button.pack(side=tk.LEFT, padx=10)

        version_frame.pack(side=tk.LEFT, padx=10)

    else:
        messagebox.showerror("错误", "你选择的文件夹不正确！")
        confirm_button.config(state=tk.DISABLED)


def on_select(event):
    global selected_version
    selected_version = event.widget.get()
    print(f"已选择版本：{selected_version}")

root = tk.Tk()
root.title("Minecraft_Mods_Updater")
root.geometry("500x100")
frame = tk.Frame(root)
frame.pack()

# 版本选择标签
version_select_label = tk.Label(frame, text="选择你的Minecraft版本：")

# 版本下拉框和文本框
version_frame = tk.Frame(frame)
version_label = tk.Label(version_frame, text="版本：")
version_label.pack(side=tk.LEFT)

combo_box = ttk.Combobox(version_frame, state="readonly")
combo_box.bind("<<ComboboxSelected>>", on_select)

selected_folder = setconfig.get_config("minecraft_folder") # 检测是否设置过文件夹
selected_version = setconfig.get_config("isolation_enabled")
if selected_folder is not None:
    selected_folder = selected_folder.strip("\"")
    if selected_folder.endswith(".minecraft"):
        selected_folder = selected_folder
        version_select_label.pack(side=tk.LEFT)
        versions = scanversions.get_versions(selected_folder)
        combo_box.config(values=versions)
        combo_box.pack(side=tk.LEFT)
        version_frame.pack(side=tk.LEFT, padx=10)
else:
    # 选择文件夹按钮
    select_button = tk.Button(frame, text="选择.minecraft文件夹", command=select_folder)
    select_button.pack(side=tk.LEFT, padx=10)
    confirm_button = tk.Button(frame, text="确认", width=10, height=2, state=tk.DISABLED, command=confirm_folder)
    confirm_button.pack(side=tk.LEFT)
    isolation_var = tk.BooleanVar()
    isolation_checkbox = tk.Checkbutton(frame, text="启用版本隔离", variable=isolation_var, onvalue=True, offvalue=False)
    isolation_checkbox.pack_forget()
    confirm_button.config(state=tk.DISABLED)

root.mainloop()