import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import numpy as np
import cv2
from PIL import Image
import random

from windows.maskedHistogram import MaskedHistogram
from windows.resultTable import ResultTable
from components.progressBar import ProgressBar

from constants import TEMPERATURE_RANGE_METHODS
from utils import txt_to_array
from services.process import values_from_temperature_list

class Footer(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.pack(fill=tk.X, side=tk.BOTTOM)

    self.master = master
    self.data = []
    self.temp_ranges = []
    
    self.min_value = -30.5
    self.max_value = 24.4
    
    self.separator = ttk.Separator(self, orient=HORIZONTAL)
    self.separator.pack(side=tk.TOP, fill=tk.X, pady=(0,10))
    
    self.button = ttk.Button(self, text="Obtener t°C", command=self.get_temperature, style='success')
    self.button.pack(side=tk.RIGHT)
    
    self.selector = ttk.Combobox(self, width=15,values=TEMPERATURE_RANGE_METHODS, state="readonly", foreground="#4986ef", background="#ffffff", bootstyle="primary")
    self.selector.current(0)
    self.selector.pack(side=tk.LEFT, fill=tk.X, padx=5)
    
    self.n_range_entry = ttk.Entry(self, width=10, validate='key', validatecommand=(self.master.register(self.validate_int_numbers), '%P'))
    default_n_range_mask = 20 if len(self.master.images_list) > 20 else len(self.master.images_list) // 3
    self.n_range_entry.insert(0, default_n_range_mask)
    self.n_range_entry.pack(side=tk.LEFT, fill=tk.X, padx=5)
    
  
  def validate_int_numbers(self, value):
    if value.isdigit() or value == '':
        return True
    return False
  
  def validate_numbers(self, value):
    if value.isdigit() or value == '':
        return True
    if value.replace('.', '', 1).isdigit() and len(value.split('.')[1]) <= 2:
      return True
    if value[0] == '-' and value[1:].replace('.', '', 1).isdigit() and len(value.split('.')[1]) <= 2:
      return True
    return False
  
  def get_temperature(self):
    mask_list = self.master.mask_list
    image_list = self.master.images_list
    path = self.master.path
    method_name = self.selector.get()
    n_entry = int(float(self.n_range_entry.get()))
    
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
    
    
    self.data = []
    
    if method_name == 'Individual':
      for image in image_list:
        img = txt_to_array(path + "/" + image)
        height, width = img.shape
        average_mask_img = Image.fromarray(average_mask).convert('L').resize((width, height))
        
        masked_histogram = MaskedHistogram(
          master = self.master,
          path = str(path + "/" + image), 
          mask_vertex=average_mask_img,
          total_masks=len(image_list),
          current_mask=image_list.index(image),
          action=self.add_data)
        self.wait_window(masked_histogram)
    
    else:
      range_list = []
      if method_name == 'Primeros':
        range_list = image_list[:n_entry]
      elif method_name == 'Últimos':
        range_list = image_list[-n_entry:]
      elif method_name == 'Seleccionados':
        selected = self.master.Images_list.list.selection()
        if len(selected) == 0:
          Messagebox.show_error(message="No hay imágenes seleccionadas", title='Aviso', parent=None, alert=True, buttons=["Aceptar:primary"])
          return
        for item in selected:
          range_list.append(self.master.Images_list.list.item(item)['text'])
      else:
        range_list = [image_list[i] for i in random.sample(range(len(image_list)), n_entry)]
      
      self.temp_ranges = []
      for image in range_list:
        img = txt_to_array(path + "/" + image)
        height, width = img.shape
        average_mask_img = Image.fromarray(average_mask).convert('L').resize((width, height))
        
        masked_histogram = MaskedHistogram(
          master = self.master,
          path = str(path + "/" + image), 
          mask_vertex=average_mask_img,
          total_masks=len(range_list),
          current_mask=range_list.index(image),
          action=self.add_temp_ranges,
          action_type='range')
        
        self.wait_window(masked_histogram)
      
      if len(self.temp_ranges) > 0:
        average_min = sum([x[0] for x in self.temp_ranges]) // len(self.temp_ranges)
        average_max = sum([x[1] for x in self.temp_ranges]) // len(self.temp_ranges)
      else:
        average_min = float(self.min_entry.get())
        average_max = float(self.max_entry.get())
      
      master = self.master
      progress = ProgressBar(master, total=len(image_list))
      
      for index,image in enumerate(image_list):
        img = txt_to_array(path + "/" + image)
        height, width = img.shape
        average_mask_img = Image.fromarray(average_mask).convert('L').resize((width, height))
        
        average_mask_resized = np.array(average_mask_img)
        
        temperature_list = np.array([ pixel for pixel in img[average_mask_resized == 1].flatten()])
        filtered_temperature_list = [t for t in temperature_list if t >= average_min and t <= average_max]
       
        values = values_from_temperature_list(filtered_temperature_list)
        
        self.add_data({
          "img": path + "/" + image,
          "values": values
        })
        
        progress.update(index)
      
      progress.destroy()
      
      
    if len(self.data) > 0:
      ResultTable(self.master, self.data)

  def add_temp_ranges(self, range):
    self.temp_ranges.append(range)
  
  def add_data(self, new_data):
    self.data.append(new_data)
    
  def values_set(self):
    self.n_range_entry.delete(0, tk.END)
    self.n_range_entry.insert(0, 20 if len(self.master.images_list) > 20 else len(self.master.images_list) // 3)