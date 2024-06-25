import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ProgressBar(ttk.Frame):
  def __init__(self, master, total):
    super().__init__(master, padding=(5, 5))
    self.place(relx=0.5, rely=0.5, anchor="center")
    self.master = master
    
    self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
    self.progress.pack()
    
    self.progress['maximum'] = total
    self.progress['value'] = 0
    
    self.percentage = ttk.Label(self, text="0%")
    self.percentage.pack()
  
  def update(self, value):
    self.progress['value'] = value
    self.percentage['text'] = f"{int(value / self.progress['maximum'] * 100)}%"
    self.master.update()