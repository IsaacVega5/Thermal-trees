import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageDraw
import numpy as np

class CreateMask(ttk.Toplevel):
  def __init__(self, master, path):
    super().__init__(master)
    self.title("Crear mascara")
    self.master = master
    self.path = path
    
    self.vertices = []
    
    self.img = Image.open(path)
    width, height = self.img.size
    self.img = self.img.resize((500, int(height / width * 500)))
    
    self.tool_bar = ttk.Frame(self)
    self.tool_bar.pack(side=tk.TOP, fill=tk.X)
    
    self.undo_btn = ttk.Button(self.tool_bar, text="Deshacer")
    self.undo_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    self.clear_btn = ttk.Button(self.tool_bar, text="Limpiar", style='danger')
    self.clear_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    self.save_btn = ttk.Button(self.tool_bar, text="Guardar")
    self.save_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    self.separator = ttk.Separator(self, orient=HORIZONTAL)
    self.separator.pack(side=tk.TOP, fill=tk.X, pady=(0,10))
    
    self.img = ImageTk.PhotoImage(self.img)
    self.img_label = tk.Label(self, image=self.img)
    self.img_label.pack(side=tk.LEFT, fill=tk.X)
    self.img_label.bind("<Button-1>", self.on_img_click)
    
    self.mask = np.zeros((self.img.height(), self.img.width()))
    
    self.mask_img = Image.fromarray(self.mask * 255).convert('L')
    self.mask_img = ImageTk.PhotoImage(self.mask_img)
    self.mask_label = tk.Label(self, image=self.mask_img)
    self.mask_label.pack(side=tk.RIGHT, fill=tk.X)
    
  
  def on_img_click(self, event):
    x, y = event.x, event.y
    self.vertices.append((x, y))
    
    # TODO
    # Dibujar polígono en la imagen con los vertices de self.vertices
    
  
  # def on_img_click(self, event):
  #   x, y = event.x, event.y
  #   self.mask[y, x] = 1
  #   self.mask_img = ImageTk.PhotoImage(
  #       Image.fromarray(self.mask * 255).convert('L').point(lambda x: 255 if x > 0 else 0)
  #   )
  #   self.mask_label.configure(image=self.mask_img)
  #   self.mask_label.image = self.mask_img
    
    


    