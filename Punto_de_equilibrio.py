import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Funciones para cambiar entre pantallas
def pantalla_inicio():
    frame_entradas.grid()
    frame_tabla.grid()
    frame_integrantes.grid_forget()
    boton_integrantes.place(x=900, y=10)

def pantalla_integrantes():
    frame_integrantes.grid()
    frame_entradas.grid_forget()
    frame_tabla.grid_forget()
    boton_integrantes.place_forget()

# Función para limpiar las entradas y la tabla
def limpiar():   
    for i in tabla_resultados.get_children():
        tabla_resultados.delete(i)
    
    resultado.config(text="")
    
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

        # Calcular el punto de equilibrio
        resultado_unidades = puntoequilibrio(precioventa, costounitario, gastofijo)
            
        limpiar()

        # Generar el rango de unidades con un margen de 25% hacia ambos lados
        margen = resultado_unidades * 0.25
        unidades = [resultado_unidades - margen * 2, resultado_unidades - margen, resultado_unidades, resultado_unidades + margen, resultado_unidades + margen * 2]
        ventas = [u * precioventa for u in unidades]
        costo_variable = [u * costounitario for u in unidades]
        margen_contribucion = [ventas[i] - costo_variable[i] for i in range(len(unidades))]
        utilidad = [margen_contribucion[i] - gastofijo for i in range(len(unidades))]

        # Insertar las filas con categorías
        tabla_resultados.insert("", "end", values=("Unidades", *unidades))
        tabla_resultados.insert("", "end", values=("Ventas", *ventas))
        tabla_resultados.insert("", "end", values=("Costo Variable", *costo_variable))
        tabla_resultados.insert("", "end", values=("Margen de Contribución", *margen_contribucion))
        tabla_resultados.insert("", "end", values=("Costo Fijo", *[gastofijo]*5))
        tabla_resultados.insert("", "end", values=("Utilidad", *utilidad))
        
        # Asegurese de que la tabla este visible
        tabla_resultados.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        # Mostrar el resultado
        resultado.config(text=f"Para alcanzar el punto de equilibrio deberías vender {resultado_unidades:.2f} unidades, "
                              f"equivalentes a Q{resultado_unidades * precioventa:.2f}.\n"
                              f"En este punto, la ganancia es de 0.")
    except ValueError:
        messagebox.showerror("", "El valor introducido no es válido. Introduce por favor un número.")
        return
    
def mostrar_grafica():
    try:
        precioventa = float(entrada_preciov.get())
        costounitario = float(entrada_costounitario.get())
        gastofijo = float(entrada_gastofijo.get())
        
        #Calcular el punto de equilibrio
        resultado_unidades = puntoequilibrio(precioventa, costounitario, gastofijo)
        unidades = [i for i in range(int(resultado_unidades * 2))]  # Rango de unidades
        
        # Cálculos para la gráfica
        ventas_totales = [u * precioventa for u in unidades]
        costos_variables = [u * costounitario for u in unidades]
        costos_fijos = [gastofijo for _ in unidades]  # Los costos fijos son constantes
        costos_totales = [costos_variables[i] + gastofijo for i in range(len(unidades))]
        
        # Se crea la figura
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Graficar y genera las lineas segun el color
        ax.plot(unidades, ventas_totales, label="Ventas Totales", color='green')
        ax.plot(unidades, costos_totales, label="Costos Totales", color='red')
        ax.plot(unidades, costos_variables, label="Costos Variables", color='orange')
        ax.plot(unidades, costos_fijos, label="Costos Fijos", color='purple')
        ax.axvline(x=resultado_unidades, color='blue', linestyle='--', label=f"Punto de Equilibrio: {resultado_unidades:.2f} unidades")
        
        # Configuracion de la grafica
        ax.set_title('Gráfica del Punto de Equilibrio')
        ax.set_xlabel('Unidades')
        ax.set_ylabel('Quetzales (Q)')
        ax.legend()
        ax.grid(True)
        
        # Mostrar la grafica en el canvas
        canvas = FigureCanvasTkAgg(fig, master=frame_tabla)  # Crear canvas para la gráfica
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=4, padx=10, pady=20, sticky="se")
        
    except ValueError:
        messagebox.showerror("", "El valor introducido no es válido. Introduce por favor un número.")
        
