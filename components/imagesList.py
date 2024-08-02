import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
from PIL import Image, ImageTk
from utils import txt_to_thermal
import numpy as np
import cv2

class ImagesList(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.pack(fill=tk.X, expand=True)

    self.master = master
    
    self.label = ttk.Label(self, text="Imágenes", justify="left", anchor="w")
    self.label.pack(side=tk.TOP, fill=tk.X)
    
    self.list_frame = ttk.Frame(self, style='secondary')
    self.list_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    self.img_prev_frame = ttk.Frame(self, style='secondary', height=150, width=150)
    self.img_prev_frame.pack(side=tk.RIGHT, fill=tk.X)
    
    self.scrollbar = ttk.Scrollbar(self.list_frame, style='primary')
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    self.list = ttk.Treeview(self.list_frame, height=10, yscrollcommand=self.scrollbar.set, selectmode="extended",show="tree")
    self.list.pack(side=tk.TOP, fill=tk.X)

    self.scrollbar.config(command=self.list.yview)
    
    
    self.three_img = ImageTk.PhotoImage(Image.open("./assets/tree-blue.png").resize((50, 50)))
    self.three_label = tk.Label(self.img_prev_frame, image=self.three_img, height=150, width=150)
    self.three_label.pack(side=tk.TOP, fill=tk.X)
    
    self.read_folder()
      

  def read_folder(self):
    path = self.master.path
    if not os.path.exists(path): return False
    image_list = []
    self.list.delete(*self.list.get_children())
    for file in os.listdir(path):
      if file.endswith(".txt"):
        self.list.insert("", tk.END, text=file, tags=(file,))
        self.list.bind("<ButtonRelease-1>", self.list_click)
        image_list.append(file)
    
    self.master.images_list = image_list

  def list_click(self, event):
    file = self.list.item(self.list.focus())['text']
    path = self.master.path + '/' + file
    img = ImageTk.PhotoImage(txt_to_thermal(path))
    self.three_label.configure(image=img)
    self.three_label.image = img
    pass