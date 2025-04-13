import tkinter
from tkinter import ttk  # Para la tabla y combobox
import mysql.connector
from datetime import datetime

# Conectar a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Radial_llantas"
)
cursor = conexion.cursor()

# Obtener clientes y métodos de pago desde la base de datos
cursor.execute("SELECT id_cliente, nombre_cliente FROM clientes")
clientes = cursor.fetchall()
clientes_dict = {str(row[0]): row[1] for row in clientes}
clientes_lista = list(clientes_dict.keys())  # Solo IDs para el combobox

cursor.execute("SELECT id_metodo_pago, metodo FROM metodos_pago")
metodos_pago = cursor.fetchall()
metodos_dict = {str(row[0]): row[1] for row in metodos_pago}
metodos_lista = list(metodos_dict.keys())  # Solo IDs para el combobox

# Crear ventana principal
ventana = tkinter.Tk()
ventana.geometry("800x600")
ventana.title("Gestion de Compras")

# Etiqueta principal
etiqueta = tkinter.Label(ventana, text="Registro de Compras", font=("Arial", 14))
etiqueta.pack(pady=10)

# Tabla visual con Treeview
tabla = ttk.Treeview(ventana, columns=("ID", "Cliente", "Metodo Pago", "Fecha", "Total"), show="headings")
tabla.place(x=50, y=350, width=700, height=200)

# Definir encabezados de la tabla
tabla.heading("ID", text="ID Compra")
tabla.heading("Cliente", text="Cliente")
tabla.heading("Metodo Pago", text="Metodo de Pago")
tabla.heading("Fecha", text="Fecha")
tabla.heading("Total", text="Total")

# Funciones CRUD
def crear():
    id_cliente = comboCliente.get()
    id_metodo_pago = comboMetodoPago.get()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Fecha actual en formato YYYY-MM-DD
    total = txtTotal.get()

    if not id_cliente or not id_metodo_pago or not total:
        print("Todos los campos son obligatorios")
        return
    
    try:
        total = float(total)
        if total < 0:
            print("El total debe ser positivo")
            return
    except ValueError:
        print("Total debe ser un numero valido")
        return

    cursor.execute("INSERT INTO compras (id_cliente, id_metodo_pago, fecha, total) VALUES (%s, %s, %s, %s)", 
                   (id_cliente, id_metodo_pago, fecha_actual, total))
    conexion.commit()
    
    print("Compra registrada exitosamente.")
    leer()  # Actualizar la tabla después de crear

def leer():
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT c.id_compra, cl.nombre_cliente, mp.metodo, c.fecha, c.total FROM compras c JOIN clientes cl ON c.id_cliente = cl.id_cliente JOIN metodos_pago mp ON c.id_metodo_pago = mp.id_metodo_pago")
    resultados = cursor.fetchall()

    for compra in resultados:
        id_compra, cliente, metodo_pago, fecha, total = compra
        tabla.insert("", "end", values=(id_compra, cliente, metodo_pago, fecha, f"${total:.2f}"))

def actualizar():
    id_compra = txtIdActualizar.get()
    id_cliente = comboCliente.get()
    id_metodo_pago = comboMetodoPago.get()
    total = txtTotal.get()

    if not id_compra or not id_cliente or not id_metodo_pago or not total:
        print("Todos los campos son obligatorios para actualizar")
        return
    
    cursor.execute("UPDATE compras SET id_cliente=%s, id_metodo_pago=%s, total=%s WHERE id_compra=%s", 
                   (id_cliente, id_metodo_pago, total, id_compra))
    conexion.commit()
    print("Compra actualizada exitosamente.")
    leer()

def eliminar():
    id_compra = txtEliminar.get()
    
    if not id_compra:
        print("Por favor, ingresa un ID valido para eliminar")
        return

    cursor.execute("DELETE FROM compras WHERE id_compra=%s", (id_compra,))
    conexion.commit()
    print("Compra eliminada exitosamente.")
    leer()

# Labels y cuadros de texto
lblCliente = tkinter.Label(ventana, text="Cliente:")
lblCliente.place(x=50, y=50)
comboCliente = ttk.Combobox(ventana, values=clientes_lista)
comboCliente.place(x=180, y=50, width=250)

lblMetodoPago = tkinter.Label(ventana, text="Metodo de Pago:")
lblMetodoPago.place(x=50, y=80)
comboMetodoPago = ttk.Combobox(ventana, values=metodos_lista)
comboMetodoPago.place(x=180, y=80, width=250)

lblTotal = tkinter.Label(ventana, text="Total:")
lblTotal.place(x=50, y=110)
txtTotal = tkinter.Entry(ventana, bg="#FFC0CB")
txtTotal.place(x=180, y=110, width=250)

lblIdActualizar = tkinter.Label(ventana, text="ID Compra a Actualizar:")
lblIdActualizar.place(x=50, y=140)
txtIdActualizar = tkinter.Entry(ventana, bg="white")
txtIdActualizar.place(x=180, y=140, width=250)

lblEliminar = tkinter.Label(ventana, text="ID Compra a Eliminar:")
lblEliminar.place(x=50, y=170)
txtEliminar = tkinter.Entry(ventana, bg="white")
txtEliminar.place(x=180, y=170, width=250)

# Botones CRUD
btnCrear = tkinter.Button(ventana, text="CREAR", command=crear, bg="lightgreen")
btnCrear.place(x=50, y=210, width=100)

btnLeer = tkinter.Button(ventana, text="LEER", command=leer, bg="lightblue")
btnLeer.place(x=160, y=210, width=100)

btnActualizar = tkinter.Button(ventana, text="ACTUALIZAR", command=actualizar, bg="yellow")
btnActualizar.place(x=270, y=210, width=100)

btnEliminar = tkinter.Button(ventana, text="ELIMINAR", command=eliminar, bg="red")
btnEliminar.place(x=380, y=210, width=100)

# Ejecutar la aplicación
ventana.mainloop()

# Cerrar conexión al salir
conexion.close()