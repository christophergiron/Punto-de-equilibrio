import tkinter as tk
from tkinter import messagebox
import matplotlib as mt
from tkinter import ttk
ventana = tk.Tk()
ventana.title("Punto de Equilibrio")
ventana.geometry("1000x500")

pantalla_integrantes = tk.Frame(ventana)
pantalla_principal = tk.Frame(ventana)

def pantalla_inicio():
    pantalla_principal.grid
    boton_calcular.grid(row=3, column=1, padx=10, pady=10)

def frame_integrantes():
    pantalla_integrantes.grid
    
    
def puntoequi(precioventa, costounitario, gastofijo):
    return gastofijo // (precioventa - costounitario)

def calcular():
    try:
        precioventa = float(entrada_preciov.get())
        costounitario = float(entrada_costounitario.get())
        gastofijo = float(entrada_gastofijo.get())
    
        resultado = puntoequi(precioventa, costounitario, gastofijo)
        resultado_unidades.config(text= f"Para Alcanzar el punto de equilibrio deberia vender {resultado} unidades")
    
    except ValueError:
        messagebox.showerror("", "El valor introducido no es valido, Introduce Por favor un Numero")
        return
    
bienvenida = tk.Label(pantalla_principal, text="Bienvenido ingrese los datos solicitados")
bienvenida.grid(row=0,column=3,padx=5,pady=5)
preciovl = tk.Label(ventana, text="Precio de Venta: ", font=("Times New Roman", 10))
preciovl.grid(row=1, column=0, padx=10, pady=10)

costounil = tk.Label(ventana, text="Costo por Unidad: ", font=("Times New Roman", 10))
costounil.grid(row=2, column=0, padx=10, pady=10)

gastofl = tk.Label(ventana, text="Gasto fijo: ", font=("Times New Roman", 10))
gastofl.grid(row=3, column=0, padx=10, pady=10)

entrada_preciov = tk.Entry(ventana, font=("Times New Roman", 10), width=50)
entrada_preciov.grid(row=1, column=1, padx=10, pady=10)

entrada_costounitario = tk.Entry(ventana, font=("Times New Roman", 10), width=50)
entrada_costounitario.grid(row=2, column=1, padx=10, pady=10)

entrada_gastofijo = tk.Entry(ventana, font=("Times New Roman", 10), width=50)
entrada_gastofijo.grid(row=3, column=1, padx=10, pady=10)

boton_calcular = tk.Button(ventana, command=calcular, text="Calcular", font=("Times New Roman", 10) )
boton_calcular.grid(row=4, column=1, padx=10, pady=10)

resultado_unidades= tk.Label(ventana, text="", font=("Times New Roman", 10))
resultado_unidades.grid(row=5, column=1, padx=10, pady=10)

ventana.mainloop()
