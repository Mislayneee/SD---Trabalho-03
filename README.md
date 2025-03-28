# Descrição do Projeto

Este projeto consiste em um sistema cliente-servidor para processamento de imagens, desenvolvido em Python utilizando Flask, SQLite e Pillow. O cliente permite que o usuário selecione uma imagem e a envie para o servidor, que processa a imagem aplicando um filtro e a retorna ao cliente. Além disso, os metadados das imagens (nome do arquivo, filtro aplicado e data/hora do processamento) são armazenados em um banco de dados SQLite.

O servidor recebe a imagem via HTTP, salva a versão original na pasta `imagens_enviadas` e aplica o filtro de conversão para preto e branco. Após o processamento, a imagem modificada é armazenada no servidor e enviada de volta ao cliente. O cliente, por sua vez, exibe tanto a imagem original quanto a processada em sua interface gráfica.

## Como Executar o Projeto

Para rodar o sistema, primeiro é necessário iniciar o servidor executando o arquivo `servidor.py` no terminal com o comando:

```bash
python servidor.py
```

O servidor ficará em execução na porta 5000, aguardando conexões do cliente. Em seguida, em outro terminal, o cliente pode ser iniciado com o comando:

```bash
python cliente.py
```

Uma interface gráfica será aberta para a seleção de imagens. Após escolher uma imagem, o usuário verá a imagem original e a versão processada na interface. Os arquivos gerados podem ser conferidos na pasta do projeto e no banco de dados SQLite.

# SD---Trabalho-03
