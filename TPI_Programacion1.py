#TPI Programación 1 - Gestión de Datos de Países en Python - UTN
#Valentina Quintero y Lautaro Duarte


import csv                             #importa el módulo estándar para leer y escribir archivos CSV
import os                              #importa el módulo para trabajar con rutas de archivos del sistema
import sys                             #importa el módulo para acceder a los argumentos de la línea de comandos
import unicodedata                     #importa el módulo para quitar tildes de los textos

#constantes

RUTA_CSV_DEFECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paises.csv")        #ruta de paises.csv, ubicado junto a este archivo
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]                                     #lista con los nombres de las columnas del CSV, en orden
CONTINENTES = ["África", "América", "Asia", "Europa", "Oceanía", "Antártida"]                    #lista de continentes permitidos


#utilidades de texto y formato

def normalizar(texto):                  #define la función que recibe un texto a normalizar
    #devuelve el texto en minúsculas y sin tildes (para comparar sin distinguir acentos)
    descompuesto = unicodedata.normalize("NFD", texto.strip().lower())                   #quita espacios, pasa a minúscula y separa cada letra de su tilde
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")           #une todos los caracteres salvo las marcas de tilde


def formatear_numero(numero):                        #define la función que recibe un número a formatear
    #formatea un número con separador de miles (45376763 -> 45.376.763)
    return f"{numero:,.0f}".replace(",", ".")        #da formato con comas de miles y las reemplaza por puntos


def canonizar_continente(texto):             #define la función que recibe el continente escrito por el usuario
    #devuelve el continente con su escritura oficial, o None si no es válido  
    for continente in CONTINENTES:                              #recorre cada continente permitido
        if normalizar(continente) == normalizar(texto):         #compara ignorando tildes y mayúsculas
            return continente               #devuelve el nombre oficial (con tildes) si coincide
    return None                             #si ninguno coincidió, devuelve None (continente inválido)


#validación de registros

def validar_registro(nombre, poblacion, superficie, continente):            #retorna (diccionario_pais, None) si es válido, o (None, mensaje_error) si no lo es

    nombre = str(nombre).strip()                                        #convierte el nombre a texto y quita espacios sobrantes
    continente = str(continente).strip()                                #convierte el continente a texto y quita espacios sobrantes
    if not nombre or not str(poblacion).strip() or not str(superficie).strip() or not continente:           #comprueba si algún campo quedó vacío
        return None, "hay campos vacíos"                                #devuelve el error de campos vacíos
    try:                     #inicia un bloque para capturar errores de conversión a número
        poblacion = int(str(poblacion).strip())                         #convierte la población a entero
        superficie = int(str(superficie).strip())                       #convierte la superficie a entero
    except ValueError:       #si alguna conversión falla (hay letras, decimales, etc.)
        return None, "población y superficie deben ser números enteros"             #devuelve el error de formato numérico
    if poblacion <= 0 or superficie <= 0:                         #comprueba que ambos valores sean positivos
        return None, "población y superficie deben ser mayores a cero"              #devuelve el error de valores no positivos
    continente_ok = canonizar_continente(continente)              #obtiene el continente en su forma oficial, o None
    if continente_ok is None:                                     #si el continente no está en la lista permitida
        return None, f"continente inválido '{continente}'"                           #devuelve el error de continente inválido
    return {"nombre": nombre, "poblacion": poblacion,                                #arma el diccionario del país con nombre y población
            "superficie": superficie, "continente": continente_ok}, None             #agrega superficie y continente y devuelve sin error


#archivos CSV

