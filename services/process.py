
def temperature_from_pixel_color(pixel_color):
  pixel_color = 1 - ( pixel_color / 255 )
  temperature = (pixel_color * (30.5 + 24.4)) - 30.5
  temperature = round(temperature, 2)
  return temperature