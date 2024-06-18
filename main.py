import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from components.selectFolder import SelectFolder
from components.imagesList import ImagesList
from components.entryMask import EntryMask
from components.maskList import MaskList
from components.footer import Footer

root = ttk.Window( title="Thermal Trees", iconphoto = './assets/tree-blue.png')

root.iconphoto = './assets/tree-blue.png'


class App(ttk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.pack()
    self.config (
      padding=(10, 10),
    )
    
    self.path = ""
    self.images_list = []
    self.mask_list = []
    
    self.master = master
    self.Entry_folder = SelectFolder(self)
    self.Images_list = ImagesList(self)
    self.Entry_mask = EntryMask(self)
    self.Mask_list = MaskList(self)
    
    self.footer = Footer(self)
    
    root.resizable(False, False)


if __name__ == "__main__":
	app = App(root)
	app.mainloop()