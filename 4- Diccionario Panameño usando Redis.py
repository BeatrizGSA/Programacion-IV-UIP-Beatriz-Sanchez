import redis

redis_url = "redis://default:LApzhSSk8YSwXIshipytd2PIEQutVyv5@redis-18733.c228.us-central1-1.gce.cloud.redislabs.com:18733"
r = redis.from_url(redis_url)

def agregar_palabra():
    palabra = input("Ingrese la nueva palabra: ")
    significado = input("Ingrese el significado de la palabra: ")
    r.set(palabra, significado)
    print("¡Palabra agregada exitosamente!")

def editar_palabra():
    palabra = input("Ingrese la palabra a editar: ")
    if r.exists(palabra):
        nuevo_significado = input("Ingrese el nuevo significado de la palabra: ")
        r.set(palabra, nuevo_significado)
        print("¡Palabra editada exitosamente!")
    else:
        print("Palabra no encontrada.")

def eliminar_palabra():
    palabra = input("Ingrese la palabra a eliminar: ")
    if r.exists(palabra):
        r.delete(palabra)
        print("¡Palabra eliminada exitosamente!")
    else:
        print("Palabra no encontrada.")

def ver_palabras():
    palabras = r.keys()
    if len(palabras) == 0:
        print("No se encontraron palabras.")
    else:
        for palabra in palabras:
            significado = r.get(palabra).decode('utf-8')
            print(palabra.decode('utf-8') + ": " + significado)

def buscar_palabra():
    palabra = input("Ingrese la palabra a buscar: ")
    resultado = r.get(palabra)
    if resultado:
        print(palabra + ": " + resultado.decode('utf-8'))
    else:
        print("Palabra no encontrada.")

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