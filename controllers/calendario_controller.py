from neo4j_connection import db

def obtener_eventos(alumno_id=None):
    if alumno_id:
        q = """
        MATCH (a:Alumno {id:$id})-[:TIENE_EVENTO]->(e:Evento)
        RETURN e.id AS id, e.titulo AS titulo, e.fecha AS fecha
        ORDER BY e.fecha
        """
        return db.query(q, {"id": alumno_id})
    else:
        q = """
        MATCH (e:Evento)
        RETURN e.id AS id, e.titulo AS titulo, e.fecha AS fecha
        ORDER BY e.fecha
        """
        return db.query(q)

def crear_evento_multi(alumno_ids, all_flag, datos):
    if all_flag:
        alumnos = db.query("MATCH (a:Alumno) RETURN a.id AS id")
        alumno_ids = [r["id"] for r in alumnos]
    if not alumno_ids:
        return {"error": "Debes especificar alumno_ids o all=true"}

    q = "CREATE (e:Evento {id: randomUUID(), titulo:$titulo, fecha:$fecha}) RETURN e.id AS evento_id"
    res = db.query(q, datos)
    eid = res[0]["evento_id"]

    rel = """
    UNWIND $ids AS aid
    MATCH (a:Alumno {id: aid}), (e:Evento {id:$eid})
    MERGE (a)-[:TIENE_EVENTO]->(e)
    RETURN a.id AS alumno_id
    """
    linked = db.query(rel, {"ids": alumno_ids, "eid": eid})
    return {"evento_id": eid, "asignado_a": [r["alumno_id"] for r in linked]}

def actualizar_evento(id, datos):
    q = """
    MATCH (e:Evento {id:$id})
    SET e.titulo = $titulo, e.fecha = $fecha
    RETURN e.id AS id
    """
    res = db.query(q, {"id": id, **datos})
    return {"id": res[0]["id"]} if res else {"error": "Evento no encontrado"}

def eliminar_evento(id):
    q = """
    MATCH (e:Evento {id:$id})
    DETACH DELETE e
    RETURN $id AS eliminado
    """
    res = db.query(q, {"id": id})
    return {"eliminado": res[0]["eliminado"]} if res else {"error": "Evento no encontrado"}