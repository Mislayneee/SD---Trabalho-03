from flask import Flask, request, send_file, jsonify
from PIL import Image
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)#criar aplicação/servidor

PASTA_UPLOAD = 'imagens_enviadas'#nome da pasta das imagens
if not os.path.exists(PASTA_UPLOAD):
    os.makedirs(PASTA_UPLOAD)#verifica se a pasta existe, se não, cria

def inicializar_banco():
    conexao = sqlite3.connect('imagens.db')#cria banco
    cursor = conexao.cursor()#comandos sql
    cursor.execute('''CREATE TABLE IF NOT EXISTS imagens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        filtro TEXT,
                        data_hora TEXT)''')#criar tabela e campos
    conexao.commit()#salvar
    conexao.close()

@app.route('/enviar', methods=['POST'])#definir a rota do servidor e que recebe dados
def enviar_imagem():
    if 'arquivo' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files['arquivo']
    if arquivo.filename == '':
        return jsonify({"erro": "Nome de arquivo vazio"}), 400
    
    caminho_original = os.path.join(PASTA_UPLOAD, arquivo.filename)
    arquivo.save(caminho_original) #salvar imagem

    imagem = Image.open(caminho_original).convert("L")#aplicar o filtro preto e branco

    caminho_modificado = os.path.join(PASTA_UPLOAD, 'modificada_' + arquivo.filename)
    imagem.save(caminho_modificado)#salvar imagem modificada

    conexao = sqlite3.connect('imagens.db')
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO imagens (nome, filtro, data_hora) VALUES (?, ?, ?)", 
                   (arquivo.filename, "PRETO_E_BRANCO", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conexao.commit()#registrar e salvar no BD
    conexao.close()

    return send_file(caminho_modificado, mimetype='image/jpeg')#enviar imagem de volta ao cliente

@app.route('/imagens', methods=['GET'])
def listar_imagens():
    conexao = sqlite3.connect('imagens.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM imagens")
    imagens = cursor.fetchall()
    conexao.close()
    return jsonify(imagens)#Busca todas as imagens no banco de dados e retorna como JSON

if __name__ == '__main__':
    inicializar_banco()#iniciar banco
    app.run(host='0.0.0.0', port=5000)#iniciar servidor
