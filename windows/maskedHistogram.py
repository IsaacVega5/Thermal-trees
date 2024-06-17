import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import numpy as np
from PIL import Image, ImageTk

import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from services.process import temperature_from_pixel_color


import cv2

class MaskedHistogram(ttk.Toplevel):
  def __init__(self, master, path, mask_vertex, total_masks, current_mask, action):
    super().__init__(master)
    x = self.master.winfo_x()
    y = self.master.winfo_y()
    self.geometry("+%d+%d" % (x + 100, y + 50))
    
    self.title(f'Histograma de la mascara {current_mask} de {total_masks}')
    self.master = master
    self.path = path
    self.action = action
    self.mask_vertex = mask_vertex
    self.temperature_list = []
    
    self.full_img = Image.open(path).convert('L')
    self.full_mask = Image.fromarray(mask_vertex).convert('L').resize(self.full_img.size)
    self.full_img = np.array(self.full_img)
    self.full_mask = np.array(self.full_mask)
    
    self.values = self.full_img[self.full_mask == 1]
    self.max = temperature_from_pixel_color(np.min(self.values))
    self.min = temperature_from_pixel_color(np.max(self.values))
    
    
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
    
    self.slider = ttk.Scale(self.tool_bar, from_=self.min, to=self.max, orient=HORIZONTAL, command=self.slider_change)
    self.slider.pack(side=tk.LEFT, padx=10, pady=10)
    
    self.save_btn = ttk.Button(self.tool_bar, text="Guardar", command=self.save_click)
    self.save_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    self.separator = ttk.Separator(self, orient=HORIZONTAL)
    self.separator.pack(side=tk.TOP, fill=tk.X, pady=(0,10))
    
    self.fig = Figure(figsize=(5, 4), dpi=100)
    self.fig.tight_layout()
    self.ax = self.fig.add_subplot(111)
    
    self.canvas = FigureCanvasTkAgg(self.fig, master=self)
    self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.canvas.draw()
    
    # self.masked_img_label = tk.Label(self, image=self.masked_img)
    # self.masked_img_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    self.canvas_masked_img = tk.Canvas(self, width=width, height=height)
    self.canvas_masked_img.create_image(0, 0, image=self.masked_img, anchor=tk.NW)
    self.canvas_masked_img.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    self.canvas_masked_img.bind("<ButtonRelease-1>", self.click_temperature)
    
    self.temperature_label = ttk.Label(self.canvas_masked_img, text="Temperatura: ", bootstyle="inverse-danger")
    
    self.temperature_label.place(x=2, y=2)
    
    self.protocol("WM_DELETE_WINDOW", self.on_destroy)
    
    self.resizable(False, False)
    self.data_from_img()
    self.set_temperature_pixel(width//2, height//2)
  
  def save_click(self):
    pass
  
  def on_destroy(self):
    self.destroy()
  
  def data_from_img(self):
    from tqdm import tqdm
    img = self.full_img
    mask = self.full_mask
    temperature_list = []
          
    for i in tqdm(range(img.shape[0])):
      for j in range(img.shape[1]):
        if mask[i][j] == 0:
          temperature_list.append(temperature_from_pixel_color(img[i][j]))
          
    self.temperature_list = temperature_list
    self.ax.hist(temperature_list, bins=100)
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
    self.canvas_masked_img.create_oval(x-3, y-3, x+3, y+3, fill="red")
  
  def slider_change(self, value):
    pass