import numpy as np

def values_from_temperature_list(temperature_list):
  if len(temperature_list) == 0:
    return {'min':'N/A', 'max':'N/A', 'median':'N/A', 'std':'N/A', 'Tw':'N/A', 'Td':'N/A', 'Tc':'N/A', 'CWSI':'N/A', 'porosidad':'N/A'}
  
  t_min = np.min(temperature_list)
  t_max = np.max(temperature_list)
  t_median = np.median(temperature_list)
  std = np.std(temperature_list)
  Tw = t_median - std * 2
  Td = t_median + std * 2
  
  # Temperatura promedio de valores entre tw y td
  temperature_list_tw_td = [t for t in temperature_list if t >= Tw and t <= Td]
  Tc = np.mean(temperature_list_tw_td)
  
  cwsi = ( Tc - Tw ) / ( Td - Tw ) # <- indice máximo
  
  # Calcular la porosidad
  b1 = len(temperature_list)
  b2 = len([t for t in temperature_list if t <= Tw])
  b3 = len([t for t in temperature_list if t >= Td])
  porosidad = (b1 - (b2 + b3)) * 100 / b1 
  
  values = {
    'min': t_min,
    'max': t_max,
    'median': t_median,
    'std': np.std(temperature_list),
    'Tw': Tw,
    'Td': Td,
    'Tc': Tc,
    'CWSI': cwsi,
    'porosidad': porosidad
  }
  
  return values