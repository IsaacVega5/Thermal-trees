import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class EntryMask(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.pack(fill=tk.X)

    self.master = master
    
    self.label = ttk.Label(self, text="Número de mascaras", justify="left", anchor="w")
    self.label.pack(side=tk.TOP, fill=tk.X)
    
  
    self.entry = ttk.Entry(self, width=10, validate='key', validatecommand=(self.master.register(self.validate_numbers), '%P'))
    self.entry.pack(side=tk.LEFT, fill=tk.X, padx=(0,5))
    
    self.slider = ttk.Scale(self, from_=0, to=len(self.master.images_list), orient=HORIZONTAL, command=self.slider_changed, length=560)
    default_value_mask = 20 if len(self.master.images_list) > 20 else len(self.master.images_list) // 3
    self.slider.set(default_value_mask)
    self.slider.pack(side=tk.LEFT, fill=tk.X, padx=5)
    
    self.button = ttk.Button(self, text="Crear", command=self.generate_masks)
    self.button.pack(side=tk.RIGHT)
    
  def validate_numbers(self, value):
    if value == '': 
      return True
    if value.isdigit() and int(value) <= len(self.master.images_list):
      self.slider.set(int(value))
      return True
    return False
  
  def generate_masks(self):
    pass
  
  def values_set(self):
    self.slider.config(from_=0, to=len(self.master.images_list))
    self.slider.set(20 if len(self.master.images_list) > 20 else len(self.master.images_list) // 3)
  
  def slider_changed(self, value):
    self.entry.delete(0, tk.END)
    self.entry.insert(0, int(float(value)))

