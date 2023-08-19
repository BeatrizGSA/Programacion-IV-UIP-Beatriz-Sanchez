import sqlite3
from pymongo import MongoClient

conn = sqlite3.connect('inventario.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS inventario
             (id INTEGER PRIMARY KEY, nombre TEXT, cantidad INTEGER)''')
conn.commit()

client = MongoClient('mongodb://localhost:27017/')
db = client['inventario_db']
coleccion_inventario = db['inventario']

def agregar_articulo():
    nombre = input("Ingrese el nombre del artículo: ")
    cantidad = int(input("Ingrese la cantidad del artículo: "))

    # Agregar a SQLite
    c.execute("INSERT INTO inventario (nombre, cantidad) VALUES (?, ?)", (nombre, cantidad))
    conn.commit()

    # Agregar a MongoDB
    coleccion_inventario.insert_one({"nombre": nombre, "cantidad": cantidad})
    print("¡Artículo agregado exitosamente!")

def buscar_articulo():
    nombre = input("Ingrese el nombre del artículo a buscar: ")

    # Buscar en SQLite
    c.execute("SELECT * FROM inventario WHERE nombre = ?", (nombre,))
    resultado_sqlite = c.fetchone()

    # Buscar en MongoDB
    resultado_mongodb = coleccion_inventario.find_one({"nombre": nombre})

    if resultado_sqlite and resultado_mongodb:
        print(f"SQLite: {resultado_sqlite[1]} - Cantidad: {resultado_sqlite[2]}")
        print(f"MongoDB: {resultado_mongodb['nombre']} - Cantidad: {resultado_mongodb['cantidad']}")
    else:
        print("Artículo no encontrado.")

def editar_articulo():
    nombre = input("Ingrese el nombre del artículo a editar: ")

    # Editar en SQLite
    c.execute("SELECT * FROM inventario WHERE nombre = ?", (nombre,))
    resultado_sqlite = c.fetchone()

    # Editar en MongoDB
    resultado_mongodb = coleccion_inventario.find_one({"nombre": nombre})

    if resultado_sqlite and resultado_mongodb:
        nueva_cantidad = int(input("Ingrese la nueva cantidad del artículo: "))

        # Actualizar SQLite
        c.execute("UPDATE inventario SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre))
        conn.commit()

        # Actualizar MongoDB
        coleccion_inventario.update_one({"nombre": nombre}, {"$set": {"cantidad": nueva_cantidad}})
        print("¡Artículo editado exitosamente!")
    else:
        print("Artículo no encontrado.")

def eliminar_articulo():
    nombre = input("Ingrese el nombre del artículo a eliminar: ")

    # Eliminar en SQLite
    c.execute("DELETE FROM inventario WHERE nombre = ?", (nombre,))
    conn.commit()

    # Eliminar en MongoDB
    coleccion_inventario.delete_one({"nombre": nombre})
    print("¡Artículo eliminado exitosamente!")

while True:
    print("\nAdministrador de Inventario")
    print("1. Agregar artículo")
    print("2. Buscar artículo")
    print("3. Editar artículo")
    print("4. Eliminar artículo")
    print("5. Salir")
    opcion = input("Ingrese su opción: ")

    if opcion == "1":
        agregar_articulo()
    elif opcion == "2":
        buscar_articulo()
    elif opcion == "3":
        editar_articulo()
    elif opcion == "4":
        eliminar_articulo()
    elif opcion == "5":
        break
    else:
        print("Opción inválida. Por favor, intente de nuevo.")

conn.close()

