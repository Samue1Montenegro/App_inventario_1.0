# ALUMNO : SAMUEL MONTENEGRO

# Importa todos los modulos de tkinter para realizar la interfaz gráfica.
from tkinter import *

# Importa messagebox para poder realizar notificaciones como mensajes de alerta o confirmaciones
from tkinter import messagebox

# Importa ttk para crear widgets
from tkinter import ttk

# Importa filedialog para poder lanzar un cuadro de dialogo con el usuario y elegir un archivo o directorio
from tkinter import filedialog

# Importa simpledialog para poder lanzar un cuadro de dialogo simple, en este caso para poder modificar datos mediante un campo de entrada.
from tkinter import simpledialog

# Importa tkinter y lo renombra tk para facilitar su uso en ocasiones
import tkinter as tk

# Importa re para poder utilizar expresiones regulares, en este caso para validar campos de entrada.
import re

# ----------------------------------------------------------------------------------
# ######################      MODELO              ########################
# ----------------------------------------------------------------------------------

# Se crea el diccionario global para almacenar los datos y llamarlo de diferentes funciones.
global stock
stock = {}


# Funcion para ordenar el diccionario por medio del numero id/codigo de producto
def ordenar_stock(stock):
    return dict(sorted(stock.items(), key=lambda item: int(item[0])))


# Funcion para dar de alta un prodcuto
def alta(stock, producto, id_prod, cantidad, tree):
    # Aplicar la función regex para validar el campo producto permitiendo letras, numeros, caracteres
    patron_producto = "^[A-Za-záéíóúñÑ0-9\s/_']+$"
    # Si en el campo producto se ingresan caracteres no correspondientes se le informa con una notificación
    if not re.fullmatch(patron_producto, producto):
        mostrar_notificacion(
            "Elemento no válido. Solo letras incluida la ñ, números, caracteres /, _, ' y espacios permitidos."
        )
        print("Alta = Elemento no valido")
        return False

    # Aplicar la función regex para validar el campo id/codigo permitiendo solo numeros
    patron_id_prod = "^[0-9]+$"
    # Si en el campo cantidad se ingresan caracteres no correspondientes se le informa con una notificación
    if not re.fullmatch(patron_id_prod, id_prod):
        mostrar_notificacion("Id/Codigo no válido. Solo números enteros permitidos.")
        print("Alta = cantidad no valida")
        return False

    # Aplicar la función regex para validar el campo cantidad permitiendo solo numeros
    patron_cantidad = "^[0-9]+$"
    # Si en el campo cantidad se ingresan caracteres no correspondientes se le informa con una notificación
    if not re.fullmatch(patron_cantidad, cantidad):
        mostrar_notificacion("Cantidad no válida. Solo números enteros permitidos.")
        print("Alta = cantidad no valida")
        return False

    # Verifica si el ID del producto ya existe en el stock
    if id_prod in stock:
        # Si existe, actualiza la cantidad del producto
        stock[id_prod] = (producto, stock[id_prod][1] + cantidad)
    else:
        # Si no existe, agrega el producto al stock
        stock[id_prod] = (producto, cantidad)

    # Muestra los productos ordenados en el treeview
    actualizar_treeview()
    # Limpia campos de entrada luego de dar de alta un producto.
    limpiar_campos()
    return True


# Funcion para eliminar un elemento desde los campos de entrada
def eliminar_producto_porcampo():
    global stock

    # Tomo los valores de campos de entrada, los guardo en variables y los mando como parametros a eliminar_elemento
    entrada_prod = entrada_producto.get()
    producto_id = int(entrada_codigo.get())

    # Si el producto se encuentra en el inventario, que lo elimine.
    if producto_id in stock and stock[producto_id][0] == entrada_prod:
        del stock[producto_id]
        mostrar_notificacion("Elemento eliminado con éxito.")
        guardar_inventario(stock, "inventario.txt")
        actualizar_treeview()
    else:
        mostrar_notificacion("Hubo un error! ")

    # Limpia campos de entrada al ejecutar el boton de borrar.
    limpiar_campos()


