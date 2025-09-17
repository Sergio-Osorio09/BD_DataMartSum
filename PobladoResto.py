import pandas as pd
import mysql.connector
import random
from datetime import datetime, date

# Conectar a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="DataMartSUM"
)
cursor = conn.cursor()

# Función para obtener IDs existentes
def get_existing_ids(table_name, id_column):
    cursor.execute(f"SELECT {id_column} FROM {table_name}")
    return [row[0] for row in cursor.fetchall()]

# 1. Poblar DimPeriodo
print("Poblando DimPeriodo...")
periodos = [
    ("2025-2", 2025, "2", date(2025, 8, 1), date(2025, 12, 20)),
    ("2025-1", 2025, "1", date(2025, 3, 1), date(2025, 7, 15)),
    ("2024-2", 2024, "2", date(2024, 8, 1), date(2024, 12, 20)),
    ("2024-1", 2024, "1", date(2024, 3, 1), date(2024, 7, 15))
]

for periodo in periodos:
    try:
        cursor.execute("""
            INSERT INTO DimPeriodo (codigo_periodo, anio, semestre, fecha_inicio, fecha_fin)
            VALUES (%s, %s, %s, %s, %s)
        """, periodo)
    except mysql.connector.Error as e:
        print(f"Error al insertar periodo {periodo[0]}: {e}")

conn.commit()

# 2. Poblar DimCarrera
print("Poblando DimCarrera...")
carreras = [
    ("ISW", "Ingeniería de Software", 10, 210, "2018"),
    ("ISI", "Ingeniería de Sistemas e Informática", 10, 210, "2018"),
    ("CS", "Ciencia de la Computación", 10, 200, "2018")
]

for carrera in carreras:
    try:
        cursor.execute("""
            INSERT INTO DimCarrera (codigo_carrera, nombre_carrera, duracion, creditos_totales, plan_estudios)
            VALUES (%s, %s, %s, %s, %s)
        """, carrera)
    except mysql.connector.Error as e:
        print(f"Error al insertar carrera {carrera[0]}: {e}")

conn.commit()

