import tkinter
from tkinter import ttk  # Para la tabla
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
ventana.geometry("700x500")
ventana.title("Proveedores")

# Etiqueta principal
etiqueta = tkinter.Label(ventana, text="Catalogo de Proveedores", font=("Arial", 14))
etiqueta.pack(pady=10)

# Crear tabla visual con Treeview
tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Contacto", "Teleono"), show="headings")
tabla.place(x=50, y=250, width=600, height=200)

# Definir encabezados de la tabla
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Contacto", text="Contacto")
tabla.heading("Telefono", text="Telefono")

# Funciones CRUD
def crear():
    nombre = txtNombre.get()
    contacto = txtContacto.get()
    telefono = txtTelefono.get()
    
    # Validar datos antes de insertar
    if not nombre or not contacto or not telefono:
        print("Todos los campos son obligatorios")
        return
    
    cursor.execute("INSERT INTO proveedores (nombre_proveedor, contacto_proveedor, telefono_proveedor) VALUES (%s, %s, %s)", 
                   (nombre, contacto, telefono))
    conexion.commit()
    print("Proveedor creado exitosamente.")
    leer()  # Actualizar la tabla

def leer():
    # Limpiar tabla antes de mostrar nuevos datos
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT * FROM proveedores")
    resultados = cursor.fetchall()

    # Mostrar datos en la tabla visual
    for proveedor in resultados:
        tabla.insert("", "end", values=proveedor)

def actualizar():
    id_proveedor = txtIdActualizar.get()
    nombre = txtNombre.get()
    contacto = txtContacto.get()
    telefono = txtTelefono.get()
    
    if not id_proveedor or not nombre or not contacto or not telefono:
        print("Todos los campos son obligatorios para actualizar")
        return
    
    cursor.execute("UPDATE proveedores SET nombre_proveedor=%s, contacto_proveedor=%s, telefono_proveedor=%s WHERE id_proveedor=%s", 
                   (nombre, contacto, telefono, id_proveedor))
    conexion.commit()
    print("Proveedor actualizado exitosamente.")
    leer()

def eliminar():
    id_proveedor = txtIdEliminar.get()
    
    if not id_proveedor:
        print("Por favor, ingresa un ID valido para eliminar")
        return

    cursor.execute("DELETE FROM proveedores WHERE id_proveedor=%s", (id_proveedor,))
    conexion.commit()
    print("Proveedor eliminado exitosamente.")
    leer()

# Labels y cuadros de texto
lblNombre = tkinter.Label(ventana, text="Nombre:")
lblNombre.place(x=50, y=50)
txtNombre = tkinter.Entry(ventana, bg="#FFC0CB")
txtNombre.place(x=180, y=50, width=250)

lblContacto = tkinter.Label(ventana, text="Contacto:")
lblContacto.place(x=50, y=80)
txtContacto = tkinter.Entry(ventana, bg="#FFC0CB")
txtContacto.place(x=180, y=80, width=250)

lblTelefono = tkinter.Label(ventana, text="Telefono:")
lblTelefono.place(x=50, y=110)
txtTelefono = tkinter.Entry(ventana, bg="#FFC0CB")
txtTelefono.place(x=180, y=110, width=250)

lblIdActualizar = tkinter.Label(ventana, text="ID a Actualizar:")
lblIdActualizar.place(x=50, y=140)
txtIdActualizar = tkinter.Entry(ventana, bg="white")
txtIdActualizar.place(x=180, y=140, width=250)

lblIdEliminar = tkinter.Label(ventana, text="ID a Eliminar:")
lblIdEliminar.place(x=50, y=170)
txtIdEliminar = tkinter.Entry(ventana, bg="white")
txtIdEliminar.place(x=180, y=170, width=250)

# Botones CRUD
btnCrear = tkinter.Button(ventana, text="CREAR", command=crear, bg="lightgreen")
btnCrear.place(x=50, y=200, width=100)

btnLeer = tkinter.Button(ventana, text="LEER", command=leer, bg="lightblue")
btnLeer.place(x=160, y=200, width=100)

btnActualizar = tkinter.Button(ventana, text="ACTUALIZAR", command=actualizar, bg="yellow")
btnActualizar.place(x=270, y=200, width=100)

btnEliminar = tkinter.Button(ventana, text="ELIMINAR", command=eliminar, bg="red")
btnEliminar.place(x=380, y=200, width=100)

# Ejecutar la aplicación
ventana.mainloop()

# Cerrar conexión al salir
conexion.close()