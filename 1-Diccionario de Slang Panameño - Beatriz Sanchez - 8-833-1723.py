import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('panama_slang.db')
c = conn.cursor()

# Crear la tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS panama_slang
             (palabra text PRIMARY KEY, significado text)''')

# Función para agregar una nueva palabra a la base de datos
def agregar_palabra():
    palabra = input("Ingrese la nueva palabra: ")
    significado = input("Ingrese el significado de la palabra: ")
    c.execute("INSERT INTO panama_slang VALUES (?, ?)", (palabra, significado))
    conn.commit()
    print("¡Palabra agregada exitosamente!")


# Función para editar una palabra existente en la base de datos
def editar_palabra():
    palabra = input("Ingrese la palabra a editar: ")
    nuevo_significado = input("Ingrese el nuevo significado de la palabra: ")
    c.execute("UPDATE panama_slang SET significado = ? WHERE palabra = ?", (nuevo_significado, palabra))
    conn.commit()
    print("¡Palabra editada exitosamente!")


# Función para eliminar una palabra existente de la base de datos
def eliminar_palabra():
    palabra = input("Ingrese la palabra a eliminar: ")
    c.execute("DELETE FROM panama_slang WHERE palabra = ?", (palabra,))
    conn.commit()
    print("¡Palabra eliminada exitosamente!")


# Función para ver la lista de palabras en la base de datos
def ver_palabras():
    c.execute("SELECT * FROM panama_slang")
    palabras = c.fetchall()
    if len(palabras) == 0:
        print("No se encontraron palabras.")
    else:
        for palabra in palabras:
            print(palabra[0] + ": " + palabra[1])


# Función para buscar el significado de una palabra en la base de datos
def buscar_palabra():
    palabra = input("Ingrese la palabra a buscar: ")
    c.execute("SELECT * FROM panama_slang WHERE palabra = ?", (palabra,))
    resultado = c.fetchone()
    if resultado is None:
        print("Palabra no encontrada.")
    else:
        print(resultado[0] + ": " + resultado[1])


# Bucle principal del programa
while True:
    print("\nDiccionario de Slang Panameño")
    print("1. Agregar nueva palabra")
    print("2. Editar palabra existente")
    print("3. Eliminar palabra existente")
    print("4. Ver lista de palabras")
    print("5. Buscar significado de palabra")
    print("6. Salir")
    opcion = input("Ingrese su opción: ")
    if opcion == "1":
        agregar_palabra()
    elif opcion == "2":
        editar_palabra()
    elif opcion == "3":
        eliminar_palabra()
    elif opcion == "4":
        ver_palabras()
    elif opcion == "5":
        buscar_palabra()
    elif opcion == "6":
        break
    else:
        print("Opción inválida. Por favor, intente de nuevo.")

# Cerrar la conexión a la base de datos
conn.close()