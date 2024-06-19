
def temperature_from_pixel_color(pixel_color, temperature_range = (-30.5, 24.4)):
  min = abs(temperature_range[0])
  max = abs(temperature_range[1])
  pixel_color = 1 - ( pixel_color / 255 )
  temperature = (pixel_color * (max + min)) - min
  temperature = round(temperature, 2)
  return temperature