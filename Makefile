# #################################################################
# # ARQUIVO: Makefile
# # OBJETIVO: Automatizar a infraestrutura e execução do projeto Joyce EduTech.
# #################################################################

# Variáveis
DB_NAME := joyce_edutech
DB_USER := $(USER)  # Pega o usuário do seu sistema (mvrga no seu caso)
SCHEMA_FILE := sql/schema.sql
DADOS_FILE := sql/dados.sql
PYTHON_GENERATOR := python/gerador_dados.py
PYTHON_TESTER := python/consultas_python.py

# =================================================================
# REGRAS DE EXECUÇÃO PRINCIPAIS
# =================================================================

# make setup: Instala dependências Python necessárias
setup:
	@echo "--- 1/3: Instalando dependências Python (faker, psycopg2) ---"
	python3 -m pip install faker psycopg2-binary
	@echo "--- Dependências instaladas com sucesso. ---"

# make clean: Limpa o banco de dados (DROP SCHEMA PUBLIC)
clean:
	@echo "--- Limpando banco de dados $(DB_NAME) ---"
	psql -d $(DB_NAME) -c "DROP SCHEMA public CASCADE;" || true # O '|| true' evita erro se o schema não existir
	psql -d $(DB_NAME) -c "CREATE SCHEMA public;"
	@echo "--- Banco de dados limpo. ---"

# make schema: Cria as tabelas do zero
schema: clean
	@echo "--- 2/3: Criando Schema (9 Tabelas) em $(DB_NAME) ---"
	psql -d $(DB_NAME) -f $(SCHEMA_FILE)
	@echo "--- Schema criado com sucesso. ---"

# make data: Gera dados fictícios e insere no banco
data: schema
	@echo "--- 3/3: Gerando dados e inserindo no banco (via Python) ---"
	python3 $(PYTHON_GENERATOR)
	psql -d $(DB_NAME) -f $(DADOS_FILE)
	@echo "--- Dados inseridos com sucesso. ---"

# make test: Roda as consultas SQL e exibe o resultado (via Python)
test: data
	@echo "--- EXECUTANDO TESTE DAS 12 CONSULTAS SQL VIA PYTHON ---"
	python3 $(PYTHON_TESTER)

# make all (Comando principal para subir o ambiente completo)
all: setup test
	@echo ""
	@echo "=========================================================="
	@echo "✅ AMBIENTE JOYCE EDUTECH PRONTO E TESTADO."
	@echo "=========================================================="

.PHONY: setup clean schema data test alls