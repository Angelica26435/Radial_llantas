import tkinter
from tkinter import ttk  # Para la tabla y el combobox
import mysql.connector

# Conectar a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Radial_llantas"
)
cursor = conexion.cursor()

# Obtener proveedores desde la base de datos
cursor.execute("SELECT id_proveedor, nombre_proveedor FROM proveedores")
proveedores = cursor.fetchall()
proveedores_dict = {str(row[0]): row[1] for row in proveedores}  # Diccionario ID: Nombre
proveedores_lista = list(proveedores_dict.keys())  # Solo IDs para el Combobox

# Crear ventana principal
ventana = tkinter.Tk()
ventana.geometry("850x600")
ventana.title("Gestion de Productos")

# Etiqueta principal
etiqueta = tkinter.Label(ventana, text="Catalogo de Productos", font=("Arial", 14))
etiqueta.pack(pady=10)

# Tabla visual con Treeview
tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Descripcion", "Precio", "Stock", "Tipo Producto", "Proveedor"), show="headings")
tabla.place(x=50, y=350, width=750, height=200)

# Definir encabezados de la tabla
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Descripcion", text="Descripcion")
tabla.heading("Precio", text="Precio")
tabla.heading("Stock", text="Stock")
tabla.heading("Tipo Producto", text="Tipo Producto")
tabla.heading("Proveedor", text="Proveedor")

# Funciones CRUD
def crear():
    nombre = txtNombre.get()
    descripcion = txtDescripcion.get()
    precio = txtPrecio.get()
    stock = txtStock.get()
    tipo_producto = comboTipoProducto.get()
    id_proveedor = comboProveedor.get()  # Selección desde el combobox
    
    if not nombre or not descripcion or not precio or not stock or not tipo_producto or not id_proveedor:
        print("Todos los campos son obligatorios")
        return
    
    try:
        precio = float(precio)
        stock = int(stock)
        if precio < 0 or stock < 0:
            print("El precio y el stock deben ser positivos")
            return
    except ValueError:
        print("Precio y stock deben ser numeros validos")
        return

    cursor.execute("INSERT INTO productos (nombre_producto, descripcion, precio, stock, tipo_producto, id_proveedor) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (nombre, descripcion, precio, stock, tipo_producto, id_proveedor))
    conexion.commit()
    
    print("Producto creado exitosamente.")
    leer()  # Actualizar la tabla después de crear

def leer():
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT p.id_producto, p.nombre_producto, p.descripcion, p.precio, p.stock, p.tipo_producto, pr.nombre_proveedor FROM productos p JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor")
    resultados = cursor.fetchall()

    for producto in resultados:
        id_producto, nombre, descripcion, precio, stock, tipo_producto, proveedor = producto
        tabla.insert("", "end", values=(id_producto, nombre, descripcion, f"${precio:.2f}", stock, tipo_producto, proveedor))

def actualizar():
    id_producto = txtIdActualizar.get()
    nombre = txtNombre.get()
    descripcion = txtDescripcion.get()
    precio = txtPrecio.get()
    stock = txtStock.get()
    tipo_producto = comboTipoProducto.get()
    id_proveedor = comboProveedor.get()

    if not id_producto or not nombre or not descripcion or not precio or not stock or not tipo_producto or not id_proveedor:
        print("Todos los campos son obligatorios para actualizar")
        return
    
    cursor.execute("UPDATE productos SET nombre_producto=%s, descripcion=%s, precio=%s, stock=%s, tipo_producto=%s, id_proveedor=%s WHERE id_producto=%s", 
                   (nombre, descripcion, precio, stock, tipo_producto, id_proveedor, id_producto))
    conexion.commit()
    print("Producto actualizado exitosamente.")
    leer()

def eliminar():
    id_producto = txtEliminar.get()
    
    if not id_producto:
        print("Por favor, ingresa un ID valido para eliminar")
        return

    cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
    conexion.commit()
    print("Producto eliminado exitosamente.")
    leer()

# Labels y cuadros de texto
lblNombre = tkinter.Label(ventana, text="Nombre:")
lblNombre.place(x=50, y=50)
txtNombre = tkinter.Entry(ventana, bg="#FFC0CB")
txtNombre.place(x=180, y=50, width=250)

lblDescripcion = tkinter.Label(ventana, text="Descripcion:")
lblDescripcion.place(x=50, y=80)
txtDescripcion = tkinter.Entry(ventana, bg="#FFC0CB")
txtDescripcion.place(x=180, y=80, width=250)

lblPrecio = tkinter.Label(ventana, text="Precio:")
lblPrecio.place(x=50, y=110)
txtPrecio = tkinter.Entry(ventana, bg="#FFC0CB")
txtPrecio.place(x=180, y=110, width=250)

lblStock = tkinter.Label(ventana, text="Stock:")
lblStock.place(x=50, y=140)
txtStock = tkinter.Entry(ventana, bg="#FFC0CB")
txtStock.place(x=180, y=140, width=250)

lblTipoProducto = tkinter.Label(ventana, text="Tipo Producto:")
lblTipoProducto.place(x=50, y=170)
comboTipoProducto = ttk.Combobox(ventana, values=["llanta", "poliza", "servicio"])
comboTipoProducto.place(x=180, y=170, width=250)

lblProveedor = tkinter.Label(ventana, text="Proveedor:")
lblProveedor.place(x=50, y=200)
comboProveedor = ttk.Combobox(ventana, values=proveedores_lista)
comboProveedor.place(x=180, y=200, width=250)

lblIdActualizar = tkinter.Label(ventana, text="ID Producto a Actualizar:")
lblIdActualizar.place(x=50, y=230)
txtIdActualizar = tkinter.Entry(ventana, bg="white")
txtIdActualizar.place(x=180, y=230, width=250)

lblEliminar = tkinter.Label(ventana, text="ID Producto a Eliminar:")
lblEliminar.place(x=50, y=260)
txtEliminar = tkinter.Entry(ventana, bg="white")
txtEliminar.place(x=180, y=260, width=250)

# Botones CRUD mejorados
btnCrear = tkinter.Button(ventana, text="CREAR", command=crear, bg="lightgreen")
btnCrear.place(x=50, y=300, width=100)

btnLeer = tkinter.Button(ventana, text="LEER", command=leer, bg="lightblue")
btnLeer.place(x=160, y=300, width=100)

btnActualizar = tkinter.Button(ventana, text="ACTUALIZAR", command=actualizar, bg="yellow")
btnActualizar.place(x=270, y=300, width=100)

btnEliminar = tkinter.Button(ventana, text="ELIMINAR", command=eliminar, bg="red")
btnEliminar.place(x=380, y=300, width=100)

# Ejecutar 
ventana.mainloop()

conexion.close()