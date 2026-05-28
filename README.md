<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  
</head>

<body>

  <h1>🚀 Distributed AI Image Processing System</h1>

  <p>
    Sistema distribuído para processamento e classificação de imagens utilizando
    <strong>CNN (Convolutional Neural Network)</strong>, <strong>FastAPI</strong>,
    <strong>RabbitMQ</strong> e <strong>Workers assíncronos em Python</strong>,
    totalmente orquestrado com <strong>Docker Compose</strong>.
  </p>

  <hr>

  <h2>📌 Visão Geral</h2>

  <p>
    Este projeto simula uma arquitetura real de sistemas distribuídos aplicada à Inteligência Artificial.
    As imagens são enviadas via API, colocadas em uma fila no RabbitMQ e processadas por workers independentes
    que executam inferência utilizando uma rede neural convolucional (CNN).
  </p>

  <hr>

  <h2>🧠 Arquitetura do Sistema</h2>

  <ul>
    <li><strong>API (FastAPI)</strong> → Recebe requisições e publica mensagens na fila</li>
    <li><strong>RabbitMQ</strong> → Broker de mensagens assíncronas</li>
    <li><strong>Worker</strong> → Consome mensagens e executa a CNN</li>
    <li><strong>CNN Module</strong> → Modelo de deep learning responsável pela classificação</li>
  </ul>

  <h3>🔄 Fluxo de execução</h3>

  <ol>
    <li>Usuário envia imagem para a API</li>
    <li>API publica a tarefa no RabbitMQ</li>
    <li>Worker consome a mensagem</li>
    <li>CNN processa a imagem</li>
    <li>Resultado é retornado ou registrado</li>
  </ol>

  <hr>

  <h2>⚙️ Tecnologias utilizadas</h2>

  <ul>
    <li>Python 3.11</li>
    <li>FastAPI</li>
    <li>Uvicorn</li>
    <li>TensorFlow / Keras</li>
    <li>OpenCV</li>
    <li>RabbitMQ</li>
    <li>Pika</li>
    <li>Docker & Docker Compose</li>
    <li>NumPy</li>
  </ul>

  <h2>▶️ Como executar o projeto</h2>

  <h3>🔧 Pré-requisitos</h3>
  <ul>
    <li>Docker</li>
    <li>Docker Compose</li>
  </ul>

  <h3>🚀 Execução</h3>

  <pre>
docker compose up --build
  </pre>

  <hr>

  <h2>🌐 Acessos</h2>

  <ul>
    <li>API → http://localhost:8000</li>
    <li>RabbitMQ Management → http://localhost:15672</li>
    <li>Usuário: admin</li>
    <li>Senha: admin</li>
  </ul>

  <hr>

  <h2>🧪 Exemplo de requisição</h2>

  <pre>
POST /predict
Content-Type: application/json

{
  "image": "base64_string_here"
}
  </pre>

  <hr>

  <h2>⚠️ IMPORTANTE (Cluster / Workers)</h2>

  <p>
    Para que o sistema funcione corretamente como um <strong>cluster distribuído</strong>,
    é necessário executar o Docker Compose com <strong>mais de um worker ativo</strong>.
  </p>

  <p>
    Isso garante o paralelismo no consumo da fila do RabbitMQ e simula um ambiente real de escalabilidade horizontal.
  </p>

  <p>
    Exemplo recomendado:
  </p>

  <pre>
docker compose up --scale worker=3
  </pre>

  <hr>

  <h2>🧠 Conceitos aplicados</h2>

  <ul>
    <li>Sistemas Distribuídos</li>
    <li>Mensageria com RabbitMQ</li>
    <li>Arquitetura de Microservices</li>
    <li>Deep Learning com CNN</li>
    <li>Processamento de imagens</li>
    <li>Dockerização de aplicações</li>
    <li>Escalabilidade horizontal</li>
  </ul>

  <hr>

  <h2>📈 Melhorias futuras</h2>

  <ul>
    <li>Persistência em banco de dados</li>
    <li>WebSocket para retorno em tempo real</li>
    <li>Deploy em Kubernetes</li>
    <li>Monitoramento com Prometheus + Grafana</li>
    <li>Load balancing entre workers</li>
  </ul>

  <hr>

</body>
</html>
