from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()  # Obtiene el ID del usuario del token
    user = User.query.get(user_id)  # Busca al usuario en la base de datos
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validar datos obligatorios
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    # Verificar si el email ya está registrado
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "El correo ya está registrado"}), 400

    # Cifrar la contraseña con pbkdf2:sha256
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")

    # Crear nuevo usuario
    new_user = User(username=data["username"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Buscar usuario por email
    user = User.query.filter_by(email=data["email"]).first()

    # Verificar credenciales
    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Crear token JWT (usar el ID tal cual)
    access_token = create_access_token(identity=str(user.id))


    return jsonify({"access_token": access_token}), 200
