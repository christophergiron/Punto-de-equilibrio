import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter

def pantalla_inicio():
    limpiar()
    frame_entradas.grid()
    frame_tabla.grid()
    frame_grafica.grid()
    frame_integrantes.grid_remove() 
    boton_integrantes.place(x=1250, y=10)
    boton_cerrar.place(x=1250, y=50, width=80, height=40) 
    
def pantalla_integrantes():
    frame_integrantes.grid()
    frame_entradas.grid_remove()
    frame_tabla.grid_remove()
    frame_grafica.grid_remove()
    boton_integrantes.place_forget()
    boton_cerrar.place_forget()
    
# Función para limpiar la ventana
def limpiar():
    entrada_preciov.delete(0, tk.END)
    entrada_costounitario.delete(0, tk.END)
    entrada_gastofijo.delete(0, tk.END)

    # Limpiar la tabla
    for i in tabla_resultados.get_children():
        tabla_resultados.delete(i)

    resultado.config(text="")

    # Limpiar la gráfica si existe
    if hasattr(limpiar, 'canvas') and limpiar.canvas:
        limpiar.canvas.get_tk_widget().grid_forget()
        limpiar.canvas = None

# Función para calcular el punto de equilibrio
def puntoequilibrio(precioventa, costounitario, gastofijo):
    return gastofijo / (precioventa - costounitario)

def calcular():
    try:
        precioventa = float(entrada_preciov.get())
        costounitario = float(entrada_costounitario.get())
        gastofijo = float(entrada_gastofijo.get())

        resultado_unidades = puntoequilibrio(precioventa, costounitario, gastofijo)

        margen = resultado_unidades * 0.25
        unidades = [resultado_unidades - margen * 2, resultado_unidades - margen, resultado_unidades,
                    resultado_unidades + margen, resultado_unidades + margen * 2]
        ventas = [u * precioventa for u in unidades]
        costo_variable = [u * costounitario for u in unidades]
        margen_contribucion = [ventas[i] - costo_variable[i] for i in range(len(unidades))]
        utilidad = [margen_contribucion[i] - gastofijo for i in range(len(unidades))]

        for i in tabla_resultados.get_children():
            tabla_resultados.delete(i)

        # Insertar nuevos datos en la tabla
        tabla_resultados.insert("", "end", values=("Unidades", *unidades))
        tabla_resultados.insert("", "end", values=("Ventas", *ventas))
        tabla_resultados.insert("", "end", values=("Costo Variable", *costo_variable))
        tabla_resultados.insert("", "end", values=("Margen de Contribución", *margen_contribucion))
        tabla_resultados.insert("", "end", values=("Costo Fijo", *[gastofijo] * 5))
        tabla_resultados.insert("", "end", values=("Utilidad", *utilidad))

        resultado.config(text=f"Para alcanzar el punto de equilibrio deberías vender {resultado_unidades:.2f} unidades, "f"equivalentes a Q{resultado_unidades * precioventa:.2f}.\n"f"En este punto, la ganancia es de 0.")

    except ValueError:
        messagebox.showerror("", "El valor introducido no es válido. Introduce por favor un número.")

def mostrar_grafica():
    try:
        precioventa = float(entrada_preciov.get())
        costounitario = float(entrada_costounitario.get())
        gastofijo = float(entrada_gastofijo.get())

        resultado_unidades = puntoequilibrio(precioventa, costounitario, gastofijo)
        unidades = [i for i in range(int(resultado_unidades * 2))]

        ventas_totales = [u * precioventa for u in unidades]
        costos_variables = [u * costounitario for u in unidades]
        costos_fijos = [gastofijo for _ in unidades]
        costos_totales = [costos_variables[i] + gastofijo for i in range(len(unidades))]

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(unidades, ventas_totales, label="Ventas Totales", color='green', linewidth=2)
        ax.plot(unidades, costos_totales, label="Costos Totales", color='red', linestyle='-', linewidth=2)
        ax.plot(unidades, costos_variables, label="Costos Variables", color='orange', linewidth=2)
        ax.plot(unidades, costos_fijos, label="Costos Fijos", color='purple', linewidth=2)
        ax.axvline(x=resultado_unidades, color='blue', linestyle='--', label=f"Punto de Equilibrio: {resultado_unidades:.2f} unidades")

        ax.set_title('Gráfica del Punto de Equilibrio', fontsize=14)
        ax.set_xlabel('Unidades', fontsize=12)
        ax.set_ylabel('Quetzales (Q)', fontsize=12)

        ax.set_ylim(0, max(ventas_totales) * 1.1)

        def quetzales(x, pos):
            return f'Q{x:,.0f}'
        ax.yaxis.set_major_formatter(FuncFormatter(quetzales))

        ax.grid(True)
        ax.legend()

        if hasattr(limpiar, 'canvas') and limpiar.canvas:
            limpiar.canvas.get_tk_widget().grid_forget()

        # Mostrar la nueva gráfica
        limpiar.canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
        limpiar.canvas.draw()
        limpiar.canvas.get_tk_widget().grid(row=0, column=0)

    except ValueError:
        messagebox.showerror("", "El valor introducido no es válido. Introduce por favor un número.")

