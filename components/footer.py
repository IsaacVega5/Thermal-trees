import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Footer(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.pack(fill=tk.X, side=tk.BOTTOM)

    self.master = master
    
    self.min_value = -30.5
    self.max_value = 24.4
    
    self.separator = ttk.Separator(self, orient=HORIZONTAL)
    self.separator.pack(side=tk.TOP, fill=tk.X, pady=(0,10))
    
    
    self.min_entry = ttk.Entry(self, width=10, validate='key', validatecommand=(self.master.register(self.validate_numbers), '%P'))
    self.min_entry.insert(0, self.min_value)
    self.min_entry.pack(side=tk.LEFT, fill=tk.X, padx=(0,5))
    
    self.label = ttk.Label(self, text="-", justify="left", anchor="w")
    self.label.pack(side=tk.LEFT, fill=tk.X)
    
    self.max_entry = ttk.Entry(self, width=10, validate='key', validatecommand=(self.master.register(self.validate_numbers), '%P'))
    self.max_entry.insert(0, self.max_value)
    self.max_entry.pack(side=tk.LEFT, fill=tk.X, padx=5)
    
    self.button = ttk.Button(self, text="Obtener t°C", command=self.get_temperature, style='success')
    self.button.pack(side=tk.RIGHT)
    
    
  
  def validate_numbers(self, value):
    if value.isdigit() or value == '':
      return True
    if value.replace('.', '', 1).isdigit():
      return True
    if value[0] == '-':
      return True
    return False
  
  def get_temperature(self):
    pass