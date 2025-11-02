#Funcion mostrar menu.
def mostrar_menu():
    print("\n--- 🌍 Menú de Gestión de Países ---")
    print("1. Buscar país por nombre")
    print("2. Filtrar países por continente")
    print("3. Filtrar países por rango de población")
    print("4. Filtrar países por rango de superficie")
    print("5. Ordenar países")
    print("6. Mostrar estadísticas")
    print("0. Salir")

#Funcion Mostrar pais, la utiliza para cada vez que sea necesario mostrar un pais con el formato correcto.

def _mostrar_pais(pais):
    print(f"\nCargando datos...")
    import time
    time.sleep(1)
    print(f"\n  ------------------------------")
    print(f"  Nombre:     {pais['nombre']}")
    # f"{pais['poblacion']:,}" agrega comas como separadores de miles
    print(f"  Población:  {pais['poblacion']:,}")
    print(f"  Superficie: {pais['superficie']:,} km²")
    print(f"  Continente: {pais['continente']}")
    print(f"  ------------------------------")

#Funcion cargar datos desde CSV

import csv

def cargar_csv (nombre_archivo):
    lista_paises = [] #Crea lista de paises vacias.
    try:
        with open(nombre_archivo, mode="r", newline="") as archivo: #Abre el archivo en modo lectura y utilizando newline para no modificar los saltos de linea.
            lector_csv = csv.DictReader(archivo) #Lee el archivo y cada fila la vuelve un diccionario.
            for fila in lector_csv: #Recorre los datos del archivo fila por fila
                try:
                    fila["poblacion"] =  int(fila["poblacion"]) #Intenta convertir los datos de superficie y poblacion en INT
                    fila["superficie"] = int(fila["superficie"])
                    lista_paises.append(fila) #Agrega la fila a la lista de diccionarios. 
                except ValueError:
                    print(f"Error: La fila para '{fila['nombre']}' tiene datos numéricos inválidos. Se omitirá.") #Si hay datos numericos erroneos arroja un error.
        return lista_paises
    except FileNotFoundError: #Si no encuentra el archivo tambien arroja un error.
        print(f"Error: ¡No se encontró el archivo '{nombre_archivo}'!")
        return []
    except Exception as a: #Si ocurre cualquier otro error arroja el siguiente mensaje indicando que algo esta fallando y el fallo tecnico que arroja Python.
        print(f"Error inesperado al leer el CSV: {a}")
        return []

#Funcion Buscar pais por nombre.

def buscar_pais(lista_paises):
    print("\n1 - Buscar país por nombre.") 
    busqueda = input("\nIngrese nombre del país que desea buscar: ").strip() #Le pide al usuario el pais que desea buscar.
    
    busqueda_lower = busqueda.lower() #Cambia a minusculas para busarlo en la lista.

    pais_encontrado = None #Define que todavia no encuentra ningun pais que coincida.

    for pais in lista_paises: #Recorre la lista de paies, elemento por elemento.
        nombre_pais_lower = pais["nombre"].lower() #Cambia a minusculas el pais de la lista para luego compararlo.

        if nombre_pais_lower == busqueda_lower: # Compara el pais con el pais buscado.
            pais_encontrado = pais # Si lo encuentra le asigna el diccionario de ese pais para mostrar luego los datos.
            break
    
    if pais_encontrado: # Si pais_encontrado tiene algun elemento hace lo siguiente.
        print(f"\nSe ha encontrado 1 resultado para la busqueda de {busqueda}...")
        
        _mostrar_pais(pais_encontrado) #Llama a la funcion mostrar pais para mostrar los datos del pais ordenadamente.

    else:
        print(f"\nNo se encontro ningun resultado para {busqueda}") #Si no lo encuentra muestra el mensaje.

#Funcion Filtrar continente.

def filtrar_continente(lista_paises):
    print("\n2 - Filtrar paises por continente.")

    continentes_disponibles = set() #Crea un set con los continentes disponibles, ya que elimina duplicados.
    
    for pais in lista_paises: #Recorre la lista de paises, y añande todos los continentes disponibles al set.
        continentes_disponibles.add(pais["continente"])
    
    print(f"\nContinentes disponibles en la lista: {', '.join(sorted(continentes_disponibles))}") 
    
    continente_buscado = input("\nPor favor, ingrese un continente de la lista: ").strip().capitalize() #Le pide al usuario que ingrese el continente a filtrar.

    if continente_buscado not in continentes_disponibles: #Si el continente buscado no esta en los disponibles indica que no se encuentro.
        print(f"\nEl continente {continente_buscado} no se encuentra en la lista. ")
        return
    
    paises_continente = [] #Crea la lista de paises del continente buscado, por ahora vacia.

    for pais in lista_paises: #Recorre la lista de paises pais por pais, compara el continente con el buscado y lo agrega a la lista si es necesario.
        if pais["continente"] == continente_buscado:
            paises_continente.append(pais)
    
    if paises_continente: #Si paises_continente contiene elementos indica cuantos se encontraron del continente buscado.
        print(f"\nSe han encontrado {len(paises_continente)} en {continente_buscado}...")
        for pais in paises_continente: #Recorre la lista para mostrar todos los paises y sus datos.
            _mostrar_pais(pais)
    else:
        print(f"\nNo se encontaron paises en {continente_buscado}") #Si la lista esta vacia indica que no se encontraron paises.

#Filtrar por poblacion

def filtrar_poblacion(lista_paises):
    print("\n2 - Filtrar paises por poblacion.")
    
    min_poblacion = _obtener_numero_validado ("Ingrese la poblacion minimna [EJ: 100000] [Vacio para 0]: ",0)
    max_poblacion = _obtener_numero_validado ("Ingrese la poblacion maxima [EJ: 5000000] [Vacio para sin limite]: ",99999999999)

    if min_poblacion>max_poblacion:
        print("La poblacion minima no puede ser mayor a la poblacion maxima.")
        return
    
    paises_encontrados = []
    
    for pais in lista_paises:
        if min_poblacion <= pais["poblacion"] <= max_poblacion:
            paises_encontrados.append(pais)
    if paises_encontrados:
        print(f"Se encontraron {len(paises_encontrados)} con poblacion entre {min_poblacion} y {max_poblacion}")
        for pais in paises_encontrados:
            _mostrar_pais(pais)
    else:
        print("No se encontraron paises en ese rango de problacion.")


#Funcion para validar un numero. (Se va utilizar para las funciones de filtrar.)

def _obtener_numero_validado(mensaje, default_valor):
    while True: #Bucle infinito hasta que obtengam un número
        entrada_str = input(mensaje).strip()
        
        #Opción 1: El usuario presionó Enter
        if not entrada_str:
            return default_valor
        
        #Opción 2: El usuario ingreso un numero.
        try:
            # Intenta convertirlo a entero
            valor_int = int(entrada_str)
            return valor_int #Devuelve el numero
        except ValueError:
            # Se repite el bucle
            print(f"Error: '{entrada_str}' no es un número válido. Intente de nuevo.")
