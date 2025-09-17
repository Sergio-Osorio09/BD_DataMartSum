import pandas as pd
import mysql.connector

# === 1. Cargar CSV con configuraciones ===
df = pd.read_csv(
    r"C:\Users\SERGIO\Desktop\Proyecto\InteligenciaDeNegocios\resultados_limpio.csv",
    encoding="utf-8",
    dtype={"codigo": str},   # Forzamos que 'codigo' sea texto
    low_memory=False
)

# === 2. Eliminar duplicados en 'codigo' ===
df = df.drop_duplicates(subset=["Código"], keep="first")

# === 3. Conectar a MySQL ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",          # ⚠️ Cambia si tu usuario no es root
    password="123456", # ⚠️ Cambia por tu contraseña
    database="DataMartSUM"
)
cursor = conn.cursor()

# === 4. Query de inserción ===
sql = """
INSERT INTO DimEstudiante (
    codigo,
    Ap_Paterno,
    Ap_Materno,
    Nombres,
    Tipo_Documento,
    DNI,
    Sexo,
    Telefono,
    Direccion,
    Email,
    Anio_Ingreso,
    Modalidad_Ingreso,
    Facultad,
    Programa
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# === 5. Iterar filas e insertar ===
for _, row in df.iterrows():
    values = (
        row.get("Código"),
        row.get("Ap. Paterno"),
        row.get("Ap. Materno"),
        row.get("Nombres"),
        row.get("Tipo Documento"),
        row.get("DNI"),
        row.get("Sexo"),
        row.get("Teléfono"),
        row.get("Dirección"),
        row.get("Email"),
        row.get("Año Ingreso"),
        row.get("Modalidad Ingreso"),
        row.get("Facultad"),
        row.get("Programa")
    )
    # Reemplazar NaN con None
    values = tuple(None if pd.isna(v) else v for v in values)

    try:
        cursor.execute(sql, values)
    except mysql.connector.Error as e:
        print(f"❌ Error al insertar código {row.get('codigo')}: {e}")

# === 6. Confirmar y cerrar ===
conn.commit()
cursor.close()
conn.close()

print("✅ Poblado completado correctamente.")