# Funcion para eliminar un producto mediante el id/codigo, seleccionandolo desde treeview.
def eliminar_producto_seleccionado():
    # Para asegurar que se ha seleccionado un producto.
    if tree.selection():
        # Tomo los valores seleccionando el producto para eliminarlo completamente con sus valores.
        seleccion_producto = tree.selection()

        # Obtiene la información de la fila seleccionada y la separa.
        item = tree.item(seleccion_producto)
        # Identifica los valores, siendo el valor relevante el id/codigo e ignora los demas valores.
        (
            producto_id_selec,
            _,
            _,
        ) = item["values"]

        # Pregunta si el producto se encuentra en el inventario que proceda a eliminarlo.
        if producto_id_selec in stock:
            del stock[producto_id_selec]
            # Aviso en pantalla que se ha eliminado, se actualiza el inventario y el treeview.
            mostrar_notificacion("Elemento eliminado con éxito.")
            guardar_inventario(stock, "inventario.txt")
            actualizar_treeview()
        else:
            # En caso de no encontrar el producto en inventario se le notifica.
            mostrar_notificacion("No coincide el elemento! ")
    else:
        # En caso de no detectar una seleccion correcta se le notifica.
        mostrar_notificacion("No se ha seleccionado ningun elemento! ")


# Funcion para unificar eliminar por campo y eliminar por seleccion en treeview.
def eliminar_elemento():
    # Si detecta que los formularios de entrada estan vacios, acciona la funcion eliminar_producto_seleccionado
    if entrada_producto.get() == "":
        eliminar_producto_seleccionado()
    else:
        # Si detecta caracteres en los formularios, acciona la funcion eliminar_producto_porcampo.
        eliminar_producto_porcampo()


# Función para guardar el inventario en un archivo.
def guardar_inventario(stock, archivo):
    # Se abre el archivo en modo escritura asignandole el contenido a la variable f.
    with open(archivo, "w") as f:
        # Escribe en el archivo el ID, producto y cantidad en la lista del diccionario.
        for id_prod, (producto, cantidad) in stock.items():
            f.write(f"{id_prod},{producto},{cantidad}\n")


# Función para manejar el botón de guardar.
def guardar_inventario_actualizado():
    global stock
    # Guarda el inventario actualizado.
    guardar_inventario(stock, "inventario.txt")
    # Muestra una notificación indicando que se guardaron los cambios.
    mostrar_notificacion("Inventario guardado con éxito.")


# Función para cargar el inventario desde un archivo.
def cargar_inventario(archivo):
    global stock
    stock = {}
    # Se abre el archivo en modo lectura asignandole el contenido a la variable f.
    with open(archivo, "r") as f:
        for linea in f:
            # .strip se utiliza para eliminar espacios en blanco adicionales.
            # .split se utiliza para dividir la línea en una lista de valores utilizando la coma como delimitador
            producto_id, producto, cantidad = linea.strip().split(",")
            stock[int(producto_id)] = (producto, int(cantidad))

        # Si no encuentra el archivo se le notifica.
        if not archivo:
            mostrar_notificacion("El archivo no existe, se creara uno.")

    return stock


# Función para modificar un elemento del inventario.
def modificar_producto(producto_id, nueva_cantidad, nuevo_producto):
    global stock
    # Verifica si el ID del producto está en el inventario.
    if producto_id in stock:
        # Actualiza la cantidad asociada al ID del producto.
        stock[producto_id] = (nuevo_producto, nueva_cantidad)
        # Muestra una notificación de éxito.
        mostrar_notificacion("Producto modificado con éxito!")
    else:
        # Muestra una notificación si el producto no está en el inventario.
        mostrar_notificacion(
            f"El producto con ID {producto_id} no está en el inventario."
        )


# ----------------------------------------------------------------------------------
# ######################       VISTA                ########################
# ----------------------------------------------------------------------------------
# Se crea la ventana, se le asigna a una variable y se le ingresa un nombre.
root = Tk()
root.title("Inventario")

