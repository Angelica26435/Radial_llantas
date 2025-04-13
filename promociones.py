import tkinter
from tkinter import ttk  # Para la tabla y combobox
from tkcalendar import DateEntry  # Para el calendario
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

# Obtener productos desde la base de datos
cursor.execute("SELECT id_producto, nombre_producto FROM productos")
productos = cursor.fetchall()
productos_dict = {str(row[0]): row[1] for row in productos}
productos_lista = list(productos_dict.keys())

# Crear ventana principal
ventana = tkinter.Tk()
ventana.geometry("800x600")
ventana.title("Gestion de Promociones")

# Etiqueta principal
etiqueta = tkinter.Label(ventana, text="Promociones", font=("Arial", 14))
etiqueta.pack(pady=10)

# Tabla visual con Treeview
tabla = ttk.Treeview(ventana, columns=("ID Promocion", "Producto", "Descuento", "Fecha Inicio", "Fecha Fin"), show="headings")
tabla.place(x=50, y=350, width=700, height=200)

# Definir encabezados de la tabla
tabla.heading("ID Promocion", text="ID Promocion")
tabla.heading("Producto", text="Producto")
tabla.heading("Descuento", text="Descuento")
tabla.heading("Fecha Inicio", text="Fecha Inicio")
tabla.heading("Fecha Fin", text="Fecha Fin")

# Funciones CRUD
def crear():
    id_producto = comboProducto.get()
    descuento = txtDescuento.get()
    fecha_inicio = calFechaInicio.get_date()
    fecha_fin = calFechaFin.get_date()

    if not id_producto or not descuento or not fecha_inicio or not fecha_fin:
        print("Todos los campos son obligatorios")
        return
    
    try:
        descuento = float(descuento)
        if descuento <= 0 or descuento > 100:
            print("El descuento debe ser entre 1 y 100")
            return
        if fecha_inicio > fecha_fin:
            print("La fecha de inicio no puede ser posterior a la fecha de fin")
            return
    except ValueError:
        print("Revisa el formato del descuento")
        return

    cursor.execute("INSERT INTO promociones (id_producto, descuento, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)", 
                   (id_producto, descuento, fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")))
    conexion.commit()
    
    print("Promocion creada exitosamente.")
    leer()  

def leer():
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT p.id_promocion, pr.nombre_producto, p.descuento, p.fecha_inicio, p.fecha_fin FROM promociones p JOIN productos pr ON p.id_producto = pr.id_producto")
    resultados = cursor.fetchall()

    for promo in resultados:
        id_promocion, producto, descuento, fecha_inicio, fecha_fin = promo
        tabla.insert("", "end", values=(id_promocion, producto, f"{descuento:.2f}%", fecha_inicio, fecha_fin))

def actualizar():
    id_promocion = txtIdActualizar.get()
    id_producto = comboProducto.get()
    descuento = txtDescuento.get()
    fecha_inicio = calFechaInicio.get_date()
    fecha_fin = calFechaFin.get_date()

    if not id_promocion or not id_producto or not descuento or not fecha_inicio or not fecha_fin:
        print("Todos los campos son obligatorios para actualizar")
        return

    cursor.execute("UPDATE promociones SET id_producto=%s, descuento=%s, fecha_inicio=%s, fecha_fin=%s WHERE id_promocion=%s", 
                   (id_producto, descuento, fecha_inicio, fecha_fin, id_promocion))
    conexion.commit()
    print("Promoción actualizada exitosamente.")
    leer()

def eliminar():
    id_promocion = txtEliminar.get()
    
    if not id_promocion:
        print("Por favor, ingresa un ID valido para eliminar")
        return

    cursor.execute("DELETE FROM promociones WHERE id_promocion=%s", (id_promocion,))
    conexion.commit()
    print("Promocion eliminada exitosamente.")
    leer()

# Labels y cuadros de texto
lblProducto = tkinter.Label(ventana, text="Producto:")
lblProducto.place(x=50, y=50)
comboProducto = ttk.Combobox(ventana, values=productos_lista)
comboProducto.place(x=180, y=50, width=250)

lblDescuento = tkinter.Label(ventana, text="Descuento (%):")
lblDescuento.place(x=50, y=80)
txtDescuento = tkinter.Entry(ventana, bg="#FFC0CB")
txtDescuento.place(x=180, y=80, width=250)

lblFechaInicio = tkinter.Label(ventana, text="Fecha Inicio:")
lblFechaInicio.place(x=50, y=110)
calFechaInicio = DateEntry(ventana, width=18, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
calFechaInicio.place(x=180, y=110, width=250)

lblFechaFin = tkinter.Label(ventana, text="Fecha Fin:")
lblFechaFin.place(x=50, y=140)
calFechaFin = DateEntry(ventana, width=18, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
calFechaFin.place(x=180, y=140, width=250)

lblIdActualizar = tkinter.Label(ventana, text="ID Promocion a Actualizar:")
lblIdActualizar.place(x=50, y=170)
txtIdActualizar = tkinter.Entry(ventana, bg="white")
txtIdActualizar.place(x=180, y=170, width=250)

lblEliminar = tkinter.Label(ventana, text="ID Promocion a Eliminar:")
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

# Ejecutar la aplicacion
ventana.mainloop()

# Cerrar conexion al salir
conexion.close()