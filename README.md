
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
    O frontend foi desenvolvido com <strong>Angular 20</strong> e <strong>Angular Material</strong>, oferecendo uma experiência rica e responsiva.
  </p>
  <div class="feature-grid">
    <div class="feature-card">
      <strong>📤 Upload de Múltiplos Arquivos</strong>
      <p>Seleção via clique ou drag-and-drop. Validação de tamanho (até 50MB por arquivo) e lista de arquivos com progresso individual.</p>
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
    <span class="tech-badge">Angular 20</span>
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
