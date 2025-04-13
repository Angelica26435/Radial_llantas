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

# Crear la ventana principal
ventana = tkinter.Tk()
ventana.geometry("700x500")
ventana.title("Catalogo de Clientes")

# Etiqueta principal
etiqueta = tkinter.Label(ventana, text="Catalogo de Clientes", font=("Arial", 14))
etiqueta.pack(pady=10)

# Crear la tabla visual con Treeview
tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Apellidos", "Correo", "Direccion", "Codigo Postal", "Ciudad", "Teléfono"), show="headings")
tabla.place(x=50, y=250, width=600, height=200)

# Definir encabezados de la tabla
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Apellidos", text="Apellidos")
tabla.heading("Correo", text="Correo")
tabla.heading("Direccion", text="Direccion")
tabla.heading("Codigo Postal", text="Codigo Postal")
tabla.heading("Ciudad", text="Ciudad")
tabla.heading("Telefono", text="Telefono")

# Funciones CRUD mejoradas
def crear():
    nombre = txtNombre.get()
    apellidos = txtApellidos.get()
    correo = txtCorreo.get()
    direccion = txtDireccion.get()
    codigo_postal = txtCodigoPostal.get()
    ciudad = txtCiudad.get()
    telefono = txtTelefono.get()
    
    cursor.execute("INSERT INTO clientes (nombre_cliente, apellidos, correo_cliente, direccion, codigo_postal, ciudad, telefono_cliente) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (nombre, apellidos, correo, direccion, codigo_postal, ciudad, telefono))
    conexion.commit()
    print("Cliente creado exitosamente.")

def leer():
    # Limpiar tabla antes de mostrar nuevos datos
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()

    # Mostrar datos en la tabla visual
    for cliente in resultados:
        tabla.insert("", "end", values=cliente)

def actualizar():
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    
    print("Tablas en la base de datos:")
    for tabla in tablas:
        print(tabla[0])

def eliminar():
    id_cliente = input("ID del cliente a eliminar: ")
    
    cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id_cliente,))
    conexion.commit()
    print("Cliente eliminado exitosamente.")

# Labels y cuadros de texto
lblNombre = tkinter.Label(ventana, text="Nombre:")
lblNombre.place(x=50, y=50)
txtNombre = tkinter.Entry(ventana, bg="#FFC0CB")
txtNombre.place(x=150, y=50, width=250)

lblApellidos = tkinter.Label(ventana, text="Apellidos:")
lblApellidos.place(x=50, y=80)
txtApellidos = tkinter.Entry(ventana, bg="#FFC0CB")
txtApellidos.place(x=150, y=80, width=250)

lblCorreo = tkinter.Label(ventana, text="Correo:")
lblCorreo.place(x=50, y=110)
txtCorreo = tkinter.Entry(ventana, bg="#FFC0CB")
txtCorreo.place(x=150, y=110, width=250)

lblDireccion = tkinter.Label(ventana, text="Direccion:")
lblDireccion.place(x=50, y=140)
txtDireccion = tkinter.Entry(ventana, bg="#FFC0CB")
txtDireccion.place(x=150, y=140, width=250)

lblCodigoPostal = tkinter.Label(ventana, text="Codigo Postal:")
lblCodigoPostal.place(x=50, y=170)
txtCodigoPostal = tkinter.Entry(ventana, bg="#FFC0CB")
txtCodigoPostal.place(x=150, y=170, width=250)

lblCiudad = tkinter.Label(ventana, text="Ciudad:")
lblCiudad.place(x=50, y=200)
txtCiudad = tkinter.Entry(ventana, bg="#FFC0CB")
txtCiudad.place(x=150, y=200, width=250)

lblTelefono = tkinter.Label(ventana, text="Telefono:")
lblTelefono.place(x=50, y=230)
txtTelefono = tkinter.Entry(ventana, bg="#FFC0CB")
txtTelefono.place(x=150, y=230, width=250)

# Botones CRUD mejorados
btnCrear = tkinter.Button(ventana, text="CREAR", command=crear, bg="lightgreen")
btnCrear.place(x=50, y=460, width=100)

btnLeer = tkinter.Button(ventana, text="LEER", command=leer, bg="lightblue")
btnLeer.place(x=160, y=460, width=100)

btnActualizar = tkinter.Button(ventana, text="ACTUALIZAR", command=actualizar, bg="yellow")
btnActualizar.place(x=270, y=460, width=100)

btnEliminar = tkinter.Button(ventana, text="ELIMINAR", command=eliminar, bg="red")
btnEliminar.place(x=380, y=460, width=100)

# Ejecutar la aplicación
ventana.mainloop()

# Cerrar conexión al salir
conexion.close()