import os
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar

def Decrypt(data: bytes) -> bytes:
    str_to_find = b'UnityFS'
    start = data.find(str_to_find, data.find(str_to_find)+1) 
    return data[start:]

def read_files(folder_label, current_file_label, progress):
    folder_path = filedialog.askdirectory()
    folder_label.config(text=f"AB包文件夹: {folder_path}")
    files = os.listdir(folder_path)
    progress['maximum'] = len(files)
    
    for i, file_name in enumerate(files):
        current_file_label.config(text=f"当前文件: {file_name}")
        try:
            with open(os.path.join(folder_path, file_name), 'rb') as f:
                data = f.read()
            if data[0:7].decode() != "UnityFS" : continue
            decrypted_data = Decrypt(data)
            try:
                os.makedirs('output', exist_ok=True)
                with open(f'output/{os.path.basename(file_name)}', 'wb') as output_file:
                    output_file.write(decrypted_data)
                progress.step()
            except Exception as e:
                current_file_label.config(text=f"无法将文件写入'output'目录: {e}")
                return
        except Exception as e:
            current_file_label.config(text=f"无法打开文件{file_name}: {e}")
            return
    current_file_label.config(text="处理完成.")

def start_read_files_thread(folder_label, current_file_label, progress):
    thread = threading.Thread(target=read_files, args=(folder_label, current_file_label, progress), daemon=True)
    thread.start()

def main():
    root = tk.Tk()
    root.title("交错战线 AssetBundle 解密器 By: Sakura Nyoru 2024-1-8")
    root.geometry("800x300")
    
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor='center')
    
    folder_label = tk.Label(frame, text="AB包文件夹:")
    current_file_label = tk.Label(frame, text="当前处理文件:")
    button = tk.Button(frame, text="选择AB包文件目录", command=lambda: start_read_files_thread(folder_label, current_file_label, progress))
    progress = Progressbar(frame, orient = 'horizontal', length = 300, mode = 'determinate')
    
    button.grid(row=0, column=0)
    folder_label.grid(row=1, column=0)
    current_file_label.grid(row=2, column=0)
    progress.grid(row=3, column=0)
    
    root.mainloop()

if __name__ == "__main__":
    main()
