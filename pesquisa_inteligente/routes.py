from flask import Flask, render_template
from config import Config
from database import db, inicializar_banco

# Importação dos dois módulos desenvolvidos
from auditoria_forense.routes import auditoria_bp
from pesquisa_inteligente.routes import pesquisa_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco de dados
inicializar_banco(app)

# Registra os módulos (Blueprints) de cada desenvolvedor
app.register_blueprint(auditoria_bp)
app.register_blueprint(pesquisa_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)