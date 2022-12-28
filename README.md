# Sistema de reconocimiento corporal utilizando Webcam - Fruit Ninja, Virtual Reality Edition

### Elaborado por:
- Diaz Portilla/Carlo Rodrigo
- Mamani Cañari/Gabriel Antony

### Para ejecutar el programa:
```python
pip install -r requirements.txt
python init.py
```
> **Nota:**

> En la línea número 114 del archivo init.py se tiene el siguiente código: cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

> En caso surja algún error con la cámara por favor checkear las cámaras que posee en su computadora. Las cámaras se encuentran en forman de arreglo del 0 hasta el número total de cámaras menos 1. Por ejemplo en el código mostrado estamos usando la segunda cámara reconocida por nuestro computador de pruebas pero se encuentra en la posición 1 del arreglo de cámaras. 

> Para checkear el orden de sus cámaras puede ir a la siguiente página web: https://es.webcamtests.com/

> Ahí podrá desplegar un menú y ver el orden de sus cámaras como se muestra en la siguiente imagen: 

![image](https://user-images.githubusercontent.com/85516522/209738903-fc67d50a-3fb2-4467-bfa0-a3794253f901.png)

> Con estas posiciones usted podrá elegir que cámara usar con nuestra aplicación solo cambiando el número 1 que se encuentra por defeto en la línea 114 de init.py cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) por la posición de la cámara que desee usar.

> Por ejemplo en laptos que solo tienen una cámara suele trabajar con el número 0 por lo que esa línea de código cambiada resultaría así: 

> Antes: 
```
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
```
> Cambiado: 
```
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

