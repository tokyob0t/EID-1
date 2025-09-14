# Analizador de Funciones (Tkinter + SymPy + Matplotlib)

Aplicación de escritorio que **analiza funciones** ingresadas por el usuario y muestra:

- **Dominio** (con **restricciones** detectadas automáticamente).
- **Recorrido** (intento **simbólico** y *fallback* **numérico sin NumPy**, con método explicado).
- **Intersecciones con ejes** (X e Y) y **evaluación de un punto** con paso a paso.
- **Gráfica** limpia (títulos, ejes, leyenda) y **marcado** de intersecciones y del punto evaluado.

Cumple con lo exigido en la **Parte B: Proyecto en Python (Defensa presencial)** del EID, incluyendo **interfaz**, **manejo de errores**, **estructura modular** y **uso de SymPy** (sin NumPy).

---

## 📁 Estructura del proyecto (esta repo)

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

> Ejecuta SIEMPRE desde la raíz del proyecto (la carpeta donde ves `main.py`).

---

## 🧩 Stack

- **Python** 3.10+ (probado con 3.12/3.13)
- **Tkinter** (GUI)
- **SymPy** (parseo, dominio, recorrido, solveset)
- **Matplotlib** (gráficas)
- **Sin NumPy** (requisito)

---

## 📦 Instalación

1) (Opcional) Crea un entorno virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2) Instala dependencias
```bash
pip install -r requirements.txt
```
> Si no tienes `requirements.txt`, puedes usar: `pip install sympy matplotlib`.

---

## ▶️ Ejecución

### Opción A (recomendada por simplicidad)
```bash
python main.py
```

### Opción B (como paquete)
```bash
python -m analizador.main
```

> **No ejecutes `ui.py` directo** (provoca errores de imports relativos). Usa `main.py` o el modo `-m`.

---

## 🧭 Uso de la aplicación

1. En **f(x) =** escribe la función (ej: `sin(x)/x`, `(x**2 - 1)/(x + 2)`, `log(x-1)/sqrt(x+2)`).  
2. (Opcional) En **x =** ingresa un valor para evaluar.  
3. Pulsa **Analizar** para ver:
   - **Dominio** formateado (∪, ±∞) + **restricciones**: denominadores≠0, `log`>0, `sqrt`≥0, tramos `Piecewise`.
   - **Recorrido**: exacto si SymPy puede; si no, **aproximado** con muestreo propio (sin NumPy) e indicación del método.
   - **Intersecciones** con X e Y y breve **interpretación**.
   - **Evaluación en punto** con sustitución y valor numérico.
4. Ajusta **Ventana x** y pulsa **Graficar** para ver la curva, intersecciones y el punto evaluado.

> En `ejemplos/funciones.txt` hay expresiones listas para copiar/pegar.

---

## 🧠 ¿Qué hace por dentro? (resumen)

- **Parseo seguro**: solo variable `x` y nombres permitidos (SymPy).  
- **Dominio**: `function_domain` (o `continuous_domain` fallback) + desglose de **restricciones** detectadas.  
- **Recorrido**: `function_range`; si falla, **muestreo** sobre el dominio (sin NumPy) indicando cuántas muestras se usaron.  
- **Intersecciones**: con **Y** evaluando `x=0` si pertenece al dominio; con **X** usando `solveset` y/o **bisección** asistida por muestreo.  
- **Gráfica**: se trazan **segmentos continuos** dentro del dominio (corte en discontinuidades).

---

## 🧯 Manejo de errores

- Expresiones vacías/ilegales → mensaje claro.
- Variables distintas de `x` → rechazo inmediato.
- Dominio/recorrido imposibles de determinar → explicación del motivo.
- Evaluación en punto inválida → detalle del error.

Los errores se muestran en diálogos y el reporte queda limpio.

---

## 🧪 Ejemplos recomendados

- `sin(x)/x`  
  Dominio: `(-∞, 0) ∪ (0, ∞)`  
  Recorrido aprox (método numérico indicado en reporte).

- `(x**2 - 1)/(x + 2)`  
  Dominio: `(-∞, -2) ∪ (-2, ∞)`  
  Recorrido exacto: `(-∞, -4 - 2*sqrt(3)] ∪ [-4 + 2*sqrt(3), ∞)`

- `log(x-1)/sqrt(x+2)`  
  Dominio: `(1, ∞)`

- `Piecewise((x**2, x<0), (sqrt(x), True))`  
  El reporte incluye las **condiciones por tramos**.

---
