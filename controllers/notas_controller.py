from neo4j_connection import db

def obtener_notas(alumno_id=None):
    if alumno_id:
        q = """
        MATCH (a:Alumno {id:$id})-[:TIENE_NOTA]->(n:Nota)-[:DE_TAREA]->(t:Tarea)
        RETURN n.id AS id, n.valor AS valor, n.comentario AS comentario,
               t.id AS tarea_id, t.titulo AS tarea, t.fecha AS fecha
        ORDER BY t.fecha
        """
        return db.query(q, {"id": alumno_id})
    else:
        q = """
        MATCH (a:Alumno)-[:TIENE_NOTA]->(n:Nota)-[:DE_TAREA]->(t:Tarea)
        RETURN n.id AS id, n.valor AS valor, n.comentario AS comentario,
               a.id AS alumno_id, a.nombre AS alumno,
               t.id AS tarea_id, t.titulo AS tarea, t.fecha AS fecha
        ORDER BY t.fecha, alumno
        """
        return db.query(q)

def crear_o_actualizar_nota(alumno_id, tarea_id, datos):
    q = """
    MATCH (a:Alumno {id:$alumno_id}), (t:Tarea {id:$tarea_id})
    OPTIONAL MATCH (a)-[:TIENE_NOTA]->(n:Nota)-[:DE_TAREA]->(t)
    WITH a,t,n
    CALL apoc.do.when(
      n IS NULL,
      'CREATE (n:Nota {id: randomUUID(), valor:$valor, comentario:$comentario})
       MERGE (a)-[:TIENE_NOTA]->(n)
       MERGE (n)-[:DE_TAREA]->(t)
       RETURN n',
      'SET n.valor=$valor, n.comentario=$comentario RETURN n',
      {valor:$valor, comentario:$comentario, a:a, t:t, n:n}
    ) YIELD value
    RETURN value.n.id AS nota_id
    """
    res = db.query(q, {
        "alumno_id": alumno_id,
        "tarea_id": tarea_id,
        "valor": datos.get("valor"),
        "comentario": datos.get("comentario", "")
    })
    return {"nota_id": res[0]["nota_id"]} if res else {"error": "No se pudo crear/actualizar la nota"}

def eliminar_nota(id):
    q = "MATCH (n:Nota {id:$id}) DETACH DELETE n RETURN $id AS eliminado"
    res = db.query(q, {"id": id})
    return {"eliminado": res[0]["eliminado"]} if res else {"error": "Nota no encontrada"}