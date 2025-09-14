import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sympy import Interval, Union, simplify, symbols
from .parser import parsear_expresion
from .analisis import (
    calcular_dominio,
    calcular_recorrido,
    intersecciones_ejes,
    evaluar_punto,
    extraer_restricciones_dominio,
    describir_metodo_recorrido,
)
from .utils import intervalos_a_texto, limitar, num_bonito, bullet
from .errores import ErrorParser, ErrorDominio, ErrorRecorrido, ErrorEvaluacion
from .grafico import preparar_malla

x = symbols('x', real=True)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador de Funciones")
        self.geometry("1024x720")
        self._construir_ui()

    def _construir_ui(self):
        marco_top = ttk.Frame(self, padding=10)
        marco_top.pack(fill="x")

        ttk.Label(marco_top, text="f(x) =").grid(row=0, column=0, sticky="w")
        self.entrada_funcion = ttk.Entry(marco_top, width=60)
        self.entrada_funcion.grid(row=0, column=1, padx=6)

        ttk.Label(marco_top, text="x =").grid(row=0, column=2, sticky="e")
        self.entrada_x = ttk.Entry(marco_top, width=12)
        self.entrada_x.grid(row=0, column=3, padx=6)

        self.btn_analizar = ttk.Button(marco_top, text="Analizar", command=self.analizar)
        self.btn_analizar.grid(row=0, column=4, padx=6)

        ttk.Label(marco_top, text="Ventana x:").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.min_x = ttk.Entry(marco_top, width=10); self.min_x.insert(0, "-10")
        self.max_x = ttk.Entry(marco_top, width=10); self.max_x.insert(0, "10")
        self.min_x.grid(row=1, column=1, sticky="w", pady=(8,0))
        self.max_x.grid(row=1, column=2, sticky="w", pady=(8,0))
        self.btn_graficar = ttk.Button(marco_top, text="Graficar", command=self.graficar)
        self.btn_graficar.grid(row=1, column=4, padx=6, pady=(8,0))

        panel = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        panel.pack(fill="both", expand=True, padx=10, pady=10)

        marco_reporte = ttk.Frame(panel, padding=5)
        panel.add(marco_reporte, weight=1)

        ttk.Label(marco_reporte, text="Reporte").pack(anchor="w")
        self.txt = tk.Text(marco_reporte, height=20, wrap="word")
        self.txt.pack(fill="both", expand=True)

        marco_fig = ttk.Frame(panel, padding=5)
        panel.add(marco_fig, weight=2)

        self.fig = Figure(figsize=(6,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Gráfica de f(x)")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=marco_fig)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.expr = None
        self.dominio = None
        self.punto_eval = None

    def analizar(self):
        fx = self.entrada_funcion.get().strip()
        xtexto = self.entrada_x.get().strip()
        self.txt.delete("1.0", tk.END)
        self.punto_eval = None

        try:
            expr = parsear_expresion(fx)
            self.expr = expr
        except ErrorParser as e:
            messagebox.showerror("Error de Parser", str(e)); return

        try:
            dom = calcular_dominio(expr)
            self.dominio = dom
        except Exception as e:
            messagebox.showerror("Error de Dominio", str(e)); return

        try:
            rango, exacto, n_muestras = calcular_recorrido(expr, dom)
            etiqueta_rango = f"{'Exacto' if exacto else 'Aproximado'}"
        except Exception as e:
            rango, etiqueta_rango, n_muestras = None, f"Error: {e}", None

        try:
            interx, intery = intersecciones_ejes(expr, dom)
        except Exception:
            interx, intery = [], None

        pasos = []
        if xtexto:
            try:
                x0 = float(xtexto)
                if x0 not in dom:
                    pasos = [f"x = {x0} no pertenece al dominio de f(x)."]
                else:
                    y0, pasos = evaluar_punto(expr, x0)
                    self.punto_eval = (x0, y0)
            except Exception as e:
                pasos = [f"No se pudo evaluar en x={xtexto}: {e}"]

        self._imprimir_reporte(expr, dom, rango, etiqueta_rango, interx, intery, pasos, n_muestras)

    def _imprimir_reporte(self, expr, dom, rango, etiqueta_rango, interx, intery, pasos, n_muestras):
        # 1) Función
        self.txt.insert(tk.END, "1) Función ingresada:\n")
        self.txt.insert(tk.END, f"   f(x) = {expr}\n\n")

        # 2) Dominio
        self.txt.insert(tk.END, "2) Dominio:\n")
        self.txt.insert(tk.END, f"   {intervalos_a_texto(dom)}\n")
        try:
            reglas = extraer_restricciones_dominio(expr)
            if reglas:
                self.txt.insert(tk.END, "   Restricciones detectadas:\n")
                for r in reglas:
                    self.txt.insert(tk.END, f"   {bullet(r)}")
        except Exception:
            pass
        self.txt.insert(tk.END, "\n")

        # 3) Recorrido
# 3) Recorrido
        self.txt.insert(tk.END, f"3) Recorrido ({etiqueta_rango}):\n")
        if rango is not None:
            try:
                # función local para simplificar extremos de un Interval
                def _simp_interval(I: Interval):
                    a = simplify(I.start) if hasattr(I, "start") else I.start
                    b = simplify(I.end)   if hasattr(I, "end")   else I.end
                    return Interval(a, b, left_open=I.left_open, right_open=I.right_open)

            # Si es Interval, simplificar; si es Union, simplificar cada intervalo
                R = rango
                if isinstance(R, Interval):
                    R = _simp_interval(R)
                elif isinstance(R, Union):
                    nuevos = []
                    for pieza in R.args:
                        if isinstance(pieza, Interval):
                            nuevos.append(_simp_interval(pieza))
                        else:
                            nuevos.append(pieza)
                    R = Union(*nuevos)

                self.txt.insert(tk.END, f"   {intervalos_a_texto(R)}\n")
            except Exception:
                # fallback a la impresión original si algo falla
                self.txt.insert(tk.END, f"   {intervalos_a_texto(rango)}\n")
        else:
            self.txt.insert(tk.END, f"   {etiqueta_rango}\n")
        try:
            metodo = describir_metodo_recorrido(etiqueta_rango == 'Exacto', dom, n_muestras)
            if metodo:
                self.txt.insert(tk.END, "   Método de cálculo del recorrido:\n")
                for r in metodo:
                    self.txt.insert(tk.END, f"   {bullet(r)}")
        except Exception:
            pass
        self.txt.insert(tk.END, "\n")

        # 4) Intersecciones
        self.txt.insert(tk.END, "4) Intersecciones con los ejes:\n")
        if intery is not None:
            self.txt.insert(tk.END, f"   Con eje Y: (0, {num_bonito(intery[1])})\n")
        else:
            self.txt.insert(tk.END, "   Con eje Y: No definida o fuera del dominio\n")
        if interx:
            xs = ", ".join(f"({num_bonito(vx)}, 0)" for vx, _ in interx)
            self.txt.insert(tk.END, f"   Con eje X: {xs}\n")
        else:
            self.txt.insert(tk.END, "   Con eje X: Sin intersecciones reales encontradas\n")
        self.txt.insert(tk.END, "   Interpretación:\n")
        self.txt.insert(tk.END, "   " + bullet("La intersección con Y se obtiene evaluando f(0)."))
        self.txt.insert(tk.END, "   " + bullet("Las intersecciones con X se obtienen resolviendo f(x)=0 (o detectando cruces por muestreo continuo)."))
        self.txt.insert(tk.END, "\n")

        # 5) Evaluación en punto
        if pasos:
            self.txt.insert(tk.END, "5) Evaluación en punto:\n")
            for p in pasos:
                self.txt.insert(tk.END, f"   - {p}\n")
            self.txt.insert(tk.END, "\n")

    def graficar(self):
        if self.expr is None or self.dominio is None:
            messagebox.showinfo("Información", "Primero analiza una función."); return
        try:
            xmin = float(self.min_x.get())
            xmax = float(self.max_x.get())
            if xmax <= xmin:
                raise ValueError("La ventana x es inválida.")
        except Exception as e:
            messagebox.showerror("Error", f"Ventana inválida: {e}"); return

        self.ax.clear()
        self.ax.set_title("Gráfica de f(x)")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)

        segs = preparar_malla(self.expr, self.dominio, xmin, xmax, puntos=1600)
        for seg in segs:
            xs = [p[0] for p in seg]
            ys = [p[1] for p in seg]
            self.ax.plot(xs, ys, linewidth=1.5, label=None)

        try:
            interx, intery = intersecciones_ejes(self.expr, self.dominio)
            if intery is not None and xmin <= intery[0] <= xmax:
                self.ax.scatter([intery[0]], [intery[1]], s=40, marker="o", label="Intersección Y")
            if interx:
                xs = [p[0] for p in interx if xmin <= p[0] <= xmax]
                ys = [0.0 for _ in xs]
                if xs:
                    self.ax.scatter(xs, ys, s=40, marker="x", label="Intersecciones X")
        except Exception:
            pass

        if self.punto_eval is not None:
            x0, y0 = self.punto_eval
            if xmin <= x0 <= xmax:
                self.ax.scatter([x0], [y0], s=60, marker="D", label=f"Punto ({x0:.3g},{y0:.3g})")

        self.ax.legend(loc="best", fontsize=8)
        self.canvas.draw()
