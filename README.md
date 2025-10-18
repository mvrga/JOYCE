# JOYCE
J . O . Y . C . E - Edutech for peoples : A plataform for Education community M1 Project.
Projeto ICCD- Instituto Consuelo Casa Digital Full Stack

📚 Projeto JOYCE: Plataforma Educacional (EduTech)
Visão Geral
O projeto JOYCE consiste na modelagem e implementação de um sistema de banco de dados relacional para uma plataforma de educação online (EduTech). O foco é demonstrar proficiência em:

Modelagem de dados (Diagrama ER e Terceira Forma Normal - 3FN).

Implementação de infraestrutura automatizada (PostgreSQL, Python e Makefile).

Elaboração de consultas SQL complexas para relatórios de negócio.

🚀 Funcionalidades Principais
Requisito,Detalhamento da Solução,Status
Modelagem do Banco de Dados,"Sistema modelado com 9 tabelas (Alunos, Instrutores, Cursos, etc.) em Terceira Forma Normal (3FN), garantindo integridade referencial.",✅ Concluído
Consultas de Negócio,"12 consultas SQL avançadas para geração de relatórios (ex: ranking de cursos, percentual de progresso do aluno, arrecadação total por curso).",✅ Concluído
Geração de Dados Fictícios,"Script Python para gerar dados realistas e complexos, simulando 30 alunos, 20 cursos e 80 matrículas.",✅ Concluído
Organização do Projeto,"Utilização de Makefile para automatizar a criação, limpeza e teste do ambiente.",✅ Concluído

🛠️ Tecnologias e Dependências
Para rodar este projeto, as seguintes ferramentas são necessárias:

Tecnologia,Finalidade
PostgreSQL,Servidor de Banco de Dados.
Python 3,Geração de dados e execução de testes de conexão.
GNU Make,Automatização de tarefas de infraestrutura.
faker (Python),Biblioteca para geração de dados fictícios em português.
psycopg2-binary (Python),Conector Python para PostgreSQL.

⚙️ Setup e Execução (Automação)
A maneira mais rápida e eficiente de subir o ambiente é usando o Makefile.

1. Instalação (Primeira Vez)

Instale as dependências Python necessárias para a geração de dados e conexão com o banco:

Bash
# Executado por make setup, mas listado para clareza:
python3 -m pip install faker psycopg2-binary


2. Comando Mágico: make all

Este comando executa a sequência completa de passos:

Limpa o banco de dados joyce_edutech.

Cria as 9 tabelas (sql/schema.sql).

Gera os dados fictícios (python/gerador_dados.py).

Insere os dados (sql/dados.sql).

Testa a execução das 12 consultas (python/consultas_python.py).

Bash
make all
Comandos Úteis

Comando	Descrição
make clean	Apaga todas as tabelas do banco de dados (Reset total).
make data	Cria as tabelas e insere os dados (Ideal para recarregar).
make test	Roda as 12 consultas SQL via Python e exibe os resultados.

🔬 Testes e Provas de Qualidade
A qualidade do projeto é verificada através de scripts de teste automatizados:

1. Prova da Terceira Forma Normal (3FN)

O script python/normalization_checker.py testa o schema.sql para garantir que as tabelas críticas (cursos, matriculas, avaliacoes) contenham as chaves estrangeiras (FK) e restrições UNIQUE necessárias para atender à 3FN.

Execução: python/normalization_checker.py

2. Prova das Consultas SQL

O script python/consultas_python.py demonstra o domínio sobre a conexão entre Python e PostgreSQL, executando as 12 consultas SQL e exibindo os resultados diretamente no terminal.

Execução: python/consultas_python.py (Este script é invocado pelo make test).

📁 Estrutura do Projeto
O projeto segue a seguinte organização de diretórios:

JOYCE/
├── data/              # Saída: 9 arquivos .csv gerados pelo Python.
├── docs/              # Documentação: Diagrama ER (diagrama_er.png).
├── python/            # Scripts de lógica (geração de dados e testes).
├── sql/               # Scripts SQL (schema, dados e consultas).
├── Makefile           # Automação e Infraestrutura.
└── README.md          # Este arquivo.

