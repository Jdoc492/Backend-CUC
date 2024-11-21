from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuración de MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/prueba-tecnica-cuc'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jdoc4920'  # Cambia por una clave segura

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:5173", "https://cuc-frontend.vercel.app","https://cuc-frontend.netlify.app"]}},
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])

    # Registrar Blueprints
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.resources import resources_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(resources_bp, url_prefix='/resources')

    return app
