Projeto Pedra Pagamentos

Este projeto tem como objetivo processar e gerenciar atendimentos e lotes processados utilizando Airflow, PostgreSQL e SQLAlchemy. 
Ele permite a automação de tarefas relacionadas ao processamento de dados, armazenamento de informações relevantes e geração de Gráficos.

📌 Tecnologias Utilizadas

Apache Airflow: Orquestração de workflows

PostgreSQL: Banco de dados relacional

SQLAlchemy: ORM para interação com o banco

Docker & Docker Compose: Gerenciamento de containers

🚀 Como Executar o Projeto

1️⃣ Pré-requisitos

Certifique-se de ter instalado:

Docker

Docker Compose

Python versão 3.9 ou Superior

2️⃣ Clonando o Repositório

    git clone https://github.com/FilipeDeberge/pedra_pagamentos_pipeline.git
    cd pedra_pagamentos_pipeline

3️⃣ Subindo os Containers

Para criar a imagem com as especificações do DockerFile:
    docker-compose build --no-cache

Para subir os containers com suas respectivas definições
    docker-compose up -d --build

Isso irá iniciar os serviços do PostgreSQL e do Airflow.

4️⃣ Acessando o Airflow

Após a execução, acesse o Airflow pelo navegador:

http://localhost:8080

Credenciais padrão:

Usuário: admin

Senha: admin

5️⃣ Criação o Banco e as Tabelas

Se o banco de dados e as tabelas não existirem, eles serão criados automaticamente pelo entrypoint, que roda quando os containers são carregados.


📜 Estrutura do Projeto

![image](https://github.com/user-attachments/assets/44bcdd21-aaba-4ca5-8c65-af8caabeed2d)


✅ Próximos Passos

Configurar mais DAGs no Airflow para processamento automatizado

Implementar novos endpoints para interagir com os dados

Melhorar a gestão de logs e monitoramento

Caso tenha dúvidas, consulte a documentação ou entre em contato! 🚀

