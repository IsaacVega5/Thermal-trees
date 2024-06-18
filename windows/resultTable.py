import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
import xlsxwriter
import os

from utils import get_name_from_path

class ResultTable(ttk.Toplevel):
  def __init__(self, master, data):
    super().__init__(master)
    x = self.master.winfo_x()
    y = self.master.winfo_y()
    self.geometry("+%d+%d" % (x + 100, y + 50))
    self.title('Resultados')
    self.master = master
    
    self.data = [{'img': 'C:/Users/Usuario/Desktop/DataSet/Arboles/Imagenes blanco y '
         'negro/IR_06255.tif',
  'values': {'CWSI': 0.45998206605321107,
             'Tc': 12.337622808534183,
             'Td': 35.71501038171191,
             'Tw': -7.5750103817119125,
             'max': 18.8,
             'median': 14.07,
             'min': -26.84,
             'porosidad': -100.0,
             'std': 10.822505190855956}},
 {'img': 'C:/Users/Usuario/Desktop/DataSet/Arboles/Imagenes blanco y '
         'negro/IR_06256.tif',
  'values': {'CWSI': 0.4853050215204277,
             'Tc': 6.967581001051502,
             'Td': 14.40760496872397,
             'Tw': -0.04760496872397102,
             'max': 9.98,
             'median': 7.18,
             'min': -19.95,
             'porosidad': -100.0,
             'std': 3.6138024843619854}},
 {'img': 'C:/Users/Usuario/Desktop/DataSet/Arboles/Imagenes blanco y '
         'negro/IR_06257.tif',
  'values': {'CWSI': 0.46158504177787907,
             'Tc': 11.79851868174552,
             'Td': 34.524816890322185,
             'Tw': -7.684816890322187,
             'max': 18.8,
             'median': 13.42,
             'min': -24.9,
             'porosidad': -100.0,
             'std': 10.552408445161094}},
 {'img': 'C:/Users/Usuario/Desktop/DataSet/Arboles/Imagenes blanco y '
         'negro/IR_06258.tif',
  'values': {'CWSI': 0.5361742656512146,
             'Tc': 1.4555216353974623,
             'Td': 5.37291413381053,
             'Tw': -3.07291413381053,
             'max': 9.98,
             'median': 1.15,
             'min': 0.07,
             'porosidad': -100.0,
             'std': 2.111457066905265}},
 {'img': 'C:/Users/Usuario/Desktop/DataSet/Arboles/Imagenes blanco y '
         'negro/IR_06259.tif',
  'values': {'CWSI': 0.46286644244649694,
             'Tc': 3.6880077100597912,
             'Td': 19.917524889362024,
             'Tw': -10.297524889362023,
             'max': 9.98,
             'median': 4.81,
             'min': -19.95,
             'porosidad': -100.0,
             'std': 7.553762444681012}}]
    self.saved = False
    for i in range(20):
        import random
        self.data.append({
          'img': f'C:/Users/Usuario/Desktop/DataSet/Arboles/Imagenes blanco y negro/IR_0625{i+10}.tif',
          'values': {'CWSI': random.uniform(0.4, 0.6),
                      'Tc': random.uniform(1.0, 15.0),
                      'Td': random.uniform(30.0, 50.0),
                      'Tw': random.uniform(-5.0, 5.0),
                      'max': random.uniform(9.0, 19.0),
                      'median': random.uniform(1.0, 15.0),
                      'min': random.uniform(-20.0, -5.0),
                      'porosidad': -100.0,
                      'std': random.uniform(3.0, 10.0)}
        })
    
    self.tool_bar = ttk.Frame(self)
    self.tool_bar.pack(side=tk.TOP, fill=tk.X)
    
    self.save_btn = ttk.Button(self.tool_bar, text="Guardar", command=self.save) 
    self.save_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    self.separator = ttk.Separator(self, orient=HORIZONTAL)
    self.separator.pack(side=tk.TOP, fill=tk.X, pady=(0,10))
    
    self.colData = [
      {"text": "Imagen", "stretch": True},
      {"text": "Min", "stretch": True},
      {"text": "Max", "stretch": True},
      {"text": "Median", "stretch": True},
      {"text": "DS", "stretch": True},
      {"text": "Tw", "stretch": True},
      {"text": "Td", "stretch": True},
      {"text": "Tc", "stretch": True},
      {"text": "CWSI", "stretch": True},
      {"text": "Porosidad", "stretch": True},
    ]
    
    self.rowData = []
    for row in self.data:
      self.rowData.append((
        get_name_from_path(row["img"]),
        row["values"]["min"],
        row["values"]["max"],
        row["values"]["median"],
        row["values"]["std"],
        row["values"]["Tw"],
        row["values"]["Td"],
        row["values"]["Tc"],
        row["values"]["CWSI"],
        row["values"]["porosidad"],
      ))
    
    self.table = Tableview(
      master=self,
      coldata=self.colData,
      rowdata=self.rowData,
      paginated=True,
      searchable=True,
      bootstyle=PRIMARY,
      autofit=True
    )
    self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    self.resizable(True, True)
    
    self.protocol("WM_DELETE_WINDOW", self.on_destroy)
  
  def save(self):
    destiny_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", ".xlsx")])
  
    if destiny_path is None or destiny_path == '':
      return  
    
    workBook = xlsxwriter.Workbook(destiny_path)
    worksheet = workBook.add_worksheet()
    
    bold = workBook.add_format({'bold': True})
    
    worksheet.write("A1", "Imagen", bold)
    worksheet.write("B1", "Min", bold)
    worksheet.write("C1", "Max", bold)
    worksheet.write("D1", "Median", bold)
    worksheet.write("E1", "DS", bold)
    worksheet.write("F1", "Tw", bold)
    worksheet.write("G1", "Td", bold)
    worksheet.write("H1", "Tc", bold)
    worksheet.write("I1", "CWSI", bold)
    worksheet.write("J1", "Porosidad", bold)
    
    for i, row in enumerate(self.rowData):
      for j, value in enumerate(row):
        worksheet.write(i+1, j, value)
    
    saved = False
    while not saved:
      try:
        workBook.close()
        saved = True
      except:
        msg = Messagebox.show_error(
          title="Error",
          message = "El archivo ya se encuentra abierto.\nPor favor cierre el archivo y reintente.",
          parent=self,
          alert=True,
          buttons=['Cancelar:secondary', 'Reinentar:primary']
        )
        if msg == 'Cancelar':
          return
    
    self.saved = True
    msg = Messagebox.show_question(
      title="Guardado",
      message = f"Se guardo el archivo {destiny_path}",
      parent=self,
      alert=True,
      buttons=['Aceptar:secondary', 'Abrir:primary']
    )
    if msg == 'Abrir':
      os.startfile(destiny_path)
      
  def on_destroy(self):
    if not self.saved:
      msg = Messagebox.show_question(
        title="¿Desea guardar?",
        message = "¿Seguro que desea cerrar?\nLos valores no se guardaran",
        parent=self,
        alert=True,
        buttons=['Cancelar:secondary', 'Cerrar:primary']
      )
      if msg == 'Cerrar':
        self.destroy()