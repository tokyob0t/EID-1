# Analizador de Funciones

Aplicación en Python que permite analizar y graficar funciones matemáticas ingresadas por el usuario.  

## Objetivo

El programa entrega:
- **Dominio** de la función, indicando restricciones detectadas.  
- **Recorrido**, de forma exacta si es posible o aproximada en caso contrario.  
- **Intersecciones con los ejes** X e Y.  
- **Evaluación de un punto** mostrando el desarrollo.  
- **Gráfica** de la función respetando el dominio y marcando puntos relevantes.  

## Estructura

```
analizador/
  __init__.py
  analisis.py
  errores.py
  grafico.py
  parser.py
  ui.py
  utils.py
ejemplos/
  funciones.txt
main.py
requirements.txt
```

## Requisitos

- Python 3.10+  
- Tkinter  
- SymPy  
- Matplotlib  

Instalación rápida:  
```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:  
```bash
python main.py
```

También puede ejecutarse como paquete:  
```bash
python -m analizador.main
```

## Ejemplos de uso

- `sin(x)/x`  
- `(x**2 - 1)/(x + 2)`  
- `log(x-1)/sqrt(x+2)`  

En `ejemplos/funciones.txt` se incluyen más funciones de prueba.  