# Titulo general de la aplicacion.
titulo = Label(
    root,
    text="INGRESE SUS PRODUCTOS",
    bg="#00758f",
    fg="white",
    height=3,
    width=60,
)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W + E)

# Titulos que indican en la entrada de datos en productos y configuracion de posicion.
producto = Label(root, text="PRODUCTO")
producto.grid(row=1, column=0, sticky=W)

# Titulos que indican en la entrada de datos en cantidad y configuracion de posicion.
cantidad = Label(root, text="CANTIDAD")
cantidad.grid(row=2, column=0, sticky=W)

# Titulos que indican en la entrada de datos en codigo del producto y configuracion de posicion.
id_prod = Label(root, text="CODIGO")
id_prod.grid(row=3, column=0, sticky=W)

# Defino variables para tomar valores de campos de entrada.
producto_val, cantidad_val, codigo_val = StringVar(), IntVar(), IntVar()
w_ancho = 40

# Defino variables globales a las variables que contengan entry para luego ser utilizadas por funciones.
global entrada_producto, entrada_cantidad, entrada_codigo

# Formulario para Campo de entrada de producto.
entrada_producto = Entry(root, textvariable=producto_val, width=w_ancho)
entrada_producto.grid(row=1, column=1)

# Formulario para Campo de entrada en cantidad del producto.
entrada_cantidad = Entry(root, textvariable=cantidad_val, width=w_ancho)
entrada_cantidad.grid(row=2, column=1)

# Formularios para Campo de entrada del codigo del producto.
entrada_codigo = Entry(root, textvariable=codigo_val, width=w_ancho)
entrada_codigo.grid(row=3, column=1)

# Crea una etiqueta y un campo de entrada para la consulta de un producto.
global consulta_label, consulta_entry
consulta_label = Label(root, text="CONSULTA DEL PRODUCTO")
consulta_label.grid(row=4, column=0, sticky=W)
consulta_entry = Entry(root, width=w_ancho)
consulta_entry.grid(row=4, column=1)


# ----------------------------------------------------------------------------------
# ######################      CONTROLADOR              ########################
# ----------------------------------------------------------------------------------


#  Funcion para limpiar campos de entrada luego de utilizarlos.
def limpiar_campos():
    entrada_producto.delete(0, tk.END)
    entrada_codigo.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)


# Función para agregar un elemento al inventario y actualizar la pantalla.
def guardar_y_mostrar():
    global stock, tree

    # Obtener valores de los campos de entrada.
    id_prod = entrada_codigo.get()
    producto = entrada_producto.get()
    cantidad = entrada_cantidad.get()

    # Llama a la función alta
    if alta(stock, producto, id_prod, cantidad, tree) is True:
        # Mostrar notificación de éxito solo si la función alta retorna True.
        mostrar_notificacion("Se ha agregado el producto con éxito!")
        # Guarda valores en archivo inventario.
        guardar_inventario(stock, "inventario.txt")
        # Llama a la funcion para limpiar campos de entrada y luego actualiza el treview.
        limpiar_campos()
        actualizar_treeview()


# Función para mostrar el inventario actualizado en el treeview, ya sea creado o modificado.
def actualizar_treeview():
    global tree
    global stock
    # Elimina todas las filas existentes en el treeview para actualizarlo.
    for item in tree.get_children():
        tree.delete(item)

    # Variable para identidicar las filas pares de las impares.
    fondo_par = True

    # Agrega las filas actualizadas al treeview.
    for producto_id, (producto, cantidad) in ordenar_stock(stock).items():
        # Inserta una nueva fila en el treeview con los valores del producto actual.
        tree.insert(
            "",  # El primer argumento es el ID.
            "end",  # El segundo argumento es la posición donde se insertará la nueva fila.
            # Los valores de las columnas para la nueva fila.
            values=(
                producto_id,
                producto,
                cantidad,
            ),
            # Etiqueta que determina el color de fondo de la fila.
            tags=(
                "odd" if fondo_par else "even"
            ),  # Se utilizan las etiquetas "odd" y "even" para poder asignarles configuraciones de color.
        )
        fondo_par = not fondo_par  # Alterna el fondo para la próxima fila.

        # Agrega los colores de fondo para las filas impares y pares.
        tree.tag_configure("odd", background="#E8E8E8")  # Fondo gris claro.
        tree.tag_configure("even", background="white")  # Fondo blanco.


