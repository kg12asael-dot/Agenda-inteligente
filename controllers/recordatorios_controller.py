from neo4j_connection import db

def obtener_recordatorios(alumno_id=None):
    if alumno_id:
        q = """
        MATCH (a:Alumno {id:$id})-[:TIENE_RECORDATORIO]->(r:Recordatorio)
        RETURN r.id AS id, r.titulo AS titulo, r.descripcion AS descripcion
        ORDER BY r.titulo
        """
        return db.query(q, {"id": alumno_id})
    else:
        q = """
        MATCH (r:Recordatorio)
        RETURN r.id AS id, r.titulo AS titulo, r.descripcion AS descripcion
        ORDER BY r.titulo
        """
        return db.query(q)

def crear_recordatorio_multi(alumno_ids, all_flag, datos):
    if all_flag:
        alumnos = db.query("MATCH (a:Alumno) RETURN a.id AS id")
        alumno_ids = [r["id"] for r in alumnos]
    if not alumno_ids:
        return {"error": "Debes especificar alumno_ids o all=true"}

    q = """
    CREATE (r:Recordatorio {id: randomUUID(), titulo:$titulo, descripcion:$descripcion})
    RETURN r.id AS recordatorio_id
    """
    res = db.query(q, datos)
    rid = res[0]["recordatorio_id"]

    rel = """
    UNWIND $ids AS aid
    MATCH (a:Alumno {id: aid}), (r:Recordatorio {id:$rid})
    MERGE (a)-[:TIENE_RECORDATORIO]->(r)
    RETURN a.id AS alumno_id
    """
    linked = db.query(rel, {"ids": alumno_ids, "rid": rid})
    return {"recordatorio_id": rid, "asignado_a": [r["alumno_id"] for r in linked]}

def actualizar_recordatorio(id, datos):
    q = """
    MATCH (r:Recordatorio {id:$id})
    SET r.titulo = $titulo, r.descripcion = $descripcion
    RETURN r.id AS id
    """
    res = db.query(q, {"id": id, **datos})
    return {"id": res[0]["id"]} if res else {"error": "Recordatorio no encontrado"}

def eliminar_recordatorio(id):
    q = """
    MATCH (r:Recordatorio {id:$id})
    DETACH DELETE r
    RETURN $id AS eliminado
    """
    res = db.query(q, {"id": id})
    return {"eliminado": res[0]["eliminado"]} if res else {"error": "Recordatorio no encontrado"}