from flask import Flask, render_template, redirect, url_for
from config import Config
from database import db, inicializar_banco
from flask_login import LoginManager

# Importação dos blueprints de todos os módulos
from auditoria_forense.routes import auditoria_bp
from pesquisa_inteligente.routes import pesquisa_bp
from analise_estrategica.routes import analise_bp
from contatos.routes import auth_bp  # O novo blueprint de login

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco de dados centralizado
inicializar_banco(app)

# Configuração do Gerenciador de Sessões de Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from contatos.models import Usuario
    return Usuario.query.get(int(user_id))

# Registra todos os módulos unificados no servidor central
app.register_blueprint(auditoria_bp)
app.register_blueprint(pesquisa_bp)
app.register_blueprint(analise_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)