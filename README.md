🚀 Distributed AI Image Processing System

Sistema distribuído para processamento e classificação de imagens utilizando CNN (Convolutional Neural Network), FastAPI, RabbitMQ e Workers assíncronos em Python, orquestrado via Docker Compose.

📌 Visão Geral

Este projeto simula uma arquitetura moderna de sistemas distribuídos aplicada a IA.
As imagens são enviadas via API, enfileiradas no RabbitMQ e processadas por workers especializados que executam inferência usando uma rede neural convolucional (CNN).

🧠 Arquitetura

O sistema é dividido em três principais componentes:

API (FastAPI) → Recebe requisições e envia tarefas para a fila
RabbitMQ → Broker de mensagens para comunicação assíncrona
Worker (Python) → Consome mensagens e executa a CNN
CNN Module → Modelo de deep learning responsável pela classificação
🔄 Fluxo do sistema
Usuário envia imagem para a API
API publica mensagem no RabbitMQ
Worker consome a fila
CNN processa a imagem
Resultado é retornado/logado
🧱 Tecnologias utilizadas
Python 3.11
FastAPI
Uvicorn
TensorFlow / Keras
OpenCV
RabbitMQ
Pika
Docker & Docker Compose
NumPy

⚙️ Como executar o projeto
🔧 Pré-requisitos
Docker
Docker Compose
▶️ Executando

No diretório raiz do projeto:

docker compose up --build
🌐 Acessos
API: http://localhost:8000
RabbitMQ Panel: http://localhost:15672
usuário: admin
senha: admin
🧪 Exemplo de uso

Exemplo de requisição para a API:

POST /predict
Content-Type: application/json

{
  "image": "base64_string_here"
}
🧠 Conceitos aplicados
Sistemas Distribuídos
Mensageria assíncrona (RabbitMQ)
Microservices
Deep Learning com CNN
Processamento de imagens
Containerização com Docker
Arquitetura escalável
📈 Possíveis melhorias
