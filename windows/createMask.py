import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import cv2  

class CreateMask(ttk.Toplevel):
  def __init__(self, master, path, action, total_masks, current_mask):
    super().__init__(master)
    x = self.master.winfo_x()
    y = self.master.winfo_y()
    self.geometry("+%d+%d" % (x + 100, y + 50))
    
    self.title(f'Mascara {current_mask} de {total_masks}')
    self.master = master
    self.path = path
    self.action = action
    self.vertices = []
    
    self.img = Image.open(path)
    width, height = self.img.size
    self.img = self.img.resize((500, int(height / width * 500)))
    
    self.tool_bar = ttk.Frame(self)
    self.tool_bar.pack(side=tk.TOP, fill=tk.X)
    
    self.undo_btn = ttk.Button(self.tool_bar, text="Deshacer", command=self.undo_click)
    self.undo_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    self.clear_btn = ttk.Button(self.tool_bar, text="Limpiar", style='danger', command=self.clear_click)
    self.clear_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    self.save_btn = ttk.Button(self.tool_bar, text="Guardar", command=self.save_click)
    self.save_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    self.separator = ttk.Separator(self, orient=HORIZONTAL)
    self.separator.pack(side=tk.TOP, fill=tk.X, pady=(0,10))
    
    self.img = ImageTk.PhotoImage(self.img)
    self.img_canvas = tk.Canvas(self, width=self.img.width(), height=self.img.height())
    self.img_canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
    self.img_canvas.pack(side=tk.LEFT, fill=tk.X)
    self.img_canvas.bind("<Button-1>", self.on_img_click)
    
    self.mask = np.zeros((self.img.height(), self.img.width()))
    
    self.mask_img = Image.fromarray(self.mask * 255).convert('L')
    self.mask_img = ImageTk.PhotoImage(self.mask_img)
    self.mask_label = tk.Label(self, image=self.mask_img)
    self.mask_label.pack(side=tk.RIGHT, fill=tk.X)
    
    
    self.bind("<Control-z>", self.ctr_z)
    self.protocol("WM_DELETE_WINDOW", self.on_destroy)
    
    self.resizable(False, False)
    
    
  def save_click(self):
    mask = {
      "size" : self.mask.shape,
      "vertices" : self.vertices
    }
    
    self.action(mask)
    
    self.destroy()
  
  def on_img_click(self, event):
    x, y = event.x, event.y
    self.vertices.append((x, y))
      
    self.draw_img_polygon()
    self.draw_mask_polygon()
    
  def undo_click(self):
    self.undo_polygons()
  
  def ctr_z(self,event):
    self.undo_polygons()
  
  def clear_click(self):
    self.vertices = []
    self.draw_img_polygon()
    self.draw_mask_polygon()
  
  def undo_polygons(self):
    if len(self.vertices) <= 0:
      return
    self.vertices.pop()
    self.draw_img_polygon()
    self.draw_mask_polygon()
  
  def draw_img_polygon(self):
    #Limpiamos el canvas
    self.img_canvas.delete('all')
    self.img_canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
    
    # Dibujar polígono en la imagen con los vertices de self.vertices
    for vertex in self.vertices:
        x, y = vertex
        self.img_canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='red')
        
    if len(self.vertices) <= 1: 
      return
    
    self.img_canvas.create_polygon(self.vertices, fill='red', outline='red', stipple='gray50')
    
  
  def draw_mask_polygon(self):
    mask = np.zeros((self.img.height(), self.img.width()))
    figure = np.array([self.vertices])
    
    if len(self.vertices) > 0:
      cv2.fillPoly(mask, [figure], 1)
    
    self.mask = mask
    self.mask_img = Image.fromarray(self.mask * 255).convert('L')
    self.mask_img = ImageTk.PhotoImage(self.mask_img)
    self.mask_label.configure(image=self.mask_img)
    self.mask_label.image = self.mask_img
    
  def on_destroy(self):
    msg = Messagebox.show_question(message="¿Seguro que desea cerrar la ventana?\nLa mascara no se guardará", title='Cerrar ventana', parent=None, alert=True, buttons=['Cancelar:secondary', 'Cerrar:primary'])
    if msg == 'Cancelar':
      return
    self.destroy()