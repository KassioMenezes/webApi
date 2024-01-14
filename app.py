from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'db4free.net',
    'user': 'kassola',
    'password': 'Sysbot@2017',
    'database': 'kassioedu'
}

# Conectar ao banco de dados
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.route('/dados', methods=['GET'])
def obter_dados():
    # Consulta no banco de dados
    query = "SELECT * FROM usuario"
    cursor.execute(query)

    # Obtém os resultados
    dados = cursor.fetchall()

    # Transforma os resultados em um formato JSON
    dados_json = []
    for dado in dados:
        dado_dict = {
            'id': dado[0],
            'nome': dado[1],
            'senha': dado[2]
            # Adicione mais campos conforme necessário
        }
        dados_json.append(dado_dict)

    return jsonify({'dados': dados_json})

if __name__ == '__main__':
    app.run(debug=True)