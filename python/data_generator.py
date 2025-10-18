# #################################################################
# # ARQUIVO: python/gerador_dados.py
# # OBJETIVO: Gera dados fictícios para 9 tabelas, exporta para CSV e um script SQL de INSERT.
# #################################################################

import csv
import random
from datetime import datetime, timedelta

# Instalação necessária: pip install faker
from faker import Faker

# Configuração do Faker para gerar dados em português do Brasil
fake = Faker('pt_BR')

# --- CONFIGURAÇÕES DE VOLUME DE DADOS ---
NUM_ALUNOS = 30
NUM_INSTRUTORES = 10
NUM_CURSOS = 20
NUM_MATRICULAS = 80  # Relação M:N
NUM_MODULOS_POR_CURSO = 5
NUM_AULAS_POR_MODULO = 4
NUM_AVALIACOES = 70


# --- ESTRUTURAS DE DADOS GLOBAIS (Listas que armazenarão os dicionários) ---
LISTA_ALUNOS = []
LISTA_INSTRUTORES = []
LISTA_CATEGORIAS = []
LISTA_CURSOS = []
LISTA_MODULOS = []
LISTA_AULAS = []
LISTA_MATRICULAS = []
LISTA_PROGRESSO_AULAS = []
LISTA_AVALIACOES = []


# --- VARIÁVEIS AUXILIARES (Para garantir a integridade dos dados) ---
IDS_CATEGORIAS = []
IDS_INSTRUTORES = []
IDS_CURSOS = []
IDS_MATRICULAS = []
EMAIL_UNICOS = set()
MATRICULAS_UNICAS = set()  # Para garantir UNIQUE (aluno_id, curso_id)

# Níveis e Status para cumprir as restrições CHECK do SQL
NIVEIS = ['iniciante', 'intermediario', 'avancado']
STATUS_MATRICULA = ['ativa', 'concluida', 'cancelada']
TIPOS_AULA = ['video', 'texto', 'quiz']


# =================================================================
# FUNÇÕES DE EXPORTAÇÃO
# =================================================================

def exportar_para_csv(nome_arquivo, dados):
    """Exporta uma lista de dicionários para um arquivo CSV na pasta 'data/'."""
    if not dados:
        return

    # O CSV não aceita valores 'NULL' como string. Ele precisa que a célula seja vazia.
    # Faz uma cópia e substitui 'NULL' por ''
    dados_formatados = [{k: ('' if v == 'NULL' else v) for k, v in d.items()} for d in dados]
    
    caminho_completo = f'data/{nome_arquivo}.csv'
    
    try:
        with open(caminho_completo, 'w', newline='', encoding='utf-8') as f:
            nomes_colunas = dados_formatados[0].keys()
            writer = csv.DictWriter(f, fieldnames=nomes_colunas)
            
            writer.writeheader()
            writer.writerows(dados_formatados)
            
        print(f"-> CSV gerado: {caminho_completo}")
    except Exception as e:
        print(f"ERRO ao gerar CSV {caminho_completo}: {e}")

def exportar_para_sql(tabela, dados, arquivo_saida):
    """Gera comandos INSERT INTO e salva no arquivo SQL."""
    if not dados:
        return ""

    campos = ", ".join(dados[0].keys())
    
    comandos_insert = []
    for registro in dados:
        valores = []
        for v in registro.values():
            if v == 'NULL':
                valores.append('NULL')
            elif isinstance(v, (str, datetime)):
                # Adiciona aspas simples e escapa as aspas simples internas
                valores.append(f"'{str(v).replace("'", "''")}'")
            else:
                valores.append(str(v))
        
        valores_str = ", ".join(valores)
        comandos_insert.append(f"INSERT INTO {tabela} ({campos}) VALUES ({valores_str});")

    # Salva no arquivo final
    with open(arquivo_saida, 'a', encoding='utf-8') as f:
        f.write(f"\n-- INSERTS PARA A TABELA: {tabela.upper()}\n")
        f.write("\n".join(comandos_insert) + "\n")


# =================================================================
# FUNÇÕES DE GERAÇÃO DE DADOS POR TABELA
# =================================================================

def garantir_email_unico(nome):
    """Gera um email único e garante que não haja duplicidade."""
    while True:
        email = f"{nome.lower().replace(' ', '.').split('.')[0]}{random.randint(1, 99)}@{fake.domain_name()}"
        if email not in EMAIL_UNICOS:
            EMAIL_UNICOS.add(email)
            return email

def gerar_alunos():
    print("Gerando Alunos...")
    for i in range(1, NUM_ALUNOS + 1):
        nome = fake.name()
        
        LISTA_ALUNOS.append({
            'id': i,
            'nome': nome,
            'email': garantir_email_unico(nome),
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=60),
            'data_cadastro': fake.date_time_between(start_date='-5y', end_date='-1y')
        })

