from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('mysql+pymysql://root:1234@localhost:3306/panama_slang_mariadb')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class PanamaSlang(Base):
    __tablename__ = 'panama_slang_mariadb'
    palabra = Column(String, primary_key=True)
    significado = Column(String)

def agregar_palabra():
    palabra = input("Ingrese la nueva palabra: ")
    significado = input("Ingrese el significado de la palabra: ")
    palabra_nueva = PanamaSlang(palabra=palabra, significado=significado)
    session.add(palabra_nueva)
    session.commit()
    print("¡Palabra agregada exitosamente!")

def editar_palabra():
    palabra = input("Ingrese la palabra a editar: ")
    nueva_palabra = session.query(PanamaSlang).filter_by(palabra=palabra).first()
    if nueva_palabra:
        nuevo_significado = input("Ingrese el nuevo significado de la palabra: ")
        nueva_palabra.significado = nuevo_significado
        session.commit()
        print("¡Palabra editada exitosamente!")
    else:
        print("Palabra no encontrada.")

def eliminar_palabra():
    palabra = input("Ingrese la palabra a eliminar: ")
    palabra_eliminar = session.query(PanamaSlang).filter_by(palabra=palabra).first()
    if palabra_eliminar:
        session.delete(palabra_eliminar)
        session.commit()
        print("¡Palabra eliminada exitosamente!")
    else:
        print("Palabra no encontrada.")

def ver_palabras():
    palabras = session.query(PanamaSlang).all()
    if len(palabras) == 0:
        print("No se encontraron palabras.")
    else:
        for palabra in palabras:
            print(palabra.palabra + ": " + palabra.significado)

def buscar_palabra():
    palabra = input("Ingrese la palabra a buscar: ")
    resultado = session.query(PanamaSlang).filter_by(palabra=palabra).first()
    if resultado:
        print(resultado.palabra + ": " + resultado.significado)
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
session.close()