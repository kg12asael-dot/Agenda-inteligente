from neo4j_connection import db

def obtener_alumnos():
    query = """
    MATCH (a:Alumno)
    RETURN a.id AS id, a.nombre AS nombre
    ORDER BY a.nombre
    """
    return db.query(query)

def obtener_alumno(id_alumno):
    query = """
    MATCH (a:Alumno {id:$id_alumno})
    RETURN a.id AS id, a.nombre AS nombre
    """
    return db.query(query, {"id_alumno": id_alumno})

def crear_alumno(datos):
    query = """
    CREATE (a:Alumno {
        id: randomUUID(),
        nombre: $nombre
    })
    RETURN a.id AS id, a.nombre AS nombre
    """
    return db.query(query, datos)

def actualizar_alumno(id_alumno, datos):
    query = """
    MATCH (a:Alumno {id:$id_alumno})
    SET a.nombre = $nombre
    RETURN a.id AS id, a.nombre AS nombre
    """
    datos["id_alumno"] = id_alumno
    return db.query(query, datos)

def eliminar_alumno(id_alumno):
    query = """
    MATCH (a:Alumno {id:$id_alumno})
    DETACH DELETE a
    """
    return db.query(query, {"id_alumno": id_alumno})

def obtener_tareas_alumno(id_alumno):
    query = """
    MATCH (a:Alumno {id:$id_alumno})-[:TIENE_TAREA]->(t:Tarea)
    RETURN t.id AS id, t.titulo AS titulo, t.fecha AS fecha
    ORDER BY t.fecha
    """
    return db.query(query, {"id_alumno": id_alumno})

def obtener_notas_alumno(id_alumno):
    query = """
    MATCH (a:Alumno {id:$id_alumno})-[:TIENE_NOTA]->(n:Nota)
    RETURN n.id AS id, n.titulo AS titulo, n.contenido AS contenido
    """
    return db.query(query, {"id_alumno": id_alumno})

def obtener_recordatorios_alumno(id_alumno):
    query = """
    MATCH (a:Alumno {id:$id_alumno})-[:TIENE_RECORDATORIO]->(r:Recordatorio)
    RETURN r.id AS id, r.titulo AS titulo, r.fecha AS fecha
    ORDER BY r.fecha
    """
    return db.query(query, {"id_alumno": id_alumno})

def obtener_eventos_alumno(id_alumno):
    query = """
    MATCH (a:Alumno {id:$id_alumno})-[:TIENE_EVENTO]->(e:Evento)
    RETURN e.id AS id, e.titulo AS titulo, e.fecha AS fecha
    ORDER BY e.fecha
    """
    return db.query(query, {"id_alumno": id_alumno})