def gerar_instrutores():
    print("Gerando Instrutores...")
    for i in range(1, NUM_INSTRUTORES + 1):
        nome = fake.name()
        
        instrutor = {
            'id': i,
            'nome': nome,
            'email': garantir_email_unico(nome),
            'especialidade': fake.job(),
            'biografia': fake.paragraph(nb_sentences=3)
        }
        LISTA_INSTRUTORES.append(instrutor)
        IDS_INSTRUTORES.append(i) # Armazena ID para FK
        
def gerar_categorias():
    print("Gerando Categorias...")
    nomes_categorias = ['Programação', 'Design UX/UI', 'Marketing Digital', 
                        'Data Science', 'Finanças', 'Idiomas']
    
    for i, nome in enumerate(nomes_categorias, 1):
        LISTA_CATEGORIAS.append({
            'id': i,
            'nome': nome,
            'descricao': fake.sentence(nb_words=10)
        })
        IDS_CATEGORIAS.append(i) # Armazena ID para FK
        
def gerar_cursos():
    print("Gerando Cursos...")
    for i in range(1, NUM_CURSOS + 1):
        # Seleciona FKs aleatoriamente
        instrutor_id = random.choice(IDS_INSTRUTORES)
        categoria_id = random.choice(IDS_CATEGORIAS)
        
        LISTA_CURSOS.append({
            'id': i,
            'titulo': f"{random.choice(['Introdução', 'Avançado', 'Dominando'])} ao {fake.bs()}",
            'descricao': fake.text(max_nb_chars=200),
            'categoria_id': categoria_id,
            'instrutor_id': instrutor_id,
            'preco': round(random.uniform(29.90, 499.90), 2),
            'carga_horaria': random.randint(5, 80),
            'nivel': random.choice(NIVEIS),
            'data_criacao': fake.date_time_between(start_date='-2y', end_date='now')
        })
        IDS_CURSOS.append(i) # Armazena ID para FK

def gerar_modulos_aulas():
    print("Gerando Módulos e Aulas...")
    modulo_id = 1
    aula_id = 1

    for curso_id in IDS_CURSOS:
        # Cria Módulos para o Curso
        for ordem_mod in range(1, NUM_MODULOS_POR_CURSO + 1):
            
            LISTA_MODULOS.append({
                'id': modulo_id,
                'curso_id': curso_id,
                'titulo': f"Módulo {ordem_mod}: {fake.catch_phrase()}",
                'ordem': ordem_mod,
                'descricao': fake.sentence(nb_words=8)
            })

            # Cria Aulas para o Módulo
            for ordem_aula in range(1, NUM_AULAS_POR_MODULO + 1):
                
                aula = {
                    'id': aula_id,
                    'modulo_id': modulo_id,
                    'titulo': f"Aula {ordem_aula}: {fake.text(max_nb_chars=50)}",
                    'ordem': ordem_aula,
                    'duracao_minutos': random.randint(5, 45),
                    'tipo': random.choice(TIPOS_AULA)
                }
                LISTA_AULAS.append(aula)
                aula_id += 1
            
            modulo_id += 1


def gerar_matriculas():
    print("Gerando Matrículas...")
    global IDS_MATRICULAS
    
    # Lista de todos os alunos e cursos disponíveis
    ids_alunos_disponiveis = [a['id'] for a in LISTA_ALUNOS]
    
    for i in range(1, NUM_MATRICULAS + 1):
        aluno_id = random.choice(ids_alunos_disponiveis)
        curso_id = random.choice(IDS_CURSOS)
        
        # Garante a restrição UNIQUE (aluno_id, curso_id)
        if (aluno_id, curso_id) in MATRICULAS_UNICAS:
            continue

        MATRICULAS_UNICAS.add((aluno_id, curso_id))
        
        # Define status e datas
        status = random.choice(STATUS_MATRICULA)
        data_matricula = fake.date_time_between(start_date='-1y', end_date='-30d')
        
        data_conclusao = 'NULL'
        if status == 'concluida':
            data_conclusao = data_matricula + timedelta(days=random.randint(30, 180))
        
        # Busca o preço real do curso
        preco_curso = [c['preco'] for c in LISTA_CURSOS if c['id'] == curso_id][0]

        matricula = {
            'id': i,
            'aluno_id': aluno_id,
            'curso_id': curso_id,
            'data_matricula': data_matricula,
            'data_conclusao': data_conclusao,
            'status': status,
            'valor_pago': preco_curso # Valor pago é o preço do curso (simples)
        }
        LISTA_MATRICULAS.append(matricula)
        IDS_MATRICULAS.append(i) # Armazena ID para FK

