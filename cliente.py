import tkinter as tk
from tkinter import filedialog
import requests
from PIL import Image, ImageTk
import io

URL_SERVIDOR = "http://localhost:5000/enviar"#endereço do servidor local

#criar janela principal
janela = tk.Tk()
janela.title("Cliente - Envio de Imagem")
janela.geometry("500x500")  #definir tamanho fixo

#variáveis globais para armazenar as imagens e evitar que sejam descartadas
img_original = None
img_modificada = None

def enviar_imagem():
    global img_original, img_modificada

    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Imagem", "*.jpg *.jpeg *.png")])
    if not caminho_arquivo:
        return
    
    #exibir imagem original
    imagem_original = Image.open(caminho_arquivo)
    imagem_original.thumbnail((250, 250))#redimensiona
    img_original = ImageTk.PhotoImage(imagem_original)#converte para formato Tkinter
    rotulo_original.config(image=img_original, text="")#atualiza o rótulo com a imagem
    rotulo_original.image = img_original#mantém a referência da imagem

    with open(caminho_arquivo, 'rb') as arquivo:
        arquivos = {'arquivo': arquivo}
        resposta = requests.post(URL_SERVIDOR, files=arquivos)
    
    if resposta.status_code == 200:
        dados_imagem = resposta.content
        imagem_modificada = Image.open(io.BytesIO(dados_imagem))
        imagem_modificada.thumbnail((250, 250))#redimensiona
        img_modificada = ImageTk.PhotoImage(imagem_modificada)#converte para formato Tkinter
        
        #atualizar rótulo da imagem modificada
        rotulo_modificado.config(image=img_modificada, text="")  
        rotulo_modificado.image = img_modificada#mantém a referência

#botão para selecionar e enviar imagem
botao_enviar = tk.Button(janela, text="Selecionar e Enviar Imagem", command=enviar_imagem)
botao_enviar.pack(pady=10)

#área para exibir imagens
frame_imagens = tk.Frame(janela, bg="#d3d3d3")
frame_imagens.pack(fill="both", expand=True)

#rótulos para as imagens (inicialmente vazios)
rotulo_original = tk.Label(frame_imagens, text="Nenhuma imagem selecionada", bg="#d3d3d3")
rotulo_original.pack(side="left", padx=20)

rotulo_modificado = tk.Label(frame_imagens, text="", bg="#d3d3d3")
rotulo_modificado.pack(side="right", padx=20)

janela.mainloop()