# Ventana principal
ventana = tk.Tk()
ventana.title("Punto de Equilibrio")
ventana.geometry("1000x500")
ventana.state('zoomed')
ventana.iconbitmap('logo.ico')
# Crear un frame para las entradas y etiquetas
frame_entradas = tk.Frame(ventana)
frame_entradas.grid(row=0, column=0, sticky="nsew")

frame_tabla = tk.Frame(ventana)
frame_tabla.grid(row=1, column=0, sticky="nsew")

frame_grafica = tk.Frame(ventana)
frame_grafica.grid(row=1, column=1, sticky="nsew")

frame_integrantes = tk.Frame(ventana)
frame_integrantes.grid(row=0, column=0, sticky="nsew")
frame_integrantes.grid_remove()

# Tabla para el punto de equilibrio
columnas = ["Categoría", "Valor 1", "Valor 2", "Valor 3", "Valor 4", "Valor 5"]
tabla_resultados = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=7)
tabla_resultados.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

# Encabezados de las columnas
for col in columnas:
    tabla_resultados.heading(col, text=col)
tabla_resultados.column("Categoría", width=200)
for col in columnas[1:]:
    tabla_resultados.column(col, width=100)

# Etiquetas y entradas
bievenida = tk.Label(frame_entradas, text="Bienvenido Ingrese los datos solicitados", font=("Times New Roman", 12))
bievenida.grid(row=0, column=3, padx=80, pady=10, sticky="n")

preciovl = tk.Label(frame_entradas, text="Precio de Venta: ", font=("Times New Roman", 10))
preciovl.grid(row=1, column=0, padx=10, pady=10, sticky="e")

entrada_preciov = tk.Entry(frame_entradas, font=("Times New Roman", 10), width=20)
entrada_preciov.grid(row=1, column=1, padx=10, pady=10, sticky="w")

costounitariol = tk.Label(frame_entradas, text="Costo Unitario: ", font=("Times New Roman", 10))
costounitariol.grid(row=2, column=0, padx=10, pady=10, sticky="e")

entrada_costounitario = tk.Entry(frame_entradas, font=("Times New Roman", 10), width=20)
entrada_costounitario.grid(row=2, column=1, padx=10, pady=10, sticky="w")

gastofijol = tk.Label(frame_entradas, text="Gasto Fijo: ", font=("Times New Roman", 10))
gastofijol.grid(row=3, column=0, padx=10, pady=10, sticky="e")

entrada_gastofijo = tk.Entry(frame_entradas, font=("Times New Roman", 10), width=20)
entrada_gastofijo.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Botones
boton_grafica = tk.Button(frame_entradas, text="Mostrar Gráfica", command=mostrar_grafica)
boton_grafica.grid(row=6, column=1, padx=10, pady=10, sticky="w")

boton_calcular = tk.Button(frame_entradas, text="Calcular", command=calcular)
boton_calcular.grid(row=6, column=2, padx=10, pady=10, sticky="w")

boton_limpiar = tk.Button(frame_entradas, text="Limpiar", command=limpiar)
boton_limpiar.grid(row=6, column=3, padx=10, pady=10, sticky="w")

boton_integrantes = tk.Button(ventana, text="Integrantes", command=pantalla_integrantes)
boton_integrantes.place(x=1250, y=10)

boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
boton_cerrar.place(x=1250, y=50, width=80, height=40) 

resultado = tk.Label(frame_entradas, text="", font=("Times New Roman", 12), fg="black")
resultado.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="n")

# contenido de la pantalla integrantes 
tree = ttk.Treeview(frame_integrantes, columns=("Nombre", "Carnet", "Rol"), show="headings", height=5)
tree.heading("Nombre", text="Nombre")
tree.heading("Carnet", text="Carnet")
tree.heading("Rol", text="Rol")
tree.column("Nombre", width=250)
tree.column("Carnet", width=120)
tree.column("Rol", width=400)

tree.insert("", "end", values=("Christopher Ricardo Garcia Giron", "0907-24-10087", "Líder de proyecto, encargado del todo el punto de equilibrio y la interfaz"))
tree.insert("", "end", values=("Diego Alejandro Fernández González","0907-24-25569", "Encargado de la creacion de la grafica"))
tree.pack(padx=350, pady=50)

boton_volver_integrantes = tk.Button(frame_integrantes, text="Volver al Inicio", background="#a81638", activebackground="#d40636",command=pantalla_inicio)
boton_volver_integrantes.pack(pady=5) 

ventana.mainloop()