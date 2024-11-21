from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task, db

# Configurar el prefijo del Blueprint
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": t.id, "title": t.title, "status": t.status, "resources": t.resources} for t in tasks])


@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validar campos obligatorios
    if not data.get("title") or not data.get("status"):
        return jsonify({"error": "El título y el estado son obligatorios"}), 400

    # Validar que el estado sea válido
    if data["status"] not in ["Pendiente", "En Progreso", "Completada"]:
        return jsonify({"error": "Estado inválido"}), 400

    # Validar recursos
    valid_resources = data.get("resources", [])
    if not isinstance(valid_resources, list):
        return jsonify({"error": "Los recursos deben ser una lista"}), 400

    # Crear nueva tarea con los recursos
    new_task = Task(
        title=data["title"],
        status=data["status"],
        user_id=user_id,
        resources=valid_resources  # Guardar los IDs de los recursos
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Tarea creada exitosamente", "task_id": new_task.id}), 201


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()  # Obtiene el ID del usuario autenticado
    data = request.get_json()

    # Buscar la tarea
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    # Actualizar los campos de la tarea
    if "title" in data:
        task.title = data["title"]
    if "status" in data:
        task.status = data["status"]

    db.session.commit()

    return jsonify({"message": "Tarea actualizada exitosamente"}), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()  # Obtiene el ID del usuario autenticado

    # Buscar la tarea
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    # Eliminar la tarea
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Tarea eliminada exitosamente"}), 200
