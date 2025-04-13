import tkinter
from tkinter import ttk  # Para la tabla y combobox
import mysql.connector

# Conectar a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Radial_llantas"
)
cursor = conexion.cursor()

# Obtener datos de la base de datos
cursor.execute("SELECT id_compra, fecha FROM compras")
compras = cursor.fetchall()
compras_dict = {str(row[0]): row[1] for row in compras}
compras_lista = list(compras_dict.keys())  # IDs para el Combobox

cursor.execute("SELECT id_producto, nombre_producto, precio FROM productos")
productos = cursor.fetchall()
productos_dict = {str(row[0]): (row[1], row[2]) for row in productos}  # ID: (Nombre, Precio)
productos_lista = list(productos_dict.keys())  # IDs para el Combobox

cursor.execute("SELECT id_metodo_pago, metodo FROM metodos_pago")
metodos_pago = cursor.fetchall()
metodos_dict = {str(row[0]): row[1] for row in metodos_pago}
metodos_lista = list(metodos_dict.keys())  # IDs para el Combobox

# Crear ventana principal
ventana = tkinter.Tk()
ventana.geometry("850x600")
ventana.title("Gestion de Detalle de Compras")

# Etiqueta principal
etiqueta = tkinter.Label(ventana, text="Detalle de Compras", font=("Arial", 14))
etiqueta.pack(pady=10)

# Tabla visual con Treeview
tabla = ttk.Treeview(ventana, columns=("ID Detalle", "Compra", "Producto", "Metodo Pago", "Cantidad", "Subtotal"), show="headings")
tabla.place(x=50, y=350, width=750, height=200)

# Definir encabezados de la tabla
tabla.heading("ID Detalle", text="ID Detalle")
tabla.heading("Compra", text="Compra")
tabla.heading("Producto", text="Producto")
tabla.heading("Metodo Pago", text="Metodo de Pago")
tabla.heading("Cantidad", text="Cantidad")
tabla.heading("Subtotal", text="Subtotal")

# Funciones CRUD
def crear():
    id_compra = comboCompra.get()
    id_producto = comboProducto.get()
    id_metodo_pago = comboMetodoPago.get()
    cantidad = txtCantidad.get()

    if not id_compra or not id_producto or not id_metodo_pago or not cantidad:
        print("Todos los campos son obligatorios")
        return
    
    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0")
            return
    except ValueError:
        print("Cantidad debe ser un número valido")
        return

    # Obtener precio del producto y calcular subtotal
    precio = productos_dict[id_producto][1]
    subtotal = cantidad * precio

    cursor.execute("INSERT INTO detalle_compras (id_compra, id_producto, id_metodo_pago, cantidad, subtotal) VALUES (%s, %s, %s, %s, %s)", 
                   (id_compra, id_producto, id_metodo_pago, cantidad, subtotal))
    conexion.commit()
    
    print("Detalle de compra registrado exitosamente.")
    leer()  

def leer():
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT dc.id_detalle, c.fecha, p.nombre_producto, mp.metodo, dc.cantidad, dc.subtotal FROM detalle_compras dc JOIN compras c ON dc.id_compra = c.id_compra JOIN productos p ON dc.id_producto = p.id_producto JOIN metodos_pago mp ON dc.id_metodo_pago = mp.id_metodo_pago")
    resultados = cursor.fetchall()

    for detalle in resultados:
        id_detalle, fecha_compra, producto, metodo_pago, cantidad, subtotal = detalle
        tabla.insert("", "end", values=(id_detalle, fecha_compra, producto, metodo_pago, cantidad, f"${subtotal:.2f}"))

def actualizar():
    id_detalle = txtIdActualizar.get()
    id_compra = comboCompra.get()
    id_producto = comboProducto.get()
    id_metodo_pago = comboMetodoPago.get()
    cantidad = txtCantidad.get()

    if not id_detalle or not id_compra or not id_producto or not id_metodo_pago or not cantidad:
        print("Todos los campos son obligatorios para actualizar")
        return
    
    precio = productos_dict[id_producto][1]
    subtotal = int(cantidad) * precio

    cursor.execute("UPDATE detalle_compras SET id_compra=%s, id_producto=%s, id_metodo_pago=%s, cantidad=%s, subtotal=%s WHERE id_detalle=%s", 
                   (id_compra, id_producto, id_metodo_pago, cantidad, subtotal, id_detalle))
    conexion.commit()
    print("Detalle de compra actualizado exitosamente.")
    leer()

def eliminar():
    id_detalle = txtEliminar.get()
    
    if not id_detalle:
        print("Por favor, ingresa un ID valido para eliminar")
        return

    cursor.execute("DELETE FROM detalle_compras WHERE id_detalle=%s", (id_detalle,))
    conexion.commit()
    print("Detalle de compra eliminado exitosamente.")
    leer()

# Labels y cuadros de texto
lblCompra = tkinter.Label(ventana, text="Compra:")
lblCompra.place(x=50, y=50)
comboCompra = ttk.Combobox(ventana, values=compras_lista)
comboCompra.place(x=180, y=50, width=250)

lblProducto = tkinter.Label(ventana, text="Producto:")
lblProducto.place(x=50, y=80)
comboProducto = ttk.Combobox(ventana, values=productos_lista)
comboProducto.place(x=180, y=80, width=250)

lblMetodoPago = tkinter.Label(ventana, text="Metodo de Pago:")
lblMetodoPago.place(x=50, y=110)
comboMetodoPago = ttk.Combobox(ventana, values=metodos_lista)
comboMetodoPago.place(x=180, y=110, width=250)

lblCantidad = tkinter.Label(ventana, text="Cantidad:")
lblCantidad.place(x=50, y=140)
txtCantidad = tkinter.Entry(ventana, bg="#FFC0CB")
txtCantidad.place(x=180, y=140, width=250)

lblIdActualizar = tkinter.Label(ventana, text="ID Detalle a Actualizar:")
lblIdActualizar.place(x=50, y=170)
txtIdActualizar = tkinter.Entry(ventana, bg="white")
txtIdActualizar.place(x=180, y=170, width=250)

lblEliminar = tkinter.Label(ventana, text="ID Detalle a Eliminar:")
lblEliminar.place(x=50, y=200)
txtEliminar = tkinter.Entry(ventana, bg="white")
txtEliminar.place(x=180, y=200, width=250)

# Botones CRUD
btnCrear = tkinter.Button(ventana, text="CREAR", command=crear, bg="lightgreen")
btnCrear.place(x=50, y=250, width=100)

btnLeer = tkinter.Button(ventana, text="LEER", command=leer, bg="lightblue")
btnLeer.place(x=160, y=250, width=100)

btnActualizar = tkinter.Button(ventana, text="ACTUALIZAR", command=actualizar, bg="yellow")
btnActualizar.place(x=270, y=250, width=100)

btnEliminar = tkinter.Button(ventana, text="ELIMINAR", command=eliminar, bg="red")
btnEliminar.place(x=380, y=250, width=100)

ventana.mainloop()

conexion.close()