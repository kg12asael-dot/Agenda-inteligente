from neo4j_connection import db

alumnos = [
  {"id":"A001","nombre":"ALVAREZ SANCHEZ JOSE FRANCISCO"},
  {"id":"A002","nombre":"CRUZ MARTINEZ JUAN DAVID"},
  {"id":"A003","nombre":"ESTRADA SANCHEZ JENIFER"},
  {"id":"A004","nombre":"GARCIA GARCIA GIOVANNA"},
  {"id":"A005","nombre":"GONZALEZ MAGARIÑO KEVIN ASAEL"},
  {"id":"A006","nombre":"HERNANDEZ HERNANDEZ DIEGO ALEXANDRO"},
  {"id":"A007","nombre":"HIPOLITO CRUZ SARAHI"},
  {"id":"A008","nombre":"MACARIO CRUZ YENNI"},
  {"id":"A009","nombre":"MARTINEZ CHAVEZ CELESTE"},
  {"id":"A010","nombre":"MARTIÑON MORENO IVAN MICHEL"},
  {"id":"A011","nombre":"MORALES BERNARDINO ARIEL"},
  {"id":"A012","nombre":"NICOLAS BERNAL LUIS ARTURO"},
  {"id":"A013","nombre":"OLIVARES MORALES JOSE ARMANDO"},
  {"id":"A014","nombre":"RANGEL GUTIERREZ ALEJANDRO"},
  {"id":"A015","nombre":"SEGUNDO ESQUIVEL JAZMIN"},
  {"id":"A016","nombre":"YAÑEZ NAVARRETE BRAYAN"}
]

for a in alumnos:
    q = "MERGE (al:Alumno {id:$id}) SET al.nombre=$nombre"
    db.query(q, {"id": a["id"], "nombre": a["nombre"]})

print("Alumnos insertados/actualizados.")
