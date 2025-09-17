import csv

# Ruta de entrada y salida
entrada = r"C:\Users\SERGIO\Desktop\Proyecto\InteligenciaDeNegocios\resultados.csv"
salida = r"C:\Users\SERGIO\Desktop\Proyecto\InteligenciaDeNegocios\resultados_limpio.csv"

# Contar cuántas columnas debe tener la cabecera
with open(entrada, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    columnas_esperadas = len(header)

print(f"El archivo debería tener {columnas_esperadas} columnas por fila.")

# Crear nuevo archivo limpio
with open(entrada, "r", encoding="utf-8") as f_in, \
     open(salida, "w", encoding="utf-8", newline="") as f_out:
    
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    # Escribimos el encabezado
    header = next(reader)
    writer.writerow(header)

    # Revisamos cada fila
    lineas_erroneas = 0
    total_lineas = 0
    for row in reader:
        total_lineas += 1
        if len(row) == columnas_esperadas:
            writer.writerow(row)
        else:
            lineas_erroneas += 1

print(f"Limpieza completada ✅")
print(f"Se procesaron {total_lineas} filas.")
print(f"Se eliminaron {lineas_erroneas} filas defectuosas.")
print(f"Archivo limpio guardado en: {salida}")
