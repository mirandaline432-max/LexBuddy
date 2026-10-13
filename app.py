from flask import Flask, render_template
from config import Config
from database import db, inicializar_banco
from auditoria_forense.routes import auditoria_bp


# Importação exclusiva dos três blueprints oficiais da barra lateral do LexBuddy

from pesquisa_inteligente.routes import pesquisa_bp
from analise_estrategica.routes import analise_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco de dados unificado SQLite do LexBuddy
inicializar_banco(app)

# Registra os módulos oficiais do seu desenho

app.register_blueprint(pesquisa_bp)
app.register_blueprint(analise_bp)
app.register_blueprint(auditoria_bp)

@app.route('/')
def home():
    # Renderiza a sua Landing Page pública que já está corrigida
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)