def gerar_progresso_e_avaliacoes():
    print("Gerando Progresso de Aulas e Avaliações...")
    progresso_id = 1
    avaliacao_id = 1
    
    for matricula in LISTA_MATRICULAS:
        matricula_id = matricula['id']
        curso_id = matricula['curso_id']
        status = matricula['status']
        
        # 1. PROGRESSO DE AULAS
        # Pega todas as aulas do curso desta matrícula
        aulas_do_curso = [a for a in LISTA_AULAS if a['modulo_id'] in [m['id'] for m in LISTA_MODULOS if m['curso_id'] == curso_id]]
        
        # Determina o percentual de conclusão baseado no status
        percentual_conclusao = 0
        if status == 'concluida':
            percentual_conclusao = 1.0
        elif status == 'ativa':
            percentual_conclusao = random.uniform(0.1, 0.9) # Incompleto
        else: # cancelada
            percentual_conclusao = random.uniform(0.0, 0.1) # Quase nada

        num_aulas_concluir = int(len(aulas_do_curso) * percentual_conclusao)

        for aula in aulas_do_curso:
            concluida = (random.random() < percentual_conclusao)
            
            tempo_assistido = 0
            data_conc = 'NULL'
            
            if concluida:
                tempo_assistido = aula['duracao_minutos']
                data_conc = matricula['data_matricula'] + timedelta(days=random.randint(1, 100))
            
            LISTA_PROGRESSO_AULAS.append({
                'id': progresso_id,
                'matricula_id': matricula_id,
                'aula_id': aula['id'],
                'concluida': concluida,
                'data_conclusao': data_conc,
                'tempo_assistido_minutos': tempo_assistido
            })
            progresso_id += 1

        # 2. AVALIAÇÕES (Apenas para matrículas ativas ou concluídas)
        if status != 'cancelada' and random.random() < 0.8: # 80% de chance de avaliar
            
            # Garante que um aluno só avalia o curso uma vez (restrição UNIQUE em avaliacoes.matricula_id)
            LISTA_AVALIACOES.append({
                'id': avaliacao_id,
                'matricula_id': matricula_id,
                'curso_id': curso_id,
                'nota': random.randint(1, 5),
                'comentario': fake.sentence(nb_words=15) if random.random() > 0.3 else 'NULL',
                'data_avaliacao': matricula['data_matricula'] + timedelta(days=random.randint(10, 200))
            })
            avaliacao_id += 1


# =================================================================
# EXECUÇÃO PRINCIPAL
# =================================================================

if __name__ == "__main__":
    
    # 1. Limpa o arquivo de saída SQL para um novo start
    with open('sql/dados.sql', 'w') as f:
        f.write("-- ARQUIVO GERADO AUTOMATICAMENTE PELO gerador_dados.py\n")
        f.write("BEGIN TRANSACTION;\n\n")

    # 2. Geração dos dados em cascata (Dependências de FK)
    print("--- INICIANDO GERAÇÃO DE DADOS FICTÍCIOS ---")
    gerar_alunos()
    gerar_instrutores()
    gerar_categorias()
    gerar_cursos()
    gerar_modulos_aulas()
    gerar_matriculas()
    gerar_progresso_e_avaliacoes()
    print("--- GERAÇÃO CONCLUÍDA ---")

    # 3. Exportação para CSV (Requisito de entrega)
    print("\n--- EXPORTANDO PARA CSV ---")
    exportar_para_csv('alunos', LISTA_ALUNOS)
    exportar_para_csv('instrutores', LISTA_INSTRUTORES)
    exportar_para_csv('categorias', LISTA_CATEGORIAS)
    exportar_para_csv('cursos', LISTA_CURSOS)
    exportar_para_csv('modulos', LISTA_MODULOS)
    exportar_para_csv('aulas', LISTA_AULAS)
    exportar_para_csv('matriculas', LISTA_MATRICULAS)
    exportar_para_csv('progresso_aulas', LISTA_PROGRESSO_AULAS)
    exportar_para_csv('avaliacoes', LISTA_AVALIACOES)

    # 4. Exportação para SQL (Para injeção no PostgreSQL)
    print("\n--- EXPORTANDO PARA SQL ---")
    exportar_para_sql('alunos', LISTA_ALUNOS, 'sql/dados.sql')
    exportar_para_sql('instrutores', LISTA_INSTRUTORES, 'sql/dados.sql')
    exportar_para_sql('categorias', LISTA_CATEGORIAS, 'sql/dados.sql')
    exportar_para_sql('cursos', LISTA_CURSOS, 'sql/dados.sql')
    exportar_para_sql('modulos', LISTA_MODULOS, 'sql/dados.sql')
    exportar_para_sql('aulas', LISTA_AULAS, 'sql/dados.sql')
    exportar_para_sql('matriculas', LISTA_MATRICULAS, 'sql/dados.sql')
    exportar_para_sql('progresso_aulas', LISTA_PROGRESSO_AULAS, 'sql/dados.sql')
    exportar_para_sql('avaliacoes', LISTA_AVALIACOES, 'sql/dados.sql')
    
    # Finaliza o script SQL
    with open('sql/dados.sql', 'a') as f:
        f.write("\nCOMMIT;\n")

    print("-> SQL de dados gerado: sql/dados.sql")
    print("\n✅ Script de geração de dados concluído com sucesso!")