# 3. Poblar DimDocente (extraídos del PDF)
print("Poblando DimDocente...")
docentes_data = [
    ("07240690", "MARIA ROSA", "DAMASO", "RIOS", "F", "Ingeniería de Sistemas", "Magíster", "Principal"),
    ("10275035", "YOLANDA OLIVIA", "ORELLANA", "MANRIQUE", "F", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("41388541", "JHONATHAN", "AGUILAR", "CORONEL", "M", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("43091255", "BORJA LUIS", "HUAMAN", "TINCO", "M", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("45286733", "RONALD ALONSO", "MELGAREJO", "SOLIS", "M", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("15584946", "CARMEN VIOLETA", "DIONICIO", "MEJÍA", "F", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("40764399", "EDWIN", "MARAVI", "PERCCA", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("21571331", "LUIS LEONCIO", "BARBOZA", "CARAPE", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("42229911", "JHOHANNA", "RIOS", "DELGADO", "F", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("44752092", "PILAR", "LUCIO", "PONCE", "F", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("040037", "ANA MARIA", "HUAYNA", "DUEÑAS", "F", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("09620253", "HEDDY LILIANA", "COLCA", "GARCIA", "F", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("06326376", "MIRYAM MILAGROS", "COSME", "FÉLIX", "F", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("47661582", "RICHARD JAVIER", "CUBAS", "BECERRA", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("40667934", "HELLEN GLORIA", "TERREROS", "NAVARRO", "F", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("026182", "JULIO", "FLORES", "DIONICIO", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("042086", "MABEL ERLINDA", "TESILLO", "QUISPE", "F", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("040818", "ALEJANDO LADISLAO", "TRUJILLO", "QUINDE", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("040920", "MELCHOR NICOLÁS", "LLOSA", "DEMARTINI", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("044049", "ROLANDO WILDER", "ADRIANO", "PEÑA", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("043478", "LUIS", "MENDOZA", "CARBAJAL", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("017744", "RAUL ÁNGEL", "CONTRERAS", "CONTRERAS", "M", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("06122577", "PETRONILA MERIDA", "FANOLA", "MERINO", "F", "Ingeniería de Sistemas", "Doctor", "Principal"),
    ("07578149", "DAVID FELIX", "CANDELA", "ARCE", "M", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("07493618", "ALEXANDER EDUARDO", "INGA", "ALVA", "M", "Ingeniería de Sistemas", "Magíster", "Asociado"),
    ("041982", "GUSTAVO", "ARREDONDO", "CASTILLO", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("08803A", "PABLO JESUS", "ROMERO", "NAUPARI", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("044654", "LUIS ALBERTO", "NAVARRO", "HUAMANÍ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("045174", "RICHARD SAÚL", "TORIBIO", "SAAVEDRA", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("041565", "JOSÉ ANTONIO", "CHUMACERO", "CALLE", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("047624", "ERNESTO DAVID", "CANCHO", "RODRÍGUEZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("041331", "JUAN HONORATO", "LUNA", "VALDEZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("041871", "CARLOS ERNESTO", "CHÁVEZ", "HERRERA", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("087998", "CARLOS EDMUNDO", "NAVARRO", "DEPAZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("049179", "JUAN RICARDO", "TAPIA", "CARBAJAL", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("095753", "ZHING FONG", "LAM", "-", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("010162", "JAVIER ELMER", "CABRERA", "DÍAZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("055867", "DANIEL", "QUINTO", "PAZCE", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A5307", "YUDI LUCERO", "GUZMÁN", "MONTEZA", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A7565", "JAVIER ANTONIO", "PRUDENCIO", "VIDAL", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("099589", "FELIX ARMANDO", "FERMIN", "PEREZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("018686", "AUGUSTO PARCEMON", "CORTEZ", "VÁSQUEZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A5306", "IGOR JOVINO", "AGUILAR", "ALONSO", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1877", "ARTURO ALEJANDRO", "BARTRA", "MORE", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("091081", "LUIS ALBERTO", "ALARCÓN", "LOAYZA", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("46299018", "MARCO ANTONIO", "SOBREVILLA", "CABEZUDO", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("09571E", "JOHNLEOGARD", "TRUJILLO", "TRUJILLO", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("02099E", "LUZ CORINA", "DEL PINO", "RODRÍGUEZ", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("089575", "GILBERTO ANIBAL", "SALINAS", "AZAÑA", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A5140", "MIGUEL ÁNGEL", "PINGLO", "RAMÍREZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A5230", "CIRO", "RODRÍGUEZ", "RODRÍGUEZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("099562", "ERWIN", "MAC DOWALL", "REYNOSO", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1876", "SUMIKO ELIZABETH", "MURAKAMI", "DE LA CRUZ", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A0314", "ARMANDO DAVID", "ESPINOZA", "ROBLES", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A4525", "ROSA", "MENÉNDEZ", "MUERAS", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1874", "HUGO RAFAEL", "CORDERO", "SÁNCHEZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A4824", "LUZ SUSSY", "BAYONA", "ORÉ", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1875", "LENIS ROSSI", "WONG", "PORTILLO", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A0690", "PABLO EDWIN", "LÓPEZ", "VILLANUEVA", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("094315", "ROBERT ELIAS", "ESPINOZA", "DOMINGUEZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A9126", "IVAN CARLO", "PETRLIK", "AZABACHE", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("095702", "VÍCTOR HUGO", "BUSTAMANTE", "OLIVERA", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("09795E", "JORGE RAÚL", "DIAZ", "MUÑANTE", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1232", "MARCO ANTONIO", "CORAL", "YGNACIO", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("095729", "JORGE LUIS", "CHÁVEZ", "SOTO", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1609", "JORGE LUIS", "ZAVALETA", "CAMPOS", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A5291", "MARIO AGUSTÍN", "HUAPAYA", "CHUMPITAZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A0307", "ROLANDO ALBERTO", "MAGUIÑA", "PÉREZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1981", "WINSTON IGNACIO", "UGAZ", "CACHAY", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("08232375", "JORGE LUIS", "DEL MAR", "ARZOLA", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A2417", "HUGO DAVID", "CALDERON", "VILCA", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A6225", "MARÍA ELIZABETH", "PUELLES", "BULNES", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("011797", "CARLOS ALBERTO", "CÁNEPA", "PÉREZ", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1873", "JOEL FERNANDO", "MACHADO", "VICENTE", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A9124", "PEDRO MARTIN", "LEZAMA", "GONZALES", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A9127", "TEODORO MANUEL", "ANDRADE", "MOGOLLON", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A4524", "LUZ SUSSY", "BAYONA", "ORÉ", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A0182", "MARIA ELENA", "RUIZ", "RIVERA", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1607", "JAVIER ARTURO", "GAMBOA", "CRUZADO", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A6226", "JOSÉ ALFREDO", "HERRERA", "QUISPE", "M", "Ingeniería de Software", "Doctor", "Principal"),
    ("055123", "LUZMILA ELISA", "PRÓ", "CONCEPCIÓN", "F", "Ingeniería de Software", "Doctor", "Principal"),
    ("0A1871", "CARLOS ERNESTO", "CHÁVEZ", "HERRERA", "M", "Ingeniería de Software", "Doctor", "Principal")
]

for docente in docentes_data:
    try:
        cursor.execute("""
            INSERT INTO DimDocente (codigo_docente, nombre, apellido_paterno, apellido_materno, 
                                   genero, facultad, grado_academico, categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, docente)
    except mysql.connector.Error as e:
        print(f"Error al insertar docente {docente[0]}: {e}")

conn.commit()

# 4. Poblar DimCurso (extraídos del PDF)
print("Poblando DimCurso...")
cursos_data = [
    # Ciclo 1
    ("INE002", "PROGRAMACIÓN Y COMPUTACIÓN", 2, 1, 1, 1, "Obligatorio", "Activo"),
    ("INE013", "EMPRENDIMIENTO E INNOVACIÓN", 2, 1, 1, 1, "Obligatorio", "Activo"),
    ("INO104", "CÁLCULO I", 4, 3, 1, 1, "Obligatorio", "Activo"),
    ("INO106", "ÁLGEBRA Y GEOMETRÍA ANALÍTICA", 4, 3, 1, 1, "Obligatorio", "Activo"),
    
    # Ciclo 2
    ("INO201", "REDACCIÓN Y TÉCNICAS DE COMUNICACIÓN EFECTIVA II", 3, 2, 1, 2, "Obligatorio", "Activo"),
    ("INO202", "INVESTIGACIÓN FORMATIVA", 3, 2, 1, 2, "Obligatorio", "Activo"),
    ("INO203", "REALIDAD NACIONAL Y MUNDIAL", 2, 1, 1, 2, "Obligatorio", "Activo"),
    ("INO204", "CÁLCULO II", 4, 3, 1, 2, "Obligatorio", "Activo"),
    ("INO205", "FÍSICA I", 4, 3, 1, 2, "Obligatorio", "Activo"),
    ("INO206", "QUÍMICA GENERAL", 4, 3, 1, 2, "Obligatorio", "Activo"),
    ("INO207", "INTRODUCCIÓN A LAS CIENCIAS E INGENIERIA", 2, 1, 1, 2, "Obligatorio", "Activo"),
    
    # Ciclo 3
    ("202W0301", "ALGORÍTMICA I", 4, 3, 1, 3, "Obligatorio", "Activo"),
    ("202W0302", "ESTADÍSTICA", 3, 2, 1, 3, "Obligatorio", "Activo"),
    ("202W0303", "FISICA ELÉCTRONICA", 3, 2, 1, 3, "Obligatorio", "Activo"),
    ("202W0304", "INGENIERÍA ECONÓMICA", 3, 2, 1, 3, "Obligatorio", "Activo"),
    ("202W0305", "INTRODUCCIÓN AL DESARROLLO DE SOFTWARE", 3, 2, 1, 3, "Obligatorio", "Activo"),
    ("202W0306", "MATEMÁTICA BÁSICA", 4, 3, 1, 3, "Obligatorio", "Activo"),
    ("202W0307", "ORGANIZACIÓN Y ADMINISTRACIÓN", 3, 2, 1, 3, "Obligatorio", "Activo"),
    
    # Ciclo 4
    ("202W0401", "ALGORÍTMICA II", 4, 3, 1, 4, "Obligatorio", "Activo"),
    ("202W0402", "CONTABILIDAD PARA LA GESTIÓN", 3, 2, 1, 4, "Obligatorio", "Activo"),
    ("202W0404", "MATEMÁTICA DISCRETA", 3, 2, 1, 4, "Obligatorio", "Activo"),
    ("202W0406", "PROCESOS DE SOFTWARE", 3, 2, 1, 4, "Obligatorio", "Activo"),
    ("202W0407", "SISTEMAS DIGITALES", 3, 2, 1, 4, "Obligatorio", "Activo"),
    
    # Ciclo 5
    ("202W0501", "ANÁLISIS Y DISEÑO DE ALGORITMOS", 3, 2, 1, 5, "Obligatorio", "Activo"),
    ("202W0502", "ARQUITECTURA DE COMPUTADORAS", 3, 2, 1, 5, "Obligatorio", "Activo"),
    ("202W0503", "CALIDAD DE SOFTWARE", 3, 2, 1, 5, "Obligatorio", "Activo"),
    ("202W0504", "COMPUTACIÓN VISUAL", 3, 2, 1, 5, "Obligatorio", "Activo"),
    ("202W0505", "ESTRUCTURA DE DATOS", 4, 3, 1, 5, "Obligatorio", "Activo"),
    ("202W0506", "ECONOMÍA PARA LA GESTIÓN", 3, 2, 1, 5, "Obligatorio", "Activo"),
    ("202W0507", "INGENIERÍA DE REQUISITOS", 4, 3, 1, 5, "Obligatorio", "Activo"),
    
    # Ciclo 6
    ("202W0601", "ASEGURAMIENTO DE LA CALIDAD DEL SOFTWARE", 3, 2, 1, 6, "Obligatorio", "Activo"),
    ("202W0602", "BASE DE DATOS I", 4, 3, 1, 6, "Obligatorio", "Activo"),
    ("202W0603", "DISEÑO DE SOFTWARE", 4, 3, 1, 6, "Obligatorio", "Activo"),
    ("202W0604", "FORMACIÓN DE EMPRESAS DE SOFTWARE", 3, 2, 1, 6, "Obligatorio", "Activo"),
    ("202W0605", "GESTIÓN DE LA CONFIGURACIÓN DEL SOFTWARE", 3, 2, 1, 6, "Obligatorio", "Activo"),
    ("202W0606", "INTERACCIÓN HOMBRE COMPUTADOR", 3, 2, 1, 6, "Obligatorio", "Activo"),
    ("202W0607", "SISTEMAS OPERATIVOS", 3, 2, 1, 6, "Obligatorio", "Activo"),
    
    # Ciclo 7
    ("202W0701", "ARQUITECTURA DE SOFTWARE", 4, 3, 1, 7, "Obligatorio", "Activo"),
    ("202W0702", "BASE DE DATOS II", 4, 3, 1, 7, "Obligatorio", "Activo"),
    ("202W0703", "EXPERIENCIA DE USUARIO Y USABILIDAD", 3, 2, 1, 7, "Obligatorio", "Activo"),
    ("202W0704", "GESTIÓN DE PROYECTO DE SOFTWARE", 3, 2, 1, 7, "Obligatorio", "Activo"),
    ("202W0705", "INTELIGENCIA ARTIFICIAL", 3, 2, 1, 7, "Obligatorio", "Activo"),
    ("202W0706", "MÉTODOS FORMALES PARA PRUEBAS", 3, 2, 1, 7, "Obligatorio", "Activo"),
    ("202W0707", "REDES Y TRANSMISIÓN DE DATOS", 3, 2, 1, 7, "Obligatorio", "Activo"),
    
    # Ciclo 8
    ("202W0801", "AUTOMATIZACIÓN Y CONTROL DE SOFTWARE", 3, 2, 1, 8, "Obligatorio", "Activo"),
    ("202W0802", "INTELIGENCIA DE NEGOCIOS", 3, 2, 1, 8, "Obligatorio", "Activo"),
    ("202W0803", "METODOLOGÍA DE LA INVESTIGACIÓN", 2, 1, 1, 8, "Obligatorio", "Activo"),
    ("202W0804", "MINERÍA DE DATOS", 3, 2, 1, 8, "Obligatorio", "Activo"),
    ("202W0805", "PROGRAMACIÓN CONCURRENTE Y PARALELA", 3, 2, 1, 8, "Obligatorio", "Activo"),
    ("202W0806", "SEGURIDAD DEL SOFTWARE", 3, 2, 1, 8, "Obligatorio", "Activo"),
    ("202W0807", "TALLER DE CONSTRUCCIÓN DE SOFTWARE WEB", 3, 2, 1, 8, "Obligatorio", "Activo"),
    ("202W0808", "VERIFICACIÓN Y VALIDACIÓN DE SOFTWARE", 3, 2, 1, 8, "Obligatorio", "Activo"),
    
    # Ciclo 9
    ("202W0901", "DESARROLLO DE TESIS", 2, 1, 1, 9, "Obligatorio", "Activo"),
    ("202W0902", "GARANTÍA DE SOFTWARE", 3, 2, 1, 9, "Obligatorio", "Activo"),
    ("202W0903", "GERENCIA DE TECNOLOGÍA DE LA INFORMACIÓN", 3, 2, 1, 9, "Obligatorio", "Activo"),
    ("202W0904", "GESTIÓN DE MANTENIMIENTO DEL SOFTWARE", 3, 2, 1, 9, "Obligatorio", "Activo"),
    ("202W0905", "GESTIÓN DE RIESGO DEL SOFTWARE", 3, 2, 1, 9, "Obligatorio", "Activo"),
    ("202W0906", "INTERNET DE LAS COSAS", 3, 2, 1, 9, "Obligatorio", "Activo"),
    ("202W0907", "TALLER DE CONSTRUCCIÓN DE SOFTWARE MÓVIL", 3, 2, 1, 9, "Obligatorio", "Activo"),
    ("202W0908", "SOFTWARE INTELIGENTE", 3, 2, 1, 9, "Obligatorio", "Activo"),
    
    # Ciclo 10
    ("202W1001", "ANALÍTICA DE DATOS", 3, 2, 1, 10, "Obligatorio", "Activo"),
    ("202W1002", "DESARROLLO DE TESIS II", 2, 1, 1, 10, "Obligatorio", "Activo"),
    ("202W1003", "PRÁCTICA PRE PROFESIONAL", 4, 3, 1, 10, "Obligatorio", "Activo"),
    ("202W1004", "TALLER DE APLICACIONES SOCIALES", 3, 2, 1, 10, "Obligatorio", "Activo"),
    ("202W1005", "TENDENCIAS DE ARQUITECTURA DE SOFTWARE", 3, 2, 1, 10, "Obligatorio", "Activo"),
    ("202W1006", "TENDENCIAS EN INGENIERIA DE SOFTWARE Y GESTIÓN", 3, 2, 1, 10, "Obligatorio", "Activo")
]

for curso in cursos_data:
    try:
        cursor.execute("""
            INSERT INTO DimCurso (codigo_curso, nombre_curso, creditos, horas_teoria, horas_practica, 
                                 ciclo_curso, tipo_curso, estado_curso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, curso)
    except mysql.connector.Error as e:
        print(f"Error al insertar curso {curso[0]}: {e}")

conn.commit()

# 5. Poblar FactInscripcion con datos de ejemplo
print("Poblando FactInscripcion...")

# Obtener IDs existentes
estudiante_ids = get_existing_ids("DimEstudiante", "id_estudiante")
carrera_ids = get_existing_ids("DimCarrera", "id_carrera")
curso_ids = get_existing_ids("DimCurso", "id_curso")
docente_ids = get_existing_ids("DimDocente", "id_docente")
periodo_ids = get_existing_ids("DimPeriodo", "id_periodo")

# Crear inscripciones de ejemplo
for i in range(1000):  # Crear 1000 inscripciones de ejemplo
    id_estudiante = random.choice(estudiante_ids)
    id_carrera = random.choice(carrera_ids)
    id_curso = random.choice(curso_ids)
    id_docente = random.choice(docente_ids)
    id_periodo = random.choice(periodo_ids)
    
    # Generar nota final entre 0 y 20
    nota_final = round(random.uniform(0, 20), 2)
    
    # Determinar si el curso fue aprobado (nota >= 11)
    curso_aprobado = nota_final >= 11
    
    # Número de veces que ha llevado el curso (1-3)
    veces_curso = random.randint(1, 3)
    
    try:
        cursor.execute("""
            INSERT INTO FactInscripcion (id_estudiante, id_carrera, id_curso, id_docente, id_periodo, 
                                        nota_final, curso_aprobado, veces_curso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_estudiante, id_carrera, id_curso, id_docente, id_periodo, 
              nota_final, curso_aprobado, veces_curso))
    except mysql.connector.Error as e:
        print(f"Error al insertar inscripción {i+1}: {e}")

conn.commit()

# Cerrar conexión
cursor.close()
conn.close()

print("✅ Poblado de todas las tablas completado correctamente.")