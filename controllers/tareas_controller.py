from neo4j_connection import db

def obtener_tareas(alumno_id=None):
    if alumno_id:
        q = """
        MATCH (a:Alumno {id:$id})-[:TIENE_TAREA]->(t:Tarea)
        RETURN t.id AS id, t.titulo AS titulo, t.fecha AS fecha,
               t.descripcion AS descripcion, t.estatus AS estatus
        ORDER BY t.fecha
        """
        return db.query(q, {"id": alumno_id})
    else:
        q = """
        MATCH (t:Tarea)
        RETURN t.id AS id, t.titulo AS titulo, t.fecha AS fecha,
               t.descripcion AS descripcion, t.estatus AS estatus
        ORDER BY t.fecha
        """
        return db.query(q)

def crear_tarea_multi(alumno_ids, all_flag, datos):
    if all_flag:
        alumnos = db.query("MATCH (a:Alumno) RETURN a.id AS id")
        alumno_ids = [r["id"] for r in alumnos]
    if not alumno_ids:
        return {"error": "Debes especificar alumno_ids o all=true"}

    create_task = """
    CREATE (t:Tarea {
        id: randomUUID(),
        titulo: $titulo,
        fecha: $fecha,
        descripcion: $descripcion,
        estatus: $estatus
    })
    RETURN t.id AS tarea_id
    """
    tarea_result = db.query(create_task, datos)
    tarea_id = tarea_result[0]["tarea_id"]

    rel_query = """
    UNWIND $ids AS aid
    MATCH (a:Alumno {id: aid}), (t:Tarea {id: $tarea_id})
    MERGE (a)-[:TIENE_TAREA]->(t)
    RETURN a.id AS alumno_id
    """
    linked = db.query(rel_query, {"ids": alumno_ids, "tarea_id": tarea_id})

    return {"tarea_id": tarea_id, "asignada_a": [r["alumno_id"] for r in linked]}

def actualizar_tarea(id, datos):
    q = """
    MATCH (t:Tarea {id:$id})
    SET t.titulo = $titulo,
        t.fecha = $fecha,
        t.descripcion = $descripcion,
        t.estatus = $estatus
    RETURN t.id AS id
    """
    res = db.query(q, {"id": id, **datos})
    return {"id": res[0]["id"]} if res else {"error": "Tarea no encontrada"}

def eliminar_tarea(id):
    q = """
    MATCH (t:Tarea {id:$id})
    OPTIONAL MATCH (a:Alumno)-[r:TIENE_TAREA]->(t)
    OPTIONAL MATCH (n:Nota)-[dn:DE_TAREA]->(t)
    DELETE r, dn, n, t
    RETURN $id AS eliminado
    """
    res = db.query(q, {"id": id})
    return {"eliminado": res[0]["eliminado"]} if res else {"error": "Tarea no encontrada"}