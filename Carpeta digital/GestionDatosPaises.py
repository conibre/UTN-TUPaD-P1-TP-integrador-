import csv
import os

# --- CONSTANTES ---
ARCHIVO_CSV = "paises.csv"

# --- MÓDULO DE MANEJO DE ARCHIVOS ---

def cargar_datos():
    """
    Lee el archivo CSV y retorna una lista de diccionarios.
    Si el archivo no existe, retorna una lista vacía.
    """
    datos = []
    if os.path.exists(ARCHIVO_CSV):
        try:
            with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    # Convertimos los números de string a int para poder operar
                    fila['poblacion'] = int(fila['poblacion'])
                    fila['superficie'] = int(fila['superficie'])
                    datos.append(fila)
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    return datos

def guardar_datos(lista_paises):
    """
    Escribe la lista de diccionarios en el archivo CSV.
    """
    try:
        with open(ARCHIVO_CSV, mode='w', encoding='utf-8', newline='') as archivo:
            columnas = ['nombre', 'poblacion', 'superficie', 'continente']
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(lista_paises)
        print("--- Cambios guardados en el archivo correctamente ---")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

# --- MÓDULO DE VALIDACIONES E INPUTS ---

def solicitar_entero(mensaje):
    """
    Solicita un número entero positivo al usuario.
    Valida que no sea texto ni negativo.
    """
    valor = -1
    valido = False
    while not valido:
        entrada = input(mensaje)
        if entrada.isdigit():
            valor = int(entrada)
            valido = True
        else:
            print("Error: Debe ingresar un número entero positivo.")
    return valor

def solicitar_texto(mensaje):
    """
    Solicita un texto no vacío.
    """
    texto = ""
    valido = False
    while not valido:
        entrada = input(mensaje).strip()
        if len(entrada) > 0:
            texto = entrada
            valido = True
        else:
            print("Error: El campo no puede estar vacío.")
    return texto

# --- MÓDULO DE LÓGICA DE NEGOCIO (CRUD y Búsquedas) ---

def buscar_pais_por_nombre(lista_paises, nombre_busqueda):
    """
    Busca un país por coincidencia parcial.
    Retorna una lista con los países encontrados.
    """
    resultados = []
    nombre_busqueda = nombre_busqueda.lower()
    
    indice = 0
    cantidad = len(lista_paises)
    
    while indice < cantidad:
        pais = lista_paises[indice]
        if nombre_busqueda in pais['nombre'].lower():
            resultados.append(pais)
        indice += 1
        
    return resultados

def agregar_pais(lista_paises):
    """
    Solicita datos al usuario y agrega un nuevo país a la lista.
    """
    print("\n--- Agregar Nuevo País ---")
    nombre = solicitar_texto("Nombre del país: ").capitalize()
    
    # Verificamos si ya existe (búsqueda exacta)
    existe = False
    i = 0
    while i < len(lista_paises) and not existe:
        if lista_paises[i]['nombre'].lower() == nombre.lower():
            existe = True
        i += 1
    
    if existe:
        print(f"El país '{nombre}' ya existe en la base de datos.")
    else:
        poblacion = solicitar_entero("Población: ")
        superficie = solicitar_entero("Superficie (km2): ")
        continente = solicitar_texto("Continente: ").capitalize()
        
        nuevo_pais = {
            'nombre': nombre,
            'poblacion': poblacion,
            'superficie': superficie,
            'continente': continente
        }
        lista_paises.append(nuevo_pais)
        guardar_datos(lista_paises)
        print(f"País '{nombre}' agregado exitosamente.")

def actualizar_pais(lista_paises):
    """
    Busca un país y permite modificar su población y superficie.
    """
    print("\n--- Actualizar País ---")
    nombre_busqueda = solicitar_texto("Ingrese el nombre del país a modificar: ")
    
    # Búsqueda exacta para modificar
    encontrado = False
    indice = 0
    posicion_encontrada = -1
    
    # Iteramos usando la bandera 'encontrado'
    while indice < len(lista_paises) and not encontrado:
        if lista_paises[indice]['nombre'].lower() == nombre_busqueda.lower():
            encontrado = True
            posicion_encontrada = indice
        indice += 1
        
    if encontrado:
        pais = lista_paises[posicion_encontrada]
        print(f"Datos actuales de {pais['nombre']}: Población={pais['poblacion']}, Superficie={pais['superficie']}")
        
        nueva_poblacion = solicitar_entero("Nueva Población: ")
        nueva_superficie = solicitar_entero("Nueva Superficie: ")
        
        lista_paises[posicion_encontrada]['poblacion'] = nueva_poblacion
        lista_paises[posicion_encontrada]['superficie'] = nueva_superficie
        
        guardar_datos(lista_paises)
        print("Datos actualizados correctamente.")
    else:
        print("País no encontrado.")

# --- MÓDULO DE FILTROS Y ORDENAMIENTO ---