# Funcion para poder limpiar el campo de entrada luego de realizar la consulta.
def limpiar_campo_consulta():
    consulta_entry.delete(0, tk.END)


# Función para realizar la consulta y mostrar los resultados en el treeview de consulta.
def realizar_consulta():
    global consulta_entry, tree, inventario

    # Obtiene la palabra clave de la entrada de consulta.
    # Toma la palabra clave y se convierte a minúsculas.
    # .strip() verifica si el campo de consulta no esta vacio
    palabra_clave = consulta_entry.get().lower().strip()

    # Inicializa la variable resultados en una lista vacia.
    resultados = []

    # Recopila los valores coincidentes en una lista.
    if palabra_clave:
        resultados = [
            (producto_id, elemento, cantidad)
            for producto_id, (elemento, cantidad) in inventario.items()
            if palabra_clave in elemento.lower()
        ]

        # Limpia el treeview de consulta antes de agregar nuevos resultados.
        for i in tree.get_children():
            tree.delete(i)

        # Agrega los resultados al treeview de consulta.
        for resultado in resultados:
            tree.insert("", "end", values=resultado, tags=(resultado[0] % 2))
        # Luego de realizar la consulta limpia el formulario de entrada.
        limpiar_campo_consulta()
    else:
        # Si no se encuentra ninguna busqueda en campo consulta realiza una notificacion
        mostrar_notificacion(
            " No ha ingresado la palabra clave\n Recuerde que puede consultar por nombre o id"
        )


# Función para modificar un elemento seleccionado.
def modificar_seleccionado():
    global tree
    # Obtiene la selección actual en el treeview de consulta.
    seleccion = tree.selection()

    # Verifica si hay una selección.
    if seleccion:
        # Obtiene la información de la fila seleccionada.
        item = tree.item(seleccion)
        producto_id, producto, cantidad = item["values"]

        # Muestra un cuadro de diálogo para ingresar la nueva cantidad. askstring lo convierte en cadena de caracteres.
        nuevo_producto = simpledialog.askstring(
            "Modificar Nombre",
            f"Ingrese el nuevo nombre para el producto (ID: {producto_id}):",  # Posiciona el producto.
            initialvalue=producto,  # El valor de entrada para modificar es el nombre del producto.
        )

        # Muestra un cuadro de diálogo para ingresar nuevo nombre. askinteger lo convierte en entero.
        nueva_cantidad = simpledialog.askinteger(
            "Modificar Cantidad",
            f"Ingrese la nueva cantidad para {producto} (ID: {producto_id}):",  # Posiciona al producto y su id/codigo
            initialvalue=cantidad,  # El valor de entrada para modificar es el id/codigo del producto.
        )

        # Verifica si se ingresó una nueva cantidad.
        if nueva_cantidad is not None and nuevo_producto is not None:
            # Realiza la modificación en el inventario.
            modificar_producto(producto_id, nueva_cantidad, nuevo_producto)
            # Actualiza el treeview de consulta.
            actualizar_treeview()
    else:
        mostrar_notificacion("No se ha seleccionado ningun producto")


# Función para abrir el archivo donde se guardan los datos/inventario.
def abrir_archivo():
    global stock
    # Abre un cuadro de diálogo para que el usuario seleccione un archivo en el que contenga la estructura....
    # .... Id/Codigo , Producto , Cantidad.
    archivo = filedialog.askopenfilename(
        initialdir="/",
        title="Seleccionar archivo",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
    )
    # Verifica si se seleccionó un archivo.
    if archivo:
        # Carga el inventario desde el archivo.
        stock.clear()  # Limpia el inventario actual.
        # Actualiza el inventario con los datos del archivo.
        stock.update(cargar_inventario(archivo))
        # Muestra el inventario en el treeview.
        actualizar_treeview()


