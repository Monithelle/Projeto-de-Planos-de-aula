import os
from flask import Flask
from .config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensões
    db.init_app(app)

    # Registrar Blueprints
    from .routes.auth import auth_bp
    from .routes.prof import prof_bp
    from .routes.admin import admin_bp
    from .routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(prof_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Criação das pastas necessárias
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Context processors úteis nos templates
    @app.context_processor
    def inject_globals():
        return {
            'ano_atual': 2026,
            'sistema_nome': 'Planos de Aula'
        }

    return app

