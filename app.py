import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

class MinhaAplicacaoFlask:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        # Leitura inicial do arquivo DB.json
        with open('DB.json', 'r') as file:
            self.db_data = json.load(file)

        # Rotas da aplicação
        self.app.add_url_rule('/api/usuarios', 'obter_usuarios', self.obter_usuarios, methods=['GET'])
        self.app.add_url_rule('/api/usuarios/<int:user_id>', 'obter_usuario', self.obter_usuario, methods=['GET'])
        self.app.add_url_rule('/api/usuarios', 'criar_usuario', self.criar_usuario, methods=['POST'])
        self.app.add_url_rule('/api/usuarios/<int:user_id>', 'atualizar_usuario', self.atualizar_usuario, methods=['PUT'])
        self.app.add_url_rule('/api/usuarios/<int:user_id>', 'excluir_usuario', self.excluir_usuario, methods=['DELETE'])

    def ler_dados(self):
        with open('DB.json', 'r') as file:
            return json.load(file)

    def obter_usuarios(self):
        usuarios = self.ler_dados().get('usuarios', [])
        return render_template('usuarios.html', dados=usuarios, titulo='usuarios')

    def obter_usuario(self, user_id):
        db_data = self.ler_dados()
        usuario = next((usuario for usuario in db_data.get('usuarios', []) if usuario['id'] == user_id), None)
        if usuario:
            return render_template('usuarios.html', dados=[usuario], titulo='usuario')
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404

    def criar_usuario(self):
        novo_usuario = request.get_json()
        novo_usuario['id'] = max(user['id'] for user in self.db_data.get('usuarios', [])) + 1
        self.db_data['usuarios'].append(novo_usuario)

        # Atualiza o arquivo DB.json
        with open('DB.json', 'w') as file:
            json.dump(self.db_data, file, indent=2)

        return jsonify(novo_usuario), 201

    def atualizar_usuario(self, user_id):
        usuario = next((usuario for usuario in self.db_data.get('usuarios', []) if usuario['id'] == user_id), None)
        if usuario:
            dados_atualizados = request.get_json()
            usuario.update(dados_atualizados)

            # Atualiza o arquivo DB.json
            with open('DB.json', 'w') as file:
                json.dump(self.db_data, file, indent=2)

            return jsonify(usuario)
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404

    def excluir_usuario(self, user_id):
        self.db_data['usuarios'] = [usuario for usuario in self.db_data.get('usuarios', []) if usuario['id'] != user_id]

        # Atualiza o arquivo DB.json
        with open('DB.json', 'w') as file:
            json.dump(self.db_data, file, indent=2)

        return jsonify({'mensagem': 'Usuário excluído com sucesso'})

    def run(self):
        if __name__ == '__main__':
            self.app.run(host='0.0.0.0', port=5000, debug=True)

# Instanciação e execução da aplicação
minha_aplicacao = MinhaAplicacaoFlask()
minha_aplicacao.run()
