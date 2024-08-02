import pandas as pd
import numpy as np
from PIL import Image
import cv2

def get_name_from_path(path):
  return path.split('/')[-1].split('.')[0]

def txt_to_array(path):
  df = pd.read_fwf(path, delimiter='\t', encoding='utf-16')[2:]

  matrix = [ df.iloc[i].to_list() for i in range(len(df)) ]
  matrix = [ row[0].split('\t')[1:] for row in matrix ]
  matrix = [ [float( txt.replace('<', '').replace('~', '').replace(',', '.') ) for txt in row] for row in matrix ]
  
  return np.array(matrix)

def txt_to_thermal(path):
  img = txt_to_array(path)
  img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
  color_map = cv2.COLORMAP_VIRIDIS
  img_color = cv2.applyColorMap(img, color_map)
  
  im_pillow = Image.fromarray(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
  return im_pillow