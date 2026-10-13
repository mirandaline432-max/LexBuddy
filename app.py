from flask import Flask, render_template
from config import Config
from database import db, inicializar_banco

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco de dados relacional
inicializar_banco(app)

@app.route('/')
def home():
    # Renderiza a página inicial pública do sistema
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)