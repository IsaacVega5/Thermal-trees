# Thermal Threes
Thermal Threes es una aplicación que facilita el procesamiento de grandes volúmenes de imágenes termales, principalmente diseñada para árboles.


## Instalación
Basta con descargar ...

## Uso
De forma simplificada esta es la forma de utilizar esta aplicación:
  1. Seleccionar la carpeta donde se encuentran las imágenes.
  2. Crear las mascaras con las que se hará la máscara promedio que se aplicará a todas las imágenes. Por defecto se seleccionaran imágenes de forma aleatoria. más detalles **Tipos de selección**.
  3. Obtener temperatura, por defecto el rango de temperatura es de -30.5 a 24.4
  4. Filtrar el rango de temperatura que se utilizaran en cada imagen para procesar la información.
  5. Al realizar el paso anterior con todas las imágenes se abrirá una ventana con la información procesada.
  6. Para guardar los datos, se debe hacer click en guardar y seleccionar la ubicación del archivo xlsx.

### Seleccionar carpetas
Basta con seleccionar la carpeta en la cual se encuentran las imágenes que se desean procesar. Luego de seleccionar se mostrará ina lista de las imágenes en donde se puede ver una vista previa de las imágenes.

### Seleccionar imágenes para las máscaras
Para crear las mascaras se debe primero elegir la cantidad de imágenes que se utilizaran para crear la mascara promedio, por defecto es 20.

Además de la cantidad se debe seleccionar la forma de seleccionar las imágenes, por defecto es aleatoria.

#### Tipo de selección
- **Aleatorio**: Se seleccionarán las imágenes de forma aleatoria.
- **Primeros**: Se seleccionarán las primeras imágenes de la lista.
- **Últimos**: Se seleccionarán las último últimas imágenes de la lista.
- **Seleccionados:** Se utilizaran las imágenes que estén seleccionadas en la lista de imágenes, para seleccionar más de una imagen, basta con hacer *"Crtl + click"* sobre la imagen que se desee seleccionar. Hay que tener en cuenta que este método ignora la cantidad de máscaras seleccionadas.

### Crear las máscaras
Luego de seleccionar la cantidad de imágenes y el tipo de selección se debe hacer click en "Generar", se abrirán en secuencia ventanas en las que se debe seleccionar el area de interés de la imagen en la parte izquierda, durante este proceso se mostrará una vista previa la mascara en la parte derecha.

En caso de equivocarse se puede volver atrás en deshacer y si se quiere limpiar toda el area seleccionada para empezar de nuevo se debe hacer click en "Limpiar".

Luego de haber seleccionado el area de interés se debe hacer click en "Guardar" para guardar la mascara creada. Se abrirán ventanas similares hasta haber completado todas las mascaras.

### Obtener temperatura
Luego de tener las mascarás podemos obtener la temperatura de las imágenes con el botón "Obtener t°" en la parte inferior de la pantalla. Por defecto para obtener la temperatura se utilizará el rango de -30.5 a 24.4, pero se puede modificar en la parte inferior izquierda de la pantalla antes de haber echo click en "Obtener t°".

### Filtrar temperatura
Luego de haber echo click en "Obtener t°" se debe filtrar el rango de temperatura que se utilizarán en cada imagen para procesar la información. Se abrirán ventanas una tras otra hasta que se hayan filtrado todas las imágenes.

En la ventana de filtro, aparecerá un histograma y la imagen con la mascara promedio aplicada. En donde podremos hacer click en cualquier parte de la imagen para obtener la temperatura correspondiente.

Se debe hacer click en guardar para guardar el rango de temperaturas deseado, si se cierra la ventana sin guardar los valores de la imagen no se consideraran para el resultado final.

### Visualización de los datos
Luego de haber filtrado la temperatura de cada imagen se abrirá una ventana con todos los datos obtenidos de cada imagen, en donde se puede ver los datos antes de guardarlos en un archivo xlsx.

Para guardar los datos basta con hacer click en guardar y seleccionar el ubicación y el nombre del archivo xlsx.

Si se cierra la ventana sin haber guardado los datos no se guardarán y se deberán filtrar nuevamente las temperaturas de cada imagen.

## Datos resultantes
Los valores que se obtendrán son los siguientes:
* Temperatura minima de la imagen
* Temperatura máxima de la imagen
* Temperatura mediana de la imagen
* Desviación estándar
* Twet
* Tdry
* Temperatura promedio de la imagen en base a Twet y Tdry
* Porcentaje de porosidad de la imagen
  
## Authors

- [IsaacVega5](https://github.com/IsaacVega5)
