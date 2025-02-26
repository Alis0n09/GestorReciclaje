import json
import os
from datetime import datetime
import random


class Cliente:
    def __init__(self, id_cliente, nombre_cliente, puntos=0):
        self.id_cliente = id_cliente
        self.nombre_cliente = nombre_cliente
        self.puntos = puntos


clientes_registrados = []


def registrar_clientes():
    id_cliente = int(input("Ingrese el Id del cliente a registrar: "))
    nombre_cliente = input("Ingrese el nombre y apellido del cliente: ")
    nuevo_cliente = Cliente(id_cliente, nombre_cliente)
    clientes_registrados.append(nuevo_cliente)
    print(f"El cliente {nombre_cliente} se ha registrado con éxito. ID asignado: {id_cliente}")

    guardar_clientes(clientes_registrados)


def mostrar_clientes():
    if not clientes_registrados:
        print("No hay clientes registrados")
    else:
        for cliente in clientes_registrados:
            print(f"ID: {cliente.id_cliente}, Nombre: {cliente.nombre_cliente}, Puntos: {cliente.puntos}")


def guardar_clientes(clientes):
    with open("clientes.json", "w") as archivo:
        json.dump([cliente.__dict__ for cliente in clientes], archivo, indent=4)


def cargar_clientes():
    if not os.path.exists("clientes.json"):
        return []

    with open("clientes.json", "r", encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)
            return [Cliente(**cliente) for cliente in datos]
        except json.JSONDecodeError:
            return []



class Material:
    def __init__(self, id_material, nombre_material, puntos_por_kg):
        self.id_material = id_material
        self.nombre_material = nombre_material
        self.puntos_por_kg = puntos_por_kg


materiales_disponibles = [
    Material(1, "Papel", 1),
    Material(2, "Plástico", 2),
    Material(3, "Cartón", 1.5)
]


mensajes_finales = [
    "¡Muchas gracias por reciclar, por cada kg de papel estas salvando 17 árboles. 🌱! ",
    "Cada papel reciclado salva árboles que purifican nuestro aire. 🍃 ¡Gracias por tu aporte!",
    "¡Felicidadesss, por cada kg de plástico contribuyes a ahorrar 10 litros de petroleo. 😃! ",
    "¡Gracias por contribuir a salvar el planeta, por cada kg de cartón estas salvando 18 árboles. 🌱!",
    "¡Gracias por reciclar! Estás ayudando a reducir la contaminación. 🌍",
    "Cada pequeño gesto cuenta. ¡Sigue haciendo la diferencia! ♻️",
    "¡Gracias por reciclar! Estás ayudando a reducir el cambio climático. ☀️❄️",
    "Gracias por cuidar el futuro de las próximas generaciones. 🌿",
    "¡Tus acciones cuentan! Reciclar es sembrar esperanza para el futuro. 🌱",
    "Reciclar no cambia el mundo de inmediato, pero cambia el tuyo y eso es el comienzo. 🌍",
    "El planeta sonríe cada vez que reciclas. ¡Muchas gracias! 😊🌎",
    "Reciclar papel puede ahorrar hasta un 60% de energía. Sigue asi!! 😃 ",
    "Cuidar el planeta es tan sencillo como reciclar. ♻️ Lo haces íncreible 😃",
    "Asegúrate de limpiar los envases antes de reciclar para evitar la contaminación de otros materiales. 🚿",
    "Reciclar es genial, pero reducir y reutilizar es aún mejor. ¡Piensa en cómo darle una segunda vida a tus objetos! 🔄",
    "Usa bolsas reutilizables cuando hagas compras. ¡Es un pequeño cambio con gran impacto! 👜",
    "El agua es un recurso valioso. Recicla, pero también cuida el consumo de agua en casa. 💧",
    "Habla con tu familia y amigos sobre la importancia del reciclaje. ¡El cambio empieza en casa! 🏡",
    "Involucra a los niños en el proceso de reciclaje. ¡Así crecerán con conciencia ambiental! 👧👦",

]


def mostrar_mensajes():
    mensaje = random.choice(mensajes_finales)  
    print(mensaje)