# Funcion para poder mostrar notificaciones.
def mostrar_notificacion(mensaje):
    messagebox.showinfo("Notificación", mensaje)


# ----------------------------------------------------------------------------------
# ######################          TREEVIEW             ######################
# ----------------------------------------------------------------------------------
# Crea el treeview para mostrar el inventario en la ventana
global tree

# Se le pasa como parametro al treeview la variable root, las columnas que contiene....
# .... y el argumento show para indicarle que solo muestre las columnas deseadas
tree = ttk.Treeview(root, columns=("ID", "Producto", "Cantidad"), show="headings")

# Columnas para Producto, codigo y cantidad
tree["columns"] = ("ID", "Producto", "Cantidad")
tree.column("ID", width=100, minwidth=50, anchor=CENTER)
tree.column("Producto", width=300, minwidth=80, anchor=CENTER)
tree.column("Cantidad", width=300, minwidth=80, anchor=CENTER)

# Nombre de columnas
tree.heading("ID", text="CODIGO")
tree.heading("Producto", text="PRODUCTO")
tree.heading("Cantidad", text="CANTIDAD")
tree.grid(row=10, column=0, columnspan=4)

# Crea la barra de deslizamiento vertical.
tree_scrollbar = Scrollbar(root, command=tree.yview)
tree.configure(yscrollcommand=tree_scrollbar.set)
tree_scrollbar.grid(row=10, column=4, sticky="ns")

# Crea una barra de separacion
separador = ttk.Separator(
    root,
    orient=HORIZONTAL,
)
separador.grid(row=6, pady=4)
# Muestra el inventario en el treeview después de cargarlo al iniciar la aplicacion.
archivo = filedialog.askopenfilename(
    title="Abrir archivo",
    filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
)
if archivo:
    inventario = cargar_inventario(archivo)
    mostrar_notificacion("Inventario cargado con éxito.")
# Llama a la funcion para actrualizar el treeview
actualizar_treeview()

# Boton para dar de alta un producto
global boton_alta
boton_alta = Button(
    root,
    text="Agregar",
    width=10,
    activeforeground="green",
    command=lambda: guardar_y_mostrar(),
)
boton_alta.grid(row=1, column=2)

# Boton para borrar un producto
global boton_borrar
boton_borrar = Button(
    root,
    text="Borrar",
    width=10,
    activeforeground="red",
    command=lambda: eliminar_elemento(),
)
boton_borrar.grid(row=2, column=2, pady=(1, 0))

# Crea el botón para modificar el elemento seleccionado O ingresando en los campos de producto y codigo.
global modificar_boton
modificar_boton = Button(
    root,
    text="Modificar Producto",
    activeforeground="cyan",
    command=lambda: modificar_seleccionado(),
)
modificar_boton.grid(row=3, column=2, pady=(1, 0))

# Boton para realizar una consulta sobre un producto.
global boton_consulta
boton_consulta = Button(
    root,
    text="Consultar",
    width=10,
    activeforeground="yellow",
    command=lambda: realizar_consulta(),
)
boton_consulta.grid(row=4, column=2, pady=(1, 0))

# Boton para poder actualizar el inventario luego de realizar una consulta.
global boton_actualizar
boton_consulta = Button(
    root,
    text="Actualizar",
    width=10,
    activeforeground="deep pink",
    command=lambda: actualizar_treeview(),
)
boton_consulta.grid(row=5, column=2, pady=(1, 0))

# Botón para abrir el archivo del inventario en caso de ser necesario.
global abrir_archivo_boton
abrir_archivo_boton = Button(
    root,
    text="Abrir Archivo",
    activeforeground="violet",
    command=lambda: abrir_archivo(),
)
abrir_archivo_boton.grid(row=1, column=3)

# Botón para guardar el inventario.
boton_guardar = Button(
    root,
    text="Guardar",
    width=10,
    activeforeground="blue",
    command=lambda: guardar_inventario_actualizado(),
)
boton_guardar.grid(row=2, column=3, pady=(1, 0))


# Bucle principal
root.mainloop()
