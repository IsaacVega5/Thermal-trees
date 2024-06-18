import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random
from ttkbootstrap.dialogs import Messagebox

from windows.createMask import CreateMask

class EntryMask(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.pack(fill=tk.X)

    self.master = master
    self.mask_list = []
    
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
    if len(self.master.mask_list) > 0:
      msg = Messagebox.show_question(message="¿Seguro que desea crear nuevamente las máscaras?\nLa máscaras ya existentes se perderán", title='Aviso', parent=self.master, alert=True, buttons=['Cancelar:secondary', 'Aceptar:primary'])
      if msg == 'Cancelar':
        return
    
    self.master.mask_list = []
    self.master.Mask_list.update_masks()
    self.mask_list = []
    
    
    n_mask = int(float(self.entry.get()))
    images_list = self.master.images_list
    mask_list = [images_list[i] for i in random.sample(range(len(images_list)), n_mask)]
    
    for i in mask_list:
      try:
        if self.master.winfo_exists():  
          new_mask = CreateMask(self.master, path=(self.master.path + "/" + i), action=self.mask_list_set, total_masks=n_mask, current_mask=mask_list.index(i) + 1)
          self.wait_window(new_mask)
          self.master.mask_list = self.mask_list
          self.master.Mask_list.update_masks()
      except:
        return 

    
  
  def values_set(self):
    self.slider.config(from_=0, to=len(self.master.images_list))
    self.slider.set(20 if len(self.master.images_list) > 20 else len(self.master.images_list) // 3)
  
  def slider_changed(self, value):
    self.entry.delete(0, tk.END)
    self.entry.insert(0, int(float(value)))
    
  def mask_list_set(self, mask):
    self.mask_list.append(mask)