# Ventana principal
ventana = tk.Tk()
ventana.title("Punto de Equilibrio")
ventana.geometry("1000x500")

# Crear un frame para las entradas y etiquetas
frame_entradas = tk.Frame(ventana)
frame_entradas.grid(row=0, column=0, sticky="nsew")

frame_tabla = tk.Frame(ventana)
frame_tabla.grid(row=1, column=0, sticky="nsew")

frame_integrantes = tk.Frame(ventana)
frame_integrantes.grid(row=0, column=0, sticky="nsew")
frame_integrantes.grid_forget()

# Label de bienvenida
bienvenida = tk.Label(frame_entradas, text="Bienvenido, ingrese los datos solicitados", font=("Times New Roman", 12))
bienvenida.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

# Etiquetas y entradas
preciovl = tk.Label(frame_entradas, text="Precio de Venta: ", font=("Times New Roman", 10))
preciovl.grid(row=1, column=0, padx=10, pady=10, sticky="e")

entrada_preciov = tk.Entry(frame_entradas, font=("Times New Roman", 10), width=20)
entrada_preciov.grid(row=1, column=1, padx=10, pady=10)

costounil = tk.Label(frame_entradas, text="Costo por Unidad: ", font=("Times New Roman", 10))
costounil.grid(row=2, column=0, padx=10, pady=10, sticky="e")

entrada_costounitario = tk.Entry(frame_entradas, font=("Times New Roman", 10), width=20)
entrada_costounitario.grid(row=2, column=1, padx=10, pady=10)

gastofl = tk.Label(frame_entradas, text="Gasto fijo: ", font=("Times New Roman", 10))
gastofl.grid(row=3, column=0, padx=10, pady=10, sticky="e")

entrada_gastofijo = tk.Entry(frame_entradas, font=("Times New Roman", 10), width=20)
entrada_gastofijo.grid(row=3, column=1, padx=10, pady=10)

boton_calcular = tk.Button(frame_entradas, command=calcular, text="Calcular", font=("Times New Roman", 10))
boton_calcular.grid(row=4, column=1, padx=10, pady=10, sticky="e")

boton_limpiar = tk.Button(frame_entradas, text="Limpiar", command=limpiar, font=("Times New Roman", 10))
boton_limpiar.grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Boton para mostrar grafica
boton_grafica = tk.Button(frame_entradas, text="Mostrar Gráfica", command=mostrar_grafica, font=("Times New Roman", 10))
boton_grafica.grid(row=5, column=1, padx=10, pady=10, sticky="e")

# Tabla para el punto de equilibrio
columnas = ["Categoría", "Valor 1", "Valor 2", "Punto Equilibrio", "Valor 4", "Valor 5"]
tabla_resultados = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=7)
tabla_resultados.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

# Encabezados de las columnas
for col in columnas:
    tabla_resultados.heading(col, text=col)

tabla_resultados.column("Categoría", width=200)
for col in columnas[1:]:
    tabla_resultados.column(col, width=100)

resultado = tk.Label(frame_tabla, text="", font=("Times New Roman", 10))
resultado.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

boton_integrantes = tk.Button(ventana, activebackground="#0085fa", bg="#00bbfa", text="Integrantes", font=("Times New Roman", 8), command=pantalla_integrantes, width=10, height=2)
boton_integrantes.place(x=900, y=10)

# Función para mostrar los integrantes
tree = ttk.Treeview(frame_integrantes, columns=("Nombre", "Carnet", "Rol"), show="headings", height=5)
tree.heading("Nombre", text="Nombre")
tree.heading("Carnet", text="Carnet")
tree.heading("Rol", text="Rol")
tree.column("Nombre", width=250)
tree.column("Carnet", width=120)
tree.column("Rol", width=300)

tree.insert("", "end", values=("Christopher Ricardo Garcia Giron", "0907-24-10087", "Líder de proyecto, encargado del punto de equilibrio"))
tree.insert("", "end", values=("Diego Alejandro Fernández González", "0907-24-25569", "encargado de la generacion de grafica"))
tree.pack(padx=150, pady=50)

boton_volver_integrantes = tk.Button(frame_integrantes, text="Volver al Inicio", command=pantalla_inicio)
boton_volver_integrantes.pack(pady=5)

pantalla_inicio()
ventana.mainloop()
