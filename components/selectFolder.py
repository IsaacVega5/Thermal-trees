import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class SelectFolder(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.pack(padx=0)

    self.master = master
    
    self.label = ttk.Label(self, text="Seleccionar carpeta", justify="left")
    self.label.grid(row=0, column=0, padx=0, pady=0, sticky=tk.W)
    
    self.entry = ttk.Entry(self, width=105)
    self.entry.insert(0, self.master.path)
    self.entry.config(state="readonly")
    self.entry.grid(row=1, column=0, padx=(0,5), pady=(0,5))

    self.button = ttk.Button(self, text="Seleccionar", command=self.selectFolder)
    self.button.grid(row=1, column=2, padx=0, pady=5)
    
  def selectFolder(self):
    folder = filedialog.askdirectory()
    self.entry.config(state="normal")
    self.entry.delete(0, tk.END)
    self.entry.insert(0, folder)
    self.entry.config(state="readonly")
    
    self.master.path = folder
    self.master.Images_list.read_folder()
    self.master.Entry_mask.values_set()