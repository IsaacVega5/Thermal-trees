import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt

from services.process import temperature_from_pixel_color

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
    mask_list = self.master.mask_list
    image_list = self.master.images_list
    path = self.master.path
    
    if len(image_list) == 0:
      Messagebox.show_error(message="No hay imágenes cargadas", title='Aviso', parent=None, alert=True, buttons=["Aceptar:primary"])
      return
    if len(mask_list) == 0:
      Messagebox.show_error(message="No hay máscaras creadas", title='Aviso', parent=None, alert=True, buttons=["Aceptar:primary"])
      return
    
    mask_array_list = []
    for mask in mask_list:
      mask_array = np.zeros(mask["size"])
      figure = np.array(mask["vertices"])
      if len(mask["vertices"]) > 0:
        cv2.fillPoly(mask_array, [figure], 1)
      mask_array_list.append(mask_array)
      
    
    average_mask = np.zeros(mask_array_list[0].shape)
    for mask_array in mask_array_list:
      average_mask += mask_array
    average_mask /= len(mask_array_list)
    
    average_mask = np.where(average_mask >= 0.5, 1, 0)
    
    print(average_mask)
    
  
    plt.figure()
    plt.imshow(average_mask, cmap='gray')
    plt.show()
    
    for image in image_list:
      img = Image.open(path + "/" + image).convert('L')
      average_mask_img = Image.fromarray(average_mask * 255).convert('L').resize(img.size)
      
      img = np.array(img)
      average_mask_resized = np.array(average_mask_img) / 255
      average_mask_resized = np.where(average_mask_resized >= 0.5, 1, 0)

      values = img[average_mask_resized == 1]
      max = temperature_from_pixel_color(np.max(values))
      mean = temperature_from_pixel_color(np.mean(values))
      min = temperature_from_pixel_color(np.min(values))
      
      print(f"Max: {max}")
      print(f"Mean: {mean}")
      print(f"Min: {min}")
      print("-------------------------------------")
      
      

    # Show individual masks
