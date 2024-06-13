import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MaskList(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.config(
      padding=(0,10),
    )
    self.pack(fill=tk.X, expand=True)

    self.master = master
    self.label = ttk.Label(self, text="Mascaras", justify="left", anchor="w")
    
    self.mask_list_frame = ttk.Treeview(self, height=10, selectmode="extended",show="tree")
    self.mask_list_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    self.scrollbar = ttk.Scrollbar(self, command=self.mask_list_frame.yview)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    self.mask_list_frame.configure(yscrollcommand=self.scrollbar.set)
    