def cargar_paises(ruta):                                     #lee el CSV y devuelve (lista_de_paises, lista_de_errores)
    #las filas con errores de formato se omiten y se informan; el programa no se cae
    paises, errores = [], []                                 #crea dos listas vacías: una para países y otra para mensajes de error
    try:                            #inicia un bloque para capturar errores de lectura de archivo
        with open(ruta, newline="", encoding="utf-8") as archivo:               #abre el archivo en UTF-8 y lo cierra solo al terminar
            lector = csv.reader(archivo)                #crea el lector que separa cada línea en columnas
            encabezado = next(lector, None)             #lee la primera línea (encabezado), o None si el archivo está vacío
            if encabezado is None or [c.strip().lower() for c in encabezado] != CAMPOS:          #verifica que el encabezado sea el esperado
                errores.append(f"Encabezado inválido. Se esperaba: {','.join(CAMPOS)}")          #registra el error de encabezado
                return paises, errores        #termina devolviendo la lista vacía y el error
            for num_fila, fila in enumerate(lector, start=2):                                    #recorre las filas de datos numerándolas desde 2 (la 1 es el encabezado)
                if not fila:                  #detecta una línea en blanco
                    continue                  #salta a la siguiente fila sin hacer nada
                if len(fila) != len(CAMPOS):                                                     #verifica que la fila tenga exactamente 4 columnas
                    errores.append(f"Fila {num_fila}: cantidad de columnas incorrecta")          #registra el error de columnas
                    continue                 #pasa a la siguiente fila
                pais, error = validar_registro(*fila)                               #valida los 4 valores de la fila
                if error:                    #si la validación devolvió un mensaje de error
                    errores.append(f"Fila {num_fila}: {error}")                     #registra el error indicando el número de fila
                else:                        #si la fila es válida
                    paises.append(pais)                             #agrega el país a la lista
    except FileNotFoundError:                                       #si el archivo no existe
        errores.append(f"No se encontró el archivo '{ruta}'")                       #registra el error de archivo inexistente
    except (OSError, UnicodeDecodeError) as exc:                                    #si hubo un problema de lectura o de codificación
        errores.append(f"No se pudo leer el archivo: {exc}")                        #registra el error con el detalle
    return paises, errores                          #devuelve los países cargados y la lista de errores


def guardar_paises(paises, ruta):                                #escribe la lista de países en el CSV. Retorna True si tuvo éxito 
    try:                                #inicia un bloque para capturar errores de escritura
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:      #abre el archivo para escribir (lo reemplaza) en UTF-8
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)           #crea el escritor que usa los diccionarios y el orden de CAMPOS
            escritor.writeheader()                                          #escribe la línea de encabezado
            escritor.writerows(paises)                                      #escribe una línea por cada país de la lista
        return True                                                         #indica que se guardó correctamente
    except OSError as exc:                                                  #si ocurre un error del sistema (permisos, disco, etc.)
        print(f" Error. No se pudo guardar el archivo: {exc}")                          #informa el error al usuario
        return False                    #indica que no se pudo guardar


#entrada de datos con validación

def pedir_texto(mensaje):                                      #pide un texto no vacío, repitiendo hasta que sea válido           
    while True:                                                #repite indefinidamente hasta recibir un valor válido
        valor = input(mensaje).strip()                                      #muestra el mensaje, lee lo escrito y quita espacios sobrantes
        if valor:                    #si el texto no está vacío
            return valor             #lo devuelve y termina la función
        print("Error. El campo no puede estar vacío.")                      #si estaba vacío, avisa y vuelve a pedirlo


def pedir_entero(mensaje, permitir_vacio=False):                  #pide un entero positivo. Si permitir_vacio=True, Enter devuelve None          
    while True:                 #repite hasta recibir un valor válido
        valor = input(mensaje).strip()        #lee lo escrito y quita espacios sobrantes
        if not valor and permitir_vacio:      #si está vacío y se permite dejarlo vacío
            return None                       #devuelve None para indicar "sin cambios"
        if not valor:                         #si está vacío y no se permite
            print("Error. El campo no puede estar vacío.")                                   #avisa el error
            continue                     #vuelve al inicio del bucle para pedirlo de nuevo
        try:                             #inicia un bloque para capturar errores de conversión
            numero = int(valor)                     #intenta convertir el texto a entero
        except ValueError:                          #si el texto no es un entero válido
            print("Error. Ingrese un número entero válido (sin puntos ni letras).")           #avisa el error
            continue                #vuelve a pedir el dato
        if numero <= 0:                      #comprueba que el número sea positivo
            print("Error. El número debe ser mayor a cero.")                                  #avisa el error
            continue                #vuelve a pedir el dato
        return numero               #devuelve el entero válido


