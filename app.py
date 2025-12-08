from flask import Flask, render_template, request, jsonify
from controllers.tareas_controller import (
    crear_tarea_multi, obtener_tareas, actualizar_tarea, eliminar_tarea
)
from controllers.recordatorios_controller import (
    crear_recordatorio_multi, obtener_recordatorios, actualizar_recordatorio, eliminar_recordatorio
)
from controllers.notas_controller import (
    obtener_notas, crear_o_actualizar_nota, eliminar_nota
)
from controllers.calendario_controller import (
    crear_evento_multi, obtener_eventos, actualizar_evento, eliminar_evento
)
from controllers.alumnos_controller import obtener_alumnos

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("base.html", current_year=2025)

@app.route("/tareas")
def tareas():
    return render_template("tareas.html", current_year=2025)

@app.route("/recordatorios")
def recordatorios():
    return render_template("recordatorios.html", current_year=2025)

@app.route("/notas")
def notas():
    return render_template("notas.html", current_year=2025)

@app.route("/calendario")
def calendario():
    return render_template("calendario.html", current_year=2025)

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html", current_year=2025)

@app.route("/api/alumnos")
def api_alumnos():
    return jsonify(obtener_alumnos())


@app.route("/api/tareas", methods=["GET"])
def api_tareas():
    alumno_id = request.args.get("alumno_id")
    return jsonify(obtener_tareas(alumno_id))

@app.route("/api/tareas", methods=["POST"])
def api_crear_tarea():
    body = request.json or {}
    alumno_ids = body.get("alumno_ids", [])
    all_flag = body.get("all", False)
    datos = {
        "titulo": body.get("titulo"),
        "fecha": body.get("fecha"),
        "descripcion": body.get("descripcion"),
        "estatus": body.get("estatus")
    }
    return jsonify(crear_tarea_multi(alumno_ids, all_flag, datos))

@app.route("/api/tareas/<id>", methods=["PUT"])
def api_actualizar_tarea(id):
    body = request.json or {}
    datos = {
        "titulo": body.get("titulo"),
        "fecha": body.get("fecha"),
        "descripcion": body.get("descripcion"),
        "estatus": body.get("estatus")
    }
    return jsonify(actualizar_tarea(id, datos))

@app.route("/api/tareas/<id>", methods=["DELETE"])
def api_eliminar_tarea(id):
    return jsonify(eliminar_tarea(id))


@app.route("/api/recordatorios", methods=["GET"])
def api_recordatorios():
    alumno_id = request.args.get("alumno_id")
    return jsonify(obtener_recordatorios(alumno_id))

@app.route("/api/recordatorios", methods=["POST"])
def api_crear_recordatorio():
    body = request.json or {}
    alumno_ids = body.get("alumno_ids", [])
    all_flag = body.get("all", False)
    datos = {
        "titulo": body.get("titulo"),
        "descripcion": body.get("descripcion", "")
    }
    return jsonify(crear_recordatorio_multi(alumno_ids, all_flag, datos))

@app.route("/api/recordatorios/<id>", methods=["PUT"])
def api_actualizar_recordatorio(id):
    body = request.json or {}
    datos = {
        "titulo": body.get("titulo"),
        "descripcion": body.get("descripcion", "")
    }
    return jsonify(actualizar_recordatorio(id, datos))

@app.route("/api/recordatorios/<id>", methods=["DELETE"])
def api_eliminar_recordatorio(id):
    return jsonify(eliminar_recordatorio(id))

@app.route("/api/notas", methods=["GET"])
def api_notas():
    alumno_id = request.args.get("alumno_id")
    return jsonify(obtener_notas(alumno_id))

@app.route("/api/notas", methods=["POST"])
def api_crear_nota():
    body = request.json or {}
    alumno_id = body.get("alumno_id")
    tarea_id = body.get("tarea_id")
    datos = {
        "valor": body.get("valor"),
        "comentario": body.get("comentario", "")
    }
    resultado = crear_o_actualizar_nota(alumno_id, tarea_id, datos)
    # Añadimos un mensaje más claro
    if "nota_id" in resultado:
        resultado["mensaje"] = "Nota creada/actualizada correctamente"
    return jsonify(resultado)

@app.route("/api/notas/<id>", methods=["DELETE"])
def api_eliminar_nota(id):
    resultado = eliminar_nota(id)
    if "eliminado" in resultado:
        resultado["mensaje"] = "Nota eliminada correctamente"
    return jsonify(resultado)

@app.route("/api/eventos", methods=["GET"])
def api_eventos():
    alumno_id = request.args.get("alumno_id")
    return jsonify(obtener_eventos(alumno_id))

@app.route("/api/eventos", methods=["POST"])
def api_crear_evento():
    body = request.json or {}
    alumno_ids = body.get("alumno_ids", [])
    all_flag = body.get("all", False)
    datos = {
        "titulo": body.get("titulo"),
        "fecha": body.get("fecha")
    }
    return jsonify(crear_evento_multi(alumno_ids, all_flag, datos))

@app.route("/api/eventos/<id>", methods=["PUT"])
def api_actualizar_evento(id):
    body = request.json or {}
    datos = {
        "titulo": body.get("titulo"),
        "fecha": body.get("fecha")
    }
    return jsonify(actualizar_evento(id, datos))

@app.route("/api/eventos/<id>", methods=["DELETE"])
def api_eliminar_evento(id):
    return jsonify(eliminar_evento(id))


if __name__ == "__main__":
    app.run(debug=True)