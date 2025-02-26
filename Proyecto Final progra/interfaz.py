import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, simpledialog
from main import Cliente, cargar_clientes, guardar_clientes
import random
from main import materiales_disponibles, mensajes_finales
from main import cargar_historial, clientes_registrados

mi_fuente = ('Comic Sans MS', 14)

clientes_registrados = cargar_clientes()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("App de Reciclaje ♻️😊")  # Título de la ventana
ventana.geometry("400x400")  # Tamaño de la ventana (ancho x alto)
ventana.config(bg="white") # bg cambiar el color de la ventana 

# Etiqueta de bienvenida
etiqueta_bienvenida = tk.Label(ventana, text="Bienvenido al Menú del Reciclaje :)", font=mi_fuente,bg="#A3D39C", fg='black')
etiqueta_bienvenida.pack(pady=10)  # Espacio vertical


# Funciones para los botones
def registrar_clientes():
    id_cliente = simpledialog.askinteger("Registro", "Ingrese el ID del cliente:")
    if id_cliente is None:
        return
    nombre_cliente = simpledialog.askstring("Registro", "Ingrese el nombre y apellido del cliente:")
    if not nombre_cliente:
        return
    nuevo_cliente = Cliente(id_cliente, nombre_cliente)
    clientes_registrados.append(nuevo_cliente)

    guardar_clientes(clientes_registrados)
    messagebox.showinfo("Registro", f"El cliente {nombre_cliente} se ha registrado correctamente. ID asignado: {id_cliente}")


def ver_clientes():
    if not clientes_registrados:
        messagebox.showinfo("Clientes", "No hay clientes registrados.")
        return
    lista_clientes = "\n".join([f"ID: {c.id_cliente}, Nombre: {c.nombre_cliente}, Puntos: {c.puntos}" for c in clientes_registrados])
    messagebox.showinfo("Clientes Registrados", lista_clientes)
    

def mostrar_mensaje():
    mensaje = random.choice(mensajes_finales) 
    ventana_mensaje = tk.Toplevel(ventana)
    ventana_mensaje.title("Mensaje Motivacional")
    ventana_mensaje.geometry("300x150")
    etiqueta_mensaje = tk.Label(ventana_mensaje, text=mensaje, wraplength=280, font=("Comic Sans MS", 12), fg='black', bg="#D2E8B2" ) # wraplength = ancho en pixeles
    etiqueta_mensaje.pack(pady=20) # agrega espacio
    boton_cerrar = tk.Button(ventana_mensaje, text="Cerrar", command=ventana_mensaje.destroy, font= "Comic Sans MS")
    boton_cerrar.pack()

def reciclar():
    if not clientes_registrados:
        messagebox.showwarning("Error", "No hay clientes registrados.")
        return

    id_cliente = simpledialog.askinteger("Reciclar", "Ingrese el ID del cliente que reciclará:")
    if id_cliente is None:
        return  # Si se cancela, no sigue

    cliente = next((c for c in clientes_registrados if c.id_cliente == id_cliente), None)
    if not cliente:
        messagebox.showerror("Error", "Cliente no encontrado.")
        return

    materiales_lista = "\n".join(f"ID: {m.id_material} - {m.nombre_material} ({m.puntos_por_kg} puntos/kg)" for m in materiales_disponibles)
    id_material = simpledialog.askinteger("Reciclar", f"Seleccione el ID del material:\n{materiales_lista}")
    if id_material is None:
        return

    material = next((m for m in materiales_disponibles if m.id_material == id_material), None)
    if not material:
        messagebox.showerror("Error", "Material no encontrado.")
        return

    kg_reciclados = simpledialog.askfloat("Reciclar", f"Ingrese la cantidad en kg de {material.nombre_material} reciclado:")
    if kg_reciclados is None or kg_reciclados <= 0:
        messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
        return

    puntos_ganados = material.puntos_por_kg * kg_reciclados
    cliente.puntos += puntos_ganados

    mensaje = f"{cliente.nombre_cliente} recicló {kg_reciclados} kg de {material.nombre_material} y ganó {puntos_ganados} puntos.\n\nTotal de puntos acumulados: {cliente.puntos}"
    guardar_clientes(clientes_registrados)

    messagebox.showinfo("Reciclaje Exitoso", mensaje)
    mostrar_mensaje()  # Llamar a la función para mostrar el mensaje motivacional



def ver_historial():
    def buscar():
        cliente_id = entry_id.get()
        if not cliente_id.isdigit():
            messagebox.showerror("Error", "Ingrese un ID válido.")
            return
        
        cliente_id = int(cliente_id)
        historial = cargar_historial()
        historial_cliente = [registro for registro in historial if registro.historial_cliente_id == cliente_id]

        if not historial_cliente:
            messagebox.showinfo("Historial", f"No hay registros para el cliente con ID {cliente_id}.")
            return

        cliente = next((c for c in clientes_registrados if c.id_cliente == cliente_id), None)
        cliente_nombre = cliente.nombre_cliente if cliente else "Desconocido"

        historial_texto = f"Historial de {cliente_nombre} (ID {cliente_id}):\n\n"
        for registro in historial_cliente:
            material = next((m for m in materiales_disponibles if m.id_material == registro.historial_material_id), None)
            material_nombre = material.nombre_material if material else "Desconocido"
            historial_texto += f"- {material_nombre} | {registro.historial_fecha_entrega} | {registro.historial_cantidad_reciclada} kg\n"

        messagebox.showinfo("Historial del Cliente", historial_texto)

    ventana_busqueda = tk.Toplevel()
    ventana_busqueda.geometry("400x300") #pixeles de ancho y alto 
    ventana_busqueda.geometry("+500+200")
    ventana_busqueda.title("Buscar Historial")
    tk.Label(ventana_busqueda, text="Ingrese ID del Cliente:", font=("Comic Sans MS", 12)).pack(pady=5)
    entry_id = tk.Entry(ventana_busqueda, font=("Comic Sans MS", 12))
    entry_id.pack(pady=5)
    tk.Button(ventana_busqueda, text="Buscar", command=buscar, font=("Comic Sans MS", 12), bg="white", fg="black").pack(pady=10)

# Botones para navegar en la aplicación
boton_registrar = tk.Button(ventana, text="Registrar cliente", width=20, command=registrar_clientes, font=("Comic Sans MS", 12), bg='lightpink', fg='black')
boton_registrar.pack(pady=5)

boton_ver_clientes = tk.Button(ventana, text="Ver clientes registrados", width=20, command=ver_clientes, font=("Comic Sans MS", 12), bg='lightpink', fg='black')
boton_ver_clientes.pack(pady=5)

boton_reciclar = tk.Button(ventana, text="Reciclar", width=20, command=reciclar, font=("Comic Sans MS", 12), bg='lightpink', fg='black')
boton_reciclar.pack(pady=5)


boton_historial = tk.Button(ventana, text="Ver historial de reciclaje", width=20, command=ver_historial, font=("Comic Sans MS", 12), bg='lightpink', fg='black')
boton_historial.pack(pady=5)


# Botón para salir del programa
boton_salir = tk.Button(ventana, text="Salir", width=20, command=ventana.quit, font=("Comic Sans MS", 12), bg='lightpink', fg='black')
boton_salir.pack(pady=20)

# Iniciar la aplicación
ventana.mainloop()
