<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Distributed AI Image Processing System</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f5f5f5; color: #333; }
    .container { max-width: 1100px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
    h2 { color: #2980b9; margin-top: 30px; }
    h3 { color: #16a085; }
    pre { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 8px; overflow-x: auto; font-family: 'Courier New', monospace; }
    code { background: #ecf0f1; padding: 2px 5px; border-radius: 4px; font-family: monospace; }
    ul, ol { margin-left: 20px; }
    hr { margin: 30px 0; border: none; height: 1px; background: #ddd; }
    .badge { display: inline-block; background: #3498db; color: white; padding: 3px 8px; border-radius: 20px; font-size: 0.8em; margin-right: 5px; }
    .feature-grid { display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0; }
    .feature-card { background: #f9f9f9; border-left: 4px solid #3498db; padding: 15px; border-radius: 8px; flex: 1 1 250px; }
    .feature-card mat-icon { font-size: 24px; color: #3498db; }
    .tech-badge { background: #e0e7ff; color: #1e3a8a; padding: 5px 12px; border-radius: 20px; display: inline-block; margin: 4px; font-size: 0.9em; }
    footer { text-align: center; margin-top: 40px; font-size: 0.9em; color: #7f8c8d; }
    @media (max-width: 600px) { .container { padding: 15px; } }
  </style>
</head>
<body>
<div class="container">

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
    que executam inferência utilizando uma rede neural convolucional (CNN). Um frontend moderno em Angular
    oferece uma interface amigável para upload de múltiplos arquivos, visualização de resultados e feedback em tempo real.
  </p>

  <hr>

  <h2>🧠 Arquitetura do Sistema</h2>
  <ul>
    <li><strong>Frontend Angular</strong> → Interface para upload de arquivos e exibição das predições</li>
    <li><strong>API (FastAPI)</strong> → Recebe requisições e publica mensagens na fila</li>
    <li><strong>RabbitMQ</strong> → Broker de mensagens assíncronas</li>
    <li><strong>Worker</strong> → Consome mensagens e executa a CNN</li>
    <li><strong>CNN Module</strong> → Modelo de deep learning responsável pela classificação</li>
  </ul>

  <h3>🔄 Fluxo de execução</h3>
  <ol>
    <li>Usuário seleciona imagens no frontend Angular (drag-and-drop ou seletor de arquivos).</li>
    <li>Frontend envia as imagens para a API (FastAPI).</li>
    <li>API publica cada tarefa no RabbitMQ.</li>
    <li>Workers consomem as mensagens da fila e processam as imagens com a CNN.</li>
    <li>Resultado (classe + confiança) é retornado à API e então para o frontend, que exibe as predições ao lado de cada arquivo.</li>
  </ol>

  <hr>

  <h2>🎨 Frontend Angular – Funcionalidades</h2>
  <p>
    O frontend foi desenvolvido com <strong>Angular 21</strong> e <strong>Angular Material</strong>, oferecendo uma experiência rica e responsiva.
  </p>
  <div class="feature-grid">
    <div class="feature-card">
      <strong>📤 Upload de Múltiplos Arquivos</strong>
      <p>Seleção via clique ou drag-and-drop. Validação de tamanho (até 50MB por arquivo) e lista de arquivos com progresso individual.</p>
    </div>
    <div class="feature-card">
      <strong>🖼️ Ícones Dinâmicos</strong>
      <p>Ícone diferente para cada tipo de arquivo (imagem, PDF, vídeo, áudio, etc.) usando <code>Material Icons</code>.</p>
    </div>
    <div class="feature-card">
      <strong>📊 Progresso & Predições</strong>
      <p>Barra de progresso para cada upload. Ao final, exibe a classe prevista e a confiança (percentual).</p>
    </div>
    <div class="feature-card">
      <strong>🌙 Tema Escuro/Claro</strong>
      <p>Alternância entre tema claro e escuro para melhor usabilidade.</p>
    </div>
    <div class="feature-card">
      <strong>⚠️ Tratamento de Erros</strong>
      <p>Feedback de erros (tamanho excedido, falhas na rede, etc.) com possibilidade de limpar avisos.</p>
    </div>
    <div class="feature-card">
      <strong>🧹 Limpeza de Lista</strong>
      <p>Botão "Limpar" remove todos os arquivos da fila e cancela uploads em andamento.</p>
    </div>
  </div>

  <h3>🔧 Tecnologias do Frontend</h3>
  <div>
    <span class="tech-badge">Angular 21</span>
    <span class="tech-badge">Angular Material</span>
    <span class="tech-badge">RxJS</span>
    <span class="tech-badge">TypeScript</span>
    <span class="tech-badge">SCSS</span>
    <span class="tech-badge">HTTP Client</span>
  </div>

  <h3>📡 Comunicação com a API</h3>
  <p>
    O frontend utiliza o serviço <code>FileService</code> para enviar arquivos via <code>multipart/form-data</code> para o endpoint <code>/predict</code> da API FastAPI.
    O progresso do upload é monitorado com <code>HttpEventType.UploadProgress</code>. As respostas contêm as predições de cada imagem e são exibidas em tempo real.
  </p>

  <hr>

  <h2>⚙️ Tecnologias utilizadas (Backend e Infra)</h2>
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

  <hr>

  <h2>▶️ Como executar o projeto</h2>
  <h3>🔧 Pré-requisitos</h3>
  <ul>
    <li>Docker</li>
    <li>Docker Compose</li>
  </ul>

  <h3>🚀 Execução básica</h3>
  <pre>docker compose up --build</pre>

  <h3>⚠️ IMPORTANTE (Cluster / Workers)</h3>
  <p>
    Para que o sistema funcione corretamente como um <strong>cluster distribuído</strong>,
    é necessário executar o Docker Compose com <strong>mais de um worker ativo</strong>.
    Isso garante o paralelismo no consumo da fila do RabbitMQ e simula um ambiente real de escalabilidade horizontal.
  </p>
  <p>Exemplo recomendado:</p>
  <pre>docker compose up --scale worker=3</pre>

  <hr>

  <h2>🌐 Acessos</h2>
  <ul>
    <li>Frontend Angular → <a href="http://localhost:4200">http://localhost:4200</a></li>
    <li>API FastAPI → <a href="http://localhost:8000">http://localhost:8000</a></li>
    <li>RabbitMQ Management → <a href="http://localhost:15672">http://localhost:15672</a> (usuário: <code>admin</code>, senha: <code>admin</code>)</li>
  </ul>

  <hr>

  <h2>🧪 Exemplo de requisição direta à API (sem frontend)</h2>
  <pre>
POST /predict
Content-Type: application/json

{
  "image": "base64_string_here"
}
  </pre>

  <hr>

  <h2>🧠 Conceitos aplicados</h2>
  <ul>
    <li>Sistemas Distribuídos</li>
    <li>Mensageria com RabbitMQ</li>
    <li>Arquitetura de Microsserviços</li>
    <li>Deep Learning com CNN</li>
    <li>Processamento de imagens</li>
    <li>Dockerização de aplicações (frontend + backend + message broker)</li>
    <li>Escalabilidade horizontal</li>
    <li>Frontend moderno com Angular e Material Design</li>
  </ul>

  <hr>

  <h2>📈 Melhorias futuras</h2>
  <ul>
    <li>Persistência dos resultados em banco de dados (PostgreSQL/MongoDB)</li>
    <li>WebSocket para retorno em tempo real das predições</li>
    <li>Deploy em Kubernetes</li>
    <li>Monitoramento com Prometheus + Grafana</li>
    <li>Load balancing mais avançado entre workers</li>
    <li>Autenticação e autorização de usuários</li>
  </ul>

  <hr>
  <footer>
    Projeto desenvolvido como simulação de um sistema distribuído de IA. Código disponível em repositório público.
  </footer>
</div>
</body>
</html>