def pedir_continente():                   #pide un continente válido de la lista de continentes permitidos         
    while True:                      #repite hasta recibir un continente válido
        valor = pedir_texto(f"Continente ({', '.join(CONTINENTES)}): ")            #pide el texto mostrando las opciones disponibles
        continente = canonizar_continente(valor)                                   #lo convierte a su forma oficial, o None si no existe
        if continente:                                         #si es un continente válido
            return continente                                  #lo devuelve
        print("Error. Continente no válido. Elija uno de la lista.")         #si no lo es, avisa y vuelve a pedirlo


def pedir_rango(etiqueta):                      #pide un mínimo y un máximo (el mínimo no puede superar al máximo)     
    while True:  #repite hasta recibir un rango válido
        minimo = pedir_entero(f"{etiqueta} mínima: ")                            #pide el valor mínimo
        maximo = pedir_entero(f"{etiqueta} máxima: ")                            #pide el valor máximo
        if minimo <= maximo:            #comprueba que el rango sea coherente
            return minimo, maximo       #devuelve el rango como una tupla
        print("Error. El mínimo no puede ser mayor que el máximo.")              #si no lo es, avisa y vuelve a pedirlo


def pedir_opcion(mensaje, opciones_validas):             #pide una opción que pertenezca a opciones_validas         
    while True:                     #repite hasta recibir una opción válida
        valor = input(mensaje).strip()                  #lee lo escrito y quita espacios sobrantes
        if valor in opciones_validas:                   #comprueba que esté entre las opciones permitidas
            return valor            #devuelve la opción elegida
        print("Error. Opción inválida.")                #si no es válida, avisa y vuelve a pedirla


#lógica de negocio 

def buscar_indice_exacto(paises, nombre):                    #devuelve el índice del país con ese nombre exacto (ignora tildes/mayúsculas) o -1     
    objetivo = normalizar(nombre)                           #normaliza el nombre buscado
    for i, pais in enumerate(paises):                       #recorre la lista con su posición (i) y el país
        if normalizar(pais["nombre"]) == objetivo:          #compara los nombres normalizados
            return i                          #devuelve la posición del país encontrado
    return -1                 #si no lo encontró, devuelve -1


def agregar_pais(paises, nombre, poblacion, superficie, continente):               #agrega un país a la lista. Retorna (ok, mensaje)        
    pais, error = validar_registro(nombre, poblacion, superficie, continente)      #valida los datos recibidos
    if error:                           #si los datos no son válidos
        return False, f"No se agregó el país: {error}."                      #devuelve fracaso con el motivo
    if buscar_indice_exacto(paises, pais["nombre"]) != -1:                   #comprueba si ya existe un país con ese nombre
        return False, f"El país '{pais['nombre']}' ya existe."               #devuelve fracaso por duplicado
    paises.append(pais)                 #agrega el nuevo país al final de la lista
    return True, f"País '{pais['nombre']}' agregado correctamente."          #devuelve éxito con un mensaje


def actualizar_pais(paises, nombre, poblacion=None, superficie=None):               #actualiza población y superficie. None significa 'no modificar'. Retorna(ok, mensaje)       
    indice = buscar_indice_exacto(paises, nombre)               #busca la posición del país a actualizar
    if indice == -1:                 #si no existe
        return False, f"No existe un país llamado '{nombre}'."  #devuelve fracaso con el motivo
    if poblacion is not None:        #si se indicó una nueva población
        paises[indice]["poblacion"] = poblacion                 #reemplaza la población del país
    if superficie is not None:       #si se indicó una nueva superficie
        paises[indice]["superficie"] = superficie               #reemplaza la superficie del país
    return True, f"País '{paises[indice]['nombre']}' actualizado correctamente."            #devuelve éxito con un mensaje


def buscar_paises(paises, texto, exacta=False):                 #busca por nombre: coincidencia exacta o parcial, sin distinguir tildes ni mayúsculas      
    objetivo = normalizar(texto)    #normaliza el texto buscado
    resultado = []                  #crea la lista vacía donde se guardarán las coincidencias
    for pais in paises:             #recorre todos los países
        nombre = normalizar(pais["nombre"])          #normaliza el nombre del país actual
        if (exacta and nombre == objetivo) or (not exacta and objetivo in nombre):      #exacta: nombres iguales; parcial: el texto está contenido
            resultado.append(pais)                   #agrega el país a los resultados
    return resultado        #devuelve la lista de coincidencias (puede estar vacía)