def filtrar_paises(lista_paises):
    """
    Submenú para filtrar países.
    """
    sub_opcion = ""
    while sub_opcion != "0":
        print("\n--- Filtrar por: ---")
        print("1. Continente")
        print("2. Rango de Población")
        print("3. Rango de Superficie")
        print("0. Volver")
        
        sub_opcion = input("Seleccione: ")
        
        resultados = []
        
        if sub_opcion == "1":
            cont = solicitar_texto("Ingrese Continente: ").lower()
            i = 0
            while i < len(lista_paises):
                if lista_paises[i]['continente'].lower() == cont:
                    resultados.append(lista_paises[i])
                i += 1
            mostrar_tabla(resultados)
            
        elif sub_opcion == "2":
            min_p = solicitar_entero("Población mínima: ")
            max_p = solicitar_entero("Población máxima: ")
            i = 0
            while i < len(lista_paises):
                pob = lista_paises[i]['poblacion']
                if pob >= min_p and pob <= max_p:
                    resultados.append(lista_paises[i])
                i += 1
            mostrar_tabla(resultados)
            
        elif sub_opcion == "3":
            min_s = solicitar_entero("Superficie mínima: ")
            max_s = solicitar_entero("Superficie máxima: ")
            i = 0
            while i < len(lista_paises):
                sup = lista_paises[i]['superficie']
                if sup >= min_s and sup <= max_s:
                    resultados.append(lista_paises[i])
                i += 1
            mostrar_tabla(resultados)
            
        elif sub_opcion != "0":
            print("Opción inválida.")

def ordenar_paises(lista_paises):
    """
    Ordena la lista (copia temporal) según criterio.
    """
    print("\n--- Ordenar por: ---")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    criterio = input("Seleccione criterio: ")
    
    orden = input("Tipo de orden (1: Ascendente, 2: Descendente): ")
    es_reversa = False
    if orden == "2":
        es_reversa = True
    
    # Creamos una copia para no afectar el orden original si no se desea
    lista_ordenada = lista_paises.copy()
    
    if criterio == "1":
        lista_ordenada.sort(key=lambda x: x['nombre'], reverse=es_reversa)
        mostrar_tabla(lista_ordenada)
    elif criterio == "2":
        lista_ordenada.sort(key=lambda x: x['poblacion'], reverse=es_reversa)
        mostrar_tabla(lista_ordenada)
    elif criterio == "3":
        lista_ordenada.sort(key=lambda x: x['superficie'], reverse=es_reversa)
        mostrar_tabla(lista_ordenada)
    else:
        print("Criterio inválido.")

# --- MÓDULO DE ESTADÍSTICAS ---

def generar_estadisticas(lista_paises):
    """
    Calcula y muestra indicadores clave.
    """
    cantidad = len(lista_paises)
    if cantidad == 0:
        print("No hay datos para generar estadísticas.")
        return # Salida temprana válida en función

    max_pob_pais = lista_paises[0]
    min_pob_pais = lista_paises[0]
    suma_pob = 0
    suma_sup = 0
    conteo_continentes = {}
    
    i = 0
    while i < cantidad:
        p = lista_paises[i]
        
        # Max y Min
        if p['poblacion'] > max_pob_pais['poblacion']:
            max_pob_pais = p
        if p['poblacion'] < min_pob_pais['poblacion']:
            min_pob_pais = p
            
        # Acumuladores
        suma_pob += p['poblacion']
        suma_sup += p['superficie']
        
        # Conteo por continente (Lógica de diccionario)
        cont = p['continente']
        if cont in conteo_continentes:
            conteo_continentes[cont] += 1
        else:
            conteo_continentes[cont] = 1
            
        i += 1
        
    prom_pob = suma_pob / cantidad
    prom_sup = suma_sup / cantidad
    
    print("\n--- Estadísticas Generales ---")
    print(f"País con Mayor Población: {max_pob_pais['nombre']} ({max_pob_pais['poblacion']})")
    print(f"País con Menor Población: {min_pob_pais['nombre']} ({min_pob_pais['poblacion']})")
    print(f"Promedio de Población: {prom_pob:.2f}")
    print(f"Promedio de Superficie: {prom_sup:.2f} km2")
    
    print("\n--- Países por Continente ---")
    claves = list(conteo_continentes.keys())
    j = 0
    while j < len(claves):
        k = claves[j]
        print(f"{k}: {conteo_continentes[k]}")
        j += 1

# --- VISTA (UI Consola) ---

def mostrar_tabla(lista):
    """
    Imprime la lista de países con formato tabular.
    """
    if not lista:
        print("No se encontraron resultados.")
    else:
        print(f"\n{'NOMBRE':<20} | {'POBLACIÓN':<15} | {'SUPERFICIE':<15} | {'CONTINENTE':<15}")
        print("-" * 75)
        i = 0
        while i < len(lista):
            p = lista[i]
            print(f"{p['nombre']:<20} | {p['poblacion']:<15} | {p['superficie']:<15} | {p['continente']:<15}")
            i += 1
        print("-" * 75)

def menu_principal():
    paises = cargar_datos()
    continuar = True
    
    while continuar:
        print("\n=== GESTIÓN DE DATOS DE PAÍSES ===")
        print("1. Agregar País")
        print("2. Actualizar País")
        print("3. Buscar País")
        print("4. Filtrar Países")
        print("5. Ordenar Países")
        print("6. Ver Estadísticas")
        print("7. Ver Todos")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_pais(paises)
        elif opcion == "2":
            actualizar_pais(paises)
        elif opcion == "3":
            nombre = solicitar_texto("Ingrese nombre a buscar: ")
            res = buscar_pais_por_nombre(paises, nombre)
            mostrar_tabla(res)
        elif opcion == "4":
            filtrar_paises(paises)
        elif opcion == "5":
            ordenar_paises(paises)
        elif opcion == "6":
            generar_estadisticas(paises)
        elif opcion == "7":
            mostrar_tabla(paises)
        elif opcion == "0":
            print("Saliendo del sistema...")
            continuar = False
        else:
            print("Opción inválida, intente nuevamente.")

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    menu_principal()