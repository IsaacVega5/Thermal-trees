import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import numpy as np
from PIL import Image, ImageTk
from RangeSlider.RangeSlider import RangeSliderH 
from ttkbootstrap.dialogs import Messagebox

import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from services.process import temperature_from_pixel_color


import cv2

class MaskedHistogram(ttk.Toplevel):
  def __init__(self, master, path, mask_vertex, total_masks, current_mask, action, temperature):
    super().__init__(master)
    x = self.master.winfo_x()
    y = self.master.winfo_y()
    self.geometry("+%d+%d" % (x + 100, y + 50))
    
    self.title(f'Histograma de la mascara {current_mask +1} de {total_masks}')
    self.master = master
    self.path = path
    self.action = action
    self.mask_vertex = mask_vertex
    self.temperature_list = None
    self.bins_fig = 50
    self.temperature_range = [-30.5, 24.4]
    
    self.full_img = Image.open(path).convert('L')
    self.full_mask = Image.fromarray(mask_vertex).convert('L').resize(self.full_img.size)
    self.full_img = np.array(self.full_img)
    self.full_mask = np.array(self.full_mask)
    
    self.values = self.full_img[self.full_mask == 1]
    self.min, self.max = temperature
    
    self.img = Image.open(path)
    width, height = self.img.size
    self.img = self.img.resize((500, int(height / width * 500)))
    width, height = self.img.size
    
    self.mask = Image.fromarray(mask_vertex).convert('L').resize(self.img.size)
    self.mask = np.array(self.mask)
    
    self.masked_img = cv2.bitwise_and(np.array(self.img), np.array(self.img), mask=self.mask)
    self.masked_img = Image.fromarray(self.masked_img).convert('L')
      
    self.masked_img = ImageTk.PhotoImage(self.masked_img)
  
    self.tool_bar = ttk.Frame(self)
    self.tool_bar.pack(side=tk.TOP, fill=tk.X)
    
    self.min_value_entry = ttk.Entry(self.tool_bar, width=6, validate='key', validatecommand=(self.master.register(self.validate_numbers), '%P'))
    self.min_value_entry.pack(side=tk.LEFT, padx=10, pady=(10,5))
    self.max_value_entry = ttk.Entry(self.tool_bar, width=6, validate='key', validatecommand=(self.master.register(self.validate_numbers), '%P'))
        
    self.left_slider = tk.DoubleVar(value=self.min)
    self.right_slider = tk.DoubleVar(value=self.max)
    self.slider = RangeSliderH(self.tool_bar,
                               [self.left_slider, self.right_slider], 
                               min_val=self.min, max_val=self.max, padX = 2,
                               bar_color_outer="#4582ec",
                               bar_color_inner="#4582ec",
                               line_s_color="#4582ec",
                               line_color="#f8f9fa",
                               bar_radius=6,
                               show_value=False,
                               Height=25,
                               Width=350,
                               font_size=1,
                               step_size=0)
    self.slider.pack(side=tk.LEFT, padx=10, pady=3)
    self.max_value_entry.pack(side=tk.LEFT, padx=10, pady=(5, 10))
    
    self.save_btn = ttk.Button(self.tool_bar, text="Guardar", command=self.save_click)
    self.save_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    self.separator = ttk.Separator(self, orient=HORIZONTAL)
    self.separator.pack(side=tk.TOP, fill=tk.X, pady=(0,10))
    
    self.fig = Figure(figsize=(5, 4), dpi=100)
    self.fig.tight_layout()
    self.ax = self.fig.add_subplot(111)
    
    self.canvas = FigureCanvasTkAgg(self.fig, master=self)
    self.canvas.get_tk_widget().pack(side=tk.LEFT, expand=True)
    self.canvas.draw()
    
    self.canvas_masked_img = tk.Canvas(self, width=width, height=height)
    self.canvas_masked_img.create_image(0, 0, image=self.masked_img, anchor=tk.NW)
    self.canvas_masked_img.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=(47,5))
    self.canvas_masked_img.bind("<ButtonRelease-1>", self.click_temperature)
    
    self.temperature_label = ttk.Label(self.canvas_masked_img, text="Temperatura: ", bootstyle="inverse-danger")
    
    self.temperature_label.place(x=2, y=2)
    
    self.protocol("WM_DELETE_WINDOW", self.on_destroy)
    
    self.resizable(False, False)
    self.data_from_img()
    self.set_temperature_pixel(width//2, height//2)
    self.min_value_entry.insert(0, self.min)
    self.max_value_entry.insert(0, self.max)
    self.left_slider.trace_add('write', self.slider_change)
    self.right_slider.trace_add('write', self.slider_change)
  
  def save_click(self):
    min, max = float(self.min_value_entry.get()), float(self.max_value_entry.get())
    filtered_temperatures = [t for t in self.temperature_list if t >= min and t <= max]
    
    t_min = np.min(filtered_temperatures)
    t_max = np.max(filtered_temperatures)
    t_median = np.median(filtered_temperatures)
    std = np.std(filtered_temperatures)
    Tw = t_median - std * 2
    Td = t_median + std * 2
    
    # Temperatura promedio de valores entre tw y td
    temperature_list_tw_td = [t for t in filtered_temperatures if t >= Tw and t <= Td]
    Tc = np.mean(temperature_list_tw_td)
    
    cwsi = ( Tc - Tw ) / ( Td - Tw ) # <- indice térmico
    
    # Calcular la porosidad
    b1 = len(filtered_temperatures)
    b2 = len([t for t in filtered_temperatures if t <= Tw])
    b3 = len([t for t in filtered_temperatures if t >= Td])
    porosidad = (b1 - (b2 + b3)) * 100 / b1 
    
    values = {
      'min': t_min,
      'max': t_max,
      'median': t_median,
      'std': np.std(filtered_temperatures),
      'Tw': Tw,
      'Td': Td,
      'Tc': Tc,
      'CWSI': cwsi,
      'porosidad': porosidad
    }
    
    self.action({
      'img': self.path,
      'values': values
    })
    
    self.destroy()
  
  def on_destroy(self):
    msg = Messagebox.show_question(message="¿Seguro que desea cerrar la ventana?\nLos valores no se guardaran", title='Cerrar ventana', parent=self, alert=True, buttons=['Cancelar:secondary', 'Cerrar:primary'])
    if msg == 'Cancelar':
      return
    self.destroy()
  
  def data_from_img(self):
    img = self.full_img
    mask = self.full_mask
          
    temperature_list = np.array([temperature_from_pixel_color(pixel) for pixel in img[mask == 1].flatten()])
    self.temperature_list = temperature_list
    self.ax.hist(temperature_list, bins=self.bins_fig, color="#4582ec")
    self.canvas.draw()
  def click_temperature(self, event):
    x, y = event.x, event.y
    self.set_temperature_pixel(x, y)
  
  def set_temperature_pixel(self, x, y):
    if self.mask[y][x] == 0: return
    self.dot_draw(x, y)
    img = Image.open(self.path).convert('L')
    width, height = self.img.size
    img = self.img.resize((500, int(height / width * 500)))
    img = np.array(img)
    pixel = img[y][x][0]
    temperature = temperature_from_pixel_color(pixel)
    self.temperature_label.configure(text=f"Temperatura: {temperature}°C")
    
  def dot_draw(self, x, y):
    self.canvas_masked_img.delete('all')
    self.canvas_masked_img.create_image(0, 0, image=self.masked_img, anchor=tk.NW)
    self.canvas_masked_img.create_oval(x-3, y-3, x+3, y+3, fill="#d9534f")
  
  def slider_change(self, trace, add, remove):
    self.min_value_entry.delete(0, tk.END)
    self.min_value_entry.insert(0, round(self.left_slider.get(), 2))
    self.max_value_entry.delete(0, tk.END)
    self.max_value_entry.insert(0, round(self.right_slider.get(), 2))
    
    self.update_histogram()
    
  def validate_numbers(self, value):
    if value.isdigit() or value == '':
      self.update_histogram()
      return True
    if value.replace('.', '', 1).isdigit():
      self.update_histogram()
      return True
    if value[0] == '-' or value[1:].replace('.', '', 1).isdigit():
      self.update_histogram()
      return True
    return False

  def update_histogram(self):
    self.update_histogram_cancel()
    self.update_histogram_task = self.master.after(500, self.update_histogram_perform)
    
  def update_histogram_perform(self):
    if self.temperature_list is None: return
    min, max = float(self.min_value_entry.get()), float(self.max_value_entry.get())
    new_temperature_list = [t for t in self.temperature_list if t >= min and t <= max]
    self.ax.clear()
    self.ax.hist(new_temperature_list, bins=self.bins_fig, color="#4582ec")
    self.canvas.draw()
    
  def update_histogram_cancel(self):
    try:
      self.master.after_cancel(self.update_histogram_task)
    except:
      pass
    self.update_histogram_task = None
  