def filtrar_por_continente(paises, continente):                     #devuelve los países del continente indicado              
    objetivo = normalizar(continente)               #normaliza el continente buscado
    return [p for p in paises if normalizar(p["continente"]) == objetivo]           #devuelve solo los países cuyo continente coincide


def filtrar_por_rango(paises, campo, minimo, maximo):                       #devuelve los países cuyo campo ('poblacion' o 'superficie') está entre minimo y maximo      
    return [p for p in paises if minimo <= p[campo] <= maximo]              #devuelve los países cuyo valor está dentro del rango (inclusive)


def ordenar_paises(paises, campo, descendente=False):                     #devuelve una NUEVA lista ordenada por campo; no modifica la original                 
    if campo == "nombre":                   #si se ordena por nombre (texto)
        return sorted(paises, key=lambda p: normalizar(p["nombre"]), reverse=descendente)       #ordena por nombre sin tildes; reverse invierte si es descendente
    return sorted(paises, key=lambda p: p[campo], reverse=descendente)              #ordena por el campo numérico indicado


def calcular_estadisticas(paises):                               #devuelve un diccionario con las estadísticas pedidas, o None si no hay datos         
    if not paises:               #si la lista está vacía
        return None              #no hay nada que calcular
    cantidad = len(paises)       #guarda la cantidad total de países
    por_continente = {}          #crea el diccionario contador de países por continente
    for p in paises:             #recorre todos los países
        por_continente[p["continente"]] = por_continente.get(p["continente"], 0) + 1        #suma 1 al contador de su continente (empieza en 0)
    return {                     #devuelve un diccionario con todos los resultados
        "mayor": max(paises, key=lambda p: p["poblacion"]),                         #país con mayor población
        "menor": min(paises, key=lambda p: p["poblacion"]),                         #país con menor población
        "prom_poblacion": sum(p["poblacion"] for p in paises) / cantidad,           #promedio de población (suma / cantidad)
        "prom_superficie": sum(p["superficie"] for p in paises) / cantidad,         #promedio de superficie (suma / cantidad)
        "por_continente": por_continente,                       #diccionario con la cantidad de países por continente
    }   #cierra el diccionario de resultados


#presentación por consola

def mostrar_paises(paises):                                         #imprime una tabla con los países recibidos              
    if not paises:               #si la lista está vacía
        print("\n[INFO] No se encontraron países con ese criterio.")            #informa que no hay resultados
        return                   #termina la función
    print(f"\n{'Nombre':<18}{'Población':>16}{'Superficie km²':>18}  {'Continente':<10}")        #imprime los títulos de las columnas alineados
    print("-" * 66)              #imprime una línea separadora de 66 guiones
    for p in paises:             #recorre cada país a mostrar
        print(f"{p['nombre']:<18}{formatear_numero(p['poblacion']):>16}"                  #imprime el nombre y la población (con puntos de miles)
              f"{formatear_numero(p['superficie']):>18}  {p['continente']:<10}")          #continúa la misma línea con superficie y continente
    print("-" * 66)              #imprime otra línea separadora
    print(f"Total: {len(paises)} país(es)")                                               #imprime la cantidad de países mostrados


def mostrar_estadisticas(paises):                                #imprime las estadísticas del dataset                  
    est = calcular_estadisticas(paises)    #calcula las estadísticas
    if est is None:                        #si no hay datos
        print("\nInfo: No hay datos para calcular estadísticas.")                   #informa que no se puede calcular
        return                             #termina la función
    print("\n=== ESTADÍSTICAS ===")                 #imprime el título de la sección
    print(f"País con mayor población : {est['mayor']['nombre']} "                    #imprime el nombre del país con más población
          f"({formatear_numero(est['mayor']['poblacion'])})")                        #agrega entre paréntesis su población formateada
    print(f"País con menor población : {est['menor']['nombre']} "                    #imprime el nombre del país con menos población
          f"({formatear_numero(est['menor']['poblacion'])})")                        #agrega entre paréntesis su población formateada
    print(f"Promedio de población    : {formatear_numero(est['prom_poblacion'])}")              #imprime el promedio de población
    print(f"Promedio de superficie   : {formatear_numero(est['prom_superficie'])} km²")         #imprime el promedio de superficie
    print("Cantidad de países por continente:")                                     #imprime el encabezado del conteo por continente
    for continente in sorted(est["por_continente"], key=normalizar):                #recorre los continentes ordenados alfabéticamente sin tildes
        print(f"  - {continente}: {est['por_continente'][continente]}")             #imprime el continente y su cantidad de países


