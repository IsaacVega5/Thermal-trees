import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import numpy as np
from PIL import Image, ImageTk
import cv2

class MaskList(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.config(
      padding=(0,10),
    )
    self.pack(fill=tk.X, expand=True)

    self.master = master
    self.label = ttk.Label(self, text="Máscaras", justify="center")
    self.label.pack(side=tk.TOP)
    
    self.mask_list_frame = ScrolledFrame(self, height=150, s_bootstyle="primary")
    self.mask_list_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
    self.mask_imgs = []
  
  def update_masks(self):
    self.mask_imgs = []
    mask_list = self.master.mask_list
    if len(self.mask_list_frame.winfo_children()) > 0:
      for widget in self.mask_list_frame.winfo_children():
        widget.destroy()
        
    for mask in mask_list:
      mask_img = np.zeros(mask["size"])
      height, width = mask["size"]
      figure = np.array(mask["vertices"])
      if len(mask["vertices"]) > 0:
        cv2.fillPoly(mask_img, [figure], 1)
      
      mask_img = Image.fromarray(mask_img * 255).convert('L')
      mask_img = mask_img.resize((100, int(height / width * 100)))
      mask_img = ImageTk.PhotoImage(mask_img)
      self.mask_imgs.append(mask_img)
    
    column = 0
    row = 0
    for img in self.mask_imgs:
      mask_label = ttk.Label(self.mask_list_frame, image=img)
      # mask_label.pack(side=tk.LEFT, fill=tk.X)
      mask_label.grid(row=row, column=column, padx=5, pady=5)
      column += 1
      if column >= 6:
        column = 0
        row += 1
    