def reciclar_material(cliente, material_seleccionado):
    kg_reciclados = float(input(f"Ingrese la cantidad en kg de {material_seleccionado.nombre_material} reciclado: "))

    if kg_reciclados <= 0:
        print("La cantidad debe ser mayor a 0.")
        return

    puntos_ganados = material_seleccionado.puntos_por_kg * kg_reciclados
    cliente.puntos += puntos_ganados

    print(
        f"{cliente.nombre_cliente} recicló {kg_reciclados} kg de {material_seleccionado.nombre_material} y ganó {puntos_ganados} puntos.")
    print(f"Total de puntos acumulados: {cliente.puntos}")

    mostrar_mensajes()    

    guardar_clientes(clientes_registrados)

    historial_reciclaje.append(Historial(cliente.id_cliente, material_seleccionado.id_material,
                                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"), kg_reciclados))

    guardar_historial(historial_reciclaje)

   


def reciclar():
    if not clientes_registrados:
        print("No hay clientes registrados.")
        return

    for cliente in clientes_registrados:
        print(
            f"Cliente registrado:\n Id del cliente: {cliente.id_cliente}. Nombre: {cliente.nombre_cliente} ({cliente.puntos} puntos)")

    id_cliente = int(input("Ingrese el ID del cliente que reciclará: "))
    cliente = next((c for c in clientes_registrados if c.id_cliente == id_cliente), None)

    if cliente:
        for material in materiales_disponibles:
            print(
                f"ID: {material.id_material} - Material: {material.nombre_material} - Puntos por kg: {material.puntos_por_kg}")

        id_material = int(input("Ingrese el ID del material que desea reciclar: "))
        material_seleccionado = next((m for m in materiales_disponibles if m.id_material == id_material), None)

        if material_seleccionado:
            reciclar_material(cliente, material_seleccionado)
        else:
            print("No existe el material. Intenta con otro.")




class Historial:
    def __init__(self, historial_cliente_id, historial_material_id, historial_fecha_entrega,
                 historial_cantidad_reciclada):
        self.historial_cliente_id = historial_cliente_id
        self.historial_material_id = historial_material_id
        self.historial_fecha_entrega = historial_fecha_entrega
        self.historial_cantidad_reciclada = historial_cantidad_reciclada


historial_reciclaje = []


def mostrar_historial():
    if not historial_reciclaje:
        print("No existe historial de reciclaje todavía.")
        return

    for registro in historial_reciclaje:
        cliente = next((c for c in clientes_registrados if c.id_cliente == registro.historial_cliente_id), None)
        material = next((m for m in materiales_disponibles if m.id_material == registro.historial_material_id), None)
        cliente_nombre = cliente.nombre_cliente if cliente else "Desconocido"
        material_nombre = material.nombre_material if material else "Desconocido"
        print(
            f"Historial del cliente: ID {registro.historial_cliente_id} - {cliente_nombre} | Material: ID {registro.historial_material_id} - {material_nombre} | Fecha entrega: {registro.historial_fecha_entrega} | Cantidad reciclada: {registro.historial_cantidad_reciclada}")


def buscar_historial_cliente(cliente_id):

    cliente = next((c for c in clientes_registrados if c.id_cliente == cliente_id), None)

    if not cliente:
        print(f"No se encontró un cliente con el ID {cliente_id}.")
        return

    historial_cliente = [registro for registro in historial_reciclaje if registro.historial_cliente_id == cliente_id]

    if not historial_cliente:
        print(f"{cliente.nombre_cliente} no tiene historial de reciclaje todavía.")
        return
    
    print(f"Historial de reciclaje para {cliente.nombre_cliente} (ID: {cliente_id}):")
    for registro in historial_cliente:
        material = next((m for m in materiales_disponibles if m.id_material == registro.historial_material_id), None)
        material_nombre = material.nombre_material if material else "Desconocido"
        print(f"- Material: {material_nombre} | Fecha de entrega: {registro.historial_fecha_entrega} | Cantidad reciclada: {registro.historial_cantidad_reciclada} kg")


def guardar_historial(historial_reciclaje):
    with open("historial.json", "w") as archivo:
        json.dump([registro.__dict__ for registro in historial_reciclaje], archivo, indent=4)


def cargar_historial():
    if not os.path.exists("historial.json"):
        return []
    with open("historial.json", "r", encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)
            return [Historial(**registro) for registro in datos]
        except json.JSONDecodeError:
            return []




def menu():
    while True:
        print("-------  BIENVENIDO AL MENÚ DE RECICLAJE :) --------")
        print("1. Registrar Cliente")
        print("2. Ver Clientes Registrados")
        print("3. Reciclar ")
        print("4. Ver Historial")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_clientes()
        elif opcion == "2":
            mostrar_clientes()
        elif opcion == "3":
            reciclar()
        elif opcion == "4":
            cliente_id = int(input("Ingrese el ID del cliente para ver su historial: "))
            buscar_historial_cliente(cliente_id)
        elif opcion == "5":
            print("Saliendo del programa... Gracias por reciclar y ayudar a nuestro planeta")
            break
        else:
            print("Opción no válida. Intente de nuevo")


if __name__ == "__main__":
    clientes_registrados = cargar_clientes()
    historial_reciclaje = cargar_historial()
    menu()