#opciones del menú

def opcion_agregar(paises, ruta):                        #define la opción del menú para agregar un país
    print("\n--- Agregar país ---")                      #imprime el título de la opción
    nombre = pedir_texto("Nombre: ")                     #pide el nombre (no vacío)
    poblacion = pedir_entero("Población (entero): ")                        #pide la población (entero positivo)
    superficie = pedir_entero("Superficie en km² (entero): ")               #pide la superficie (entero positivo)
    continente = pedir_continente()                 #pide un continente válido
    ok, mensaje = agregar_pais(paises, nombre, poblacion, superficie, continente)               #intenta agregar el país y recibe el resultado
    if ok and not guardar_paises(paises, ruta):                       #si se agregó, intenta guardar en el CSV y comprueba si falló
        mensaje += " (Atención: no se pudo guardar en el CSV)"        #agrega una advertencia al mensaje
    print(("Ok " if ok else "Error ") + mensaje)                  #imprime el mensaje con el prefijo [OK] o [ERROR]


def opcion_actualizar(paises, ruta):                                  #define la opción del menú para actualizar un país
    print("\n--- Actualizar país ---")                                #imprime el título de la opción
    nombre = pedir_texto("Nombre exacto del país a actualizar: ")               #pide el nombre del país a modificar
    if buscar_indice_exacto(paises, nombre) == -1:                              #comprueba si el país no existe
        print(f"Error. No existe un país llamado '{nombre}'.")                 #informa el error
        return                                  #termina la opción sin hacer cambios
    print("(Presione Enter para dejar un dato sin cambios)")                    #explica cómo conservar un valor actual
    poblacion = pedir_entero("Nueva población: ", permitir_vacio=True)          #pide la nueva población (Enter = sin cambio)
    superficie = pedir_entero("Nueva superficie km²: ", permitir_vacio=True)    #pide la nueva superficie (Enter = sin cambio)
    if poblacion is None and superficie is None:                #si no se ingresó ningún cambio
        print("Info: No se ingresó ningún cambio.")            #informa que no se modificó nada
        return                            #termina la opción
    ok, mensaje = actualizar_pais(paises, nombre, poblacion, superficie)    #aplica los cambios y recibe el resultado
    if ok and not guardar_paises(paises, ruta):                             #si se actualizó, intenta guardar en el CSV y comprueba si falló
        mensaje += " (Atención: no se pudo guardar en el CSV)"              #agrega una advertencia al mensaje
    print(("Ok " if ok else "Error ") + mensaje)                        #imprime el mensaje con el prefijo [OK] o [ERROR]


def opcion_buscar(paises):                              #define la opción del menú para buscar por nombre
    print("\n--- Buscar país por nombre ---")                                               #imprime el título de la opción
    texto = pedir_texto("Texto a buscar: ")                                                 #pide el texto a buscar
    tipo = pedir_opcion("1) Coincidencia parcial  2) Coincidencia exacta: ", ("1", "2"))    #pide el tipo de coincidencia (1 o 2)
    mostrar_paises(buscar_paises(paises, texto, exacta=(tipo == "2")))                      #busca (exacta si eligió 2) y muestra los resultados


