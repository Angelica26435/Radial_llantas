import tkinter
from tkinter import ttk  # Para la tabla y el Combobox
import mysql.connector

# Conectar a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Radial_llantas"
)
cursor = conexion.cursor()

# Crear ventana principal
ventana = tkinter.Tk()
ventana.geometry("600x500")
ventana.title("Gestion de Metodos de Pago")

# Etiqueta principal
etiqueta = tkinter.Label(ventana, text="Metodos de Pago", font=("Arial", 14))
etiqueta.pack(pady=10)

# Tabla visual con Treeview
tabla = ttk.Treeview(ventana, columns=("ID", "Metodo"), show="headings")
tabla.place(x=50, y=270, width=500, height=150)

# Definir encabezados de la tabla
tabla.heading("ID", text="ID")
tabla.heading("Metodo", text="Metodo de Pago")

# Función para mostrar campo de otro método
def mostrar_otro(*args):
    if comboMetodo.get() == "Otro":
        txtMetodo.place(x=180, y=80, width=250)
    else:
        txtMetodo.place_forget()

# Funciones CRUD
def crear():
    metodo_pago = comboMetodo.get()

    # Si seleccionó "Otro", tomamos el valor del Entry
    if metodo_pago == "Otro":
        metodo_pago = txtMetodo.get()
    
    if not metodo_pago:
        print("El metodo de pago no puede estar vacio.")
        return

    cursor.execute("INSERT INTO metodos_pago (metodo) VALUES (%s)", (metodo_pago,))
    conexion.commit()
    
    print("Metodo de pago creado exitosamente.")
    leer()  # Actualizar la tabla

def leer():
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT * FROM metodos_pago")
    resultados = cursor.fetchall()

    for metodo in resultados:
        tabla.insert("", "end", values=metodo)

def actualizar():
    id_metodo = txtIdActualizar.get()
    metodo_pago = comboMetodo.get()

    # Si seleccionó "Otro", tomamos el valor del Entry
    if metodo_pago == "Otro":
        metodo_pago = txtMetodo.get()

    if not id_metodo or not metodo_pago:
        print("ID y Metodo son obligatorios para actualizar.")
        return

    cursor.execute("UPDATE metodos_pago SET metodo=%s WHERE id_metodo_pago=%s", (metodo_pago, id_metodo))
    conexion.commit()
    print("Metodo de pago actualizado exitosamente.")
    leer()

def eliminar():
    id_metodo = txtIdEliminar.get()
    
    if not id_metodo:
        print("Por favor, ingresa un ID valido para eliminar.")
        return

    cursor.execute("DELETE FROM metodos_pago WHERE id_metodo_pago=%s", (id_metodo,))
    conexion.commit()
    print("Metodo de pago eliminado exitosamente")
    leer()

# Labels y cuadros de texto
lblMetodo = tkinter.Label(ventana, text="Metodo de Pago:")
lblMetodo.place(x=50, y=50)

# Combobox para seleccionar método de pago
comboMetodo = ttk.Combobox(ventana, values=["Efectivo", "Tarjeta", "Otro"])
comboMetodo.place(x=180, y=50, width=250)
comboMetodo.bind("<<ComboboxSelected>>", mostrar_otro)  

# Campo de texto para "Otro"
txtMetodo = tkinter.Entry(ventana, bg="#FFC0CB")  # Se oculta hasta que "Otro" sea seleccionado

lblIdActualizar = tkinter.Label(ventana, text="ID Método a Actualizar:")
lblIdActualizar.place(x=50, y=110)
txtIdActualizar = tkinter.Entry(ventana, bg="white")
txtIdActualizar.place(x=180, y=110, width=250)

lblIdEliminar = tkinter.Label(ventana, text="ID Método a Eliminar:")
lblIdEliminar.place(x=50, y=140)
txtIdEliminar = tkinter.Entry(ventana, bg="white")
txtIdEliminar.place(x=180, y=140, width=250)

# Botones CRUD
btnCrear = tkinter.Button(ventana, text="CREAR", command=crear, bg="lightgreen")
btnCrear.place(x=50, y=180, width=100)

btnLeer = tkinter.Button(ventana, text="LEER", command=leer, bg="lightblue")
btnLeer.place(x=160, y=180, width=100)

btnActualizar = tkinter.Button(ventana, text="ACTUALIZAR", command=actualizar, bg="yellow")
btnActualizar.place(x=270, y=180, width=100)

btnEliminar = tkinter.Button(ventana, text="ELIMINAR", command=eliminar, bg="red")
btnEliminar.place(x=380, y=180, width=100)

ventana.mainloop()

conexion.close()