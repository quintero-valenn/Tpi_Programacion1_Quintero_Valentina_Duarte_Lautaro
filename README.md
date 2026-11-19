# TPI Programación 1 — Gestión de Datos de Países en Python
Trabajo Práctico Integrador: filtros, ordenamientos y estadísticas sobre un dataset de países.

## Enlaces 

| Recurso | Enlace |
|---|---|
|  Video demostrativo (permisos públicos) | **[PEGAR AQUÍ EL ENLACE AL VIDEO]** |
|  Documentación en PDF | [`Documentacion_TPI.pdf`](Documentacion_TPI.pdf) (subido en la raíz del repositorio) |

## Integrantes y participación

| Integrante | Participación |
| [Valentina Quintero] | [Búsqueda de información/filtros/ordenamientos, validaciones, parte del informe, video] |
| [Lautaro Duarte] | [Carga/guardado CSV, validaciones, estadísticas, menú, README, parte del informe, video] |

## Descripción

Aplicación de consola en **Python 3** que gestiona información de países (nombre, población,
superficie en km² y continente) a partir de un archivo **CSV**. Cada país es un **diccionario** y el
dataset completo es una **lista de diccionarios**. El código está modularizado en funciones
(*una función = una responsabilidad*), con validaciones de entrada y manejo de errores.

### Funcionalidades

1. **Agregar un país** (no se permiten campos vacíos ni duplicados).
2. **Actualizar** población y superficie de un país (Enter conserva el valor actual).
3. **Buscar** por nombre (coincidencia parcial o exacta, sin distinguir mayúsculas ni tildes).
4. **Filtrar** por continente, rango de población o rango de superficie.
5. **Ordenar** por nombre, población o superficie (ascendente o descendente).
6. **Estadísticas**: país con mayor y menor población, promedio de población, promedio de
   superficie y cantidad de países por continente.
7. **Listar** todos los países.

Los cambios (altas y actualizaciones) se guardan automáticamente en el CSV.

## Instrucciones de uso

Requisitos: **Python 3.8 o superior** 

```bash
# Ejecutar el programa (usa paises.csv de la misma carpeta)
python TPI_Programacion1.py

# Opcional: usar otro archivo CSV
python TPI_Programacion1.py otro_dataset.csv
```

### Formato del CSV

```csv
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
```

Continentes válidos: `África, América, Asia, Europa, Oceanía, Antártida`.
Si una fila tiene errores de formato, el programa informa el número de fila y el problema, la omite y continúa.

## Ejemplos de entradas/salidas

**Buscar (parcial) → 'arg'**

```
--- Buscar país por nombre ---
Texto a buscar: arg
1) Coincidencia parcial  2) Coincidencia exacta: 1

Nombre                   Población    Superficie km²  Continente
------------------------------------------------------------------
Argentina               45.376.763         2.780.400  América
------------------------------------------------------------------
Total: 1 país(es)
```

**Filtrar por rango de población (con validación)**

```
Población mínima: 100000000
Población máxima: 50000000
[ERROR] El mínimo no puede ser mayor que el máximo.
Población mínima: 50000000
Población máxima: 100000000
...
Total: 5 país(es)
```

**Agregar un país con datos inválidos**

```
Nombre: bolivia
Población (entero): abc
[ERROR] Ingrese un número entero válido (sin puntos ni letras).
Población (entero): -5
[ERROR] El número debe ser mayor a cero.
```

**Estadísticas**

```
=== ESTADÍSTICAS ===
País con mayor población : China (1.412.600.000)
País con menor población : Uruguay (3.473.727)
Promedio de población    : 210.931.619
Promedio de superficie   : 3.377.682 km²
Cantidad de países por continente:
  - África: 3
  - América: 6
  - Asia: 4
  - Europa: 5
  - Oceanía: 2
```

## Validaciones y manejo de errores

- Campos vacíos, números no enteros, negativos o cero → se vuelve a pedir el dato.
- Continente fuera de la lista y países duplicados → mensaje de error.
- Rango con mínimo mayor que el máximo → mensaje de error.
- Búsquedas o filtros sin resultados → mensaje informativo.
- CSV inexistente, encabezado incorrecto o filas defectuosas → se informan sin cerrar el programa.

## Documentación

El informe completo (marco teórico, diagramas de flujo, capturas, dificultades y bibliografía)
está en [`Documentacion_TPI.pdf`](Documentacion_TPI.pdf).
