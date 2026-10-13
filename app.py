from flask import Flask, render_template
from config import Config
from database import db, inicializar_banco

# Importação dos três blueprints desenvolvidos por vocês
from auditoria_forense.routes import auditoria_bp
from pesquisa_inteligente.routes import pesquisa_bp
from analise_estrategica.routes import analise_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco de dados centralizado
inicializar_banco(app)

# Junta todas as ramificações de rotas no servidor central do Flask
app.register_blueprint(auditoria_bp)
app.register_blueprint(pesquisa_bp)
app.register_blueprint(analise_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)