def opcion_filtrar(paises):                               #define la opción del menú para filtrar países
    print("\n--- Filtrar países ---")                     #imprime el título de la opción
    print("1) Por continente\n2) Por rango de población\n3) Por rango de superficie")  #imprime los tipos de filtro disponibles
    opcion = pedir_opcion("Opción: ", ("1", "2", "3"))                                 #pide el tipo de filtro (1, 2 o 3)
    if opcion == "1":                               #si eligió filtrar por continente
        mostrar_paises(filtrar_por_continente(paises, pedir_continente()))             #pide el continente, filtra y muestra
    elif opcion == "2":                             #si eligió filtrar por rango de población
        minimo, maximo = pedir_rango("Población")                                      #pide el rango de población
        mostrar_paises(filtrar_por_rango(paises, "poblacion", minimo, maximo))         #filtra por población y muestra
    else:                                           #si eligió filtrar por rango de superficie
        minimo, maximo = pedir_rango("Superficie")                                     #pide el rango de superficie
        mostrar_paises(filtrar_por_rango(paises, "superficie", minimo, maximo))        #filtra por superficie y muestra


def opcion_ordenar(paises):                                                             #define la opción del menú para ordenar países
    print("\n--- Ordenar países ---")                                                   #imprime el título de la opción
    print("1) Por nombre\n2) Por población\n3) Por superficie")                         #imprime los criterios de orden disponibles
    campo = {"1": "nombre", "2": "poblacion", "3": "superficie"}[                       #diccionario que traduce la opción elegida al nombre del campo
        pedir_opcion("Opción: ", ("1", "2", "3"))]                                      #pide la opción y la usa como clave del diccionario
    orden = pedir_opcion("1) Ascendente  2) Descendente: ", ("1", "2"))                 #pide el sentido del orden (1 o 2)
    mostrar_paises(ordenar_paises(paises, campo, descendente=(orden == "2")))           #ordena (descendente si eligió 2) y muestra


def mostrar_menu():                                      #define la función que imprime el menú principal
    print("\n" + "=" * 40)                               #imprime una línea de 40 signos igual
    print("   GESTIÓN DE DATOS DE PAÍSES")               
    print("=" * 40)                                      #imprime otra línea de 40 signos igual
    print("1. Agregar un país")                          
    print("2. Actualizar población y superficie")        
    print("3. Buscar país por nombre")                   
    print("4. Filtrar países")                         
    print("5. Ordenar países")                           
    print("6. Mostrar estadísticas")                    
    print("7. Listar todos los países")                  
    print("0. Salir")                                    


def main():                                                             #define la función principal que controla todo el programa
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_CSV_DEFECTO                        #usa el CSV pasado por argumento o, si no hay, el CSV por defecto
    paises, errores = cargar_paises(ruta)                                                #carga los países del CSV y recibe los errores encontrados
    if errores:                                                                          #si hubo errores al leer el CSV
        print("Advertencia. Problemas al leer el CSV:")                                 #imprime el aviso general
        for error in errores:                                                            #recorre cada error
            print("  -", error)                                                          #imprime el detalle de cada error
    print(f"Se cargaron {len(paises)} países desde '{os.path.basename(ruta)}'.")         #informa cuántos países se cargaron y de qué archivo


    while True:                                                     #repite el menú hasta que el usuario elija salir
            mostrar_menu()                                              #imprime el menú principal
            opcion = input("Seleccione una opción: ").strip()           #lee la opción elegida y quita espacios
            if opcion == "1":                           
                opcion_agregar(paises, ruta)             #ejecuta agregar país
            elif opcion == "2":                          
                opcion_actualizar(paises, ruta)          #ejecuta actualizar país
            elif opcion == "3":                          
                opcion_buscar(paises)                    #ejecuta buscar país
            elif opcion == "4":                         
                opcion_filtrar(paises)                   #ejecuta filtrar países
            elif opcion == "5":                         
                opcion_ordenar(paises)                   #ejecuta ordenar países
            elif opcion == "6":                          
                mostrar_estadisticas(paises)             #muestra las estadísticas
            elif opcion == "7":                          
                mostrar_paises(paises)                   #lista todos los países
            elif opcion == "0":                          
                print("¡Hasta luego!")                   
                break                                    #sale del bucle y termina el programa
            else:                                        #si escribió cualquier otra cosa
                print("Opción inválida. Ingrese un número del 0 al 7.")         #informa que la opción no es válida


if __name__ == "__main__":                   #comprueba que el archivo se ejecuta directamente (no importado)
    main()                                   #inicia el programa