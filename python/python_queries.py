import psycopg2
from psycopg2 import sql

# 1. CONFIGURAÇÃO DA CONEXÃO
# Como você está usando o Homebrew/psql local, as credenciais padrão são:
DB_NAME = "joyce_edutech"
DB_USER = "mvrga" 
DB_HOST = "localhost"

def conectar_bd():
    """Conecta ao PostgreSQL e retorna o objeto de conexão."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            host=DB_HOST
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def executar_consultas_e_mostrar(conn, arquivo_consultas):
    """Lê um arquivo .sql contendo múltiplas consultas e as executa, mostrando o resultado."""
    if not conn:
        return

    # 1. Lê o arquivo SQL completo
    try:
        with open(arquivo_consultas, 'r', encoding='utf-8') as f:
            # Divide o arquivo em consultas individuais usando ';' como delimitador
            # (Garante que a última parte vazia seja removida)
            consultas_sql = [c.strip() for c in f.read().split(';') if c.strip()]
    except FileNotFoundError:
        print(f"\nERRO: Arquivo {arquivo_consultas} não encontrado.")
        return

    # 2. Executa e Imprime
    with conn.cursor() as cur:
        for i, consulta in enumerate(consultas_sql, 1):
            if not consulta.upper().startswith('SELECT'):
                # Ignora comentários e comandos que não são SELECT (embora o arquivo só deva ter SELECTs)
                continue
                
            print("-" * 50)
            print(f"[{i:02d}/12] EXECUTANDO: {consulta.splitlines()[0][:60]}...")
            
            try:
                cur.execute(consulta)
                
                # 3. Formata e Imprime os Resultados
                colunas = [desc[0] for desc in cur.description]
                resultados = cur.fetchall()

                if resultados:
                    print(f"  Encontrados {len(resultados)} resultados.")
                    
                    # Imprime o cabeçalho
                    header = " | ".join(colunas)
                    print("  " + header)
                    print("  " + "-" * len(header))
                    
                    # Imprime as primeiras 5 linhas para demonstração
                    for linha in resultados[:5]:
                        # Converte a tupla em string para exibição
                        print("  " + " | ".join(map(str, linha)))
                else:
                    print("  Nenhum resultado encontrado (Tabela Vazia ou Filtro Restritivo).")
                    
            except psycopg2.ProgrammingError as e:
                print(f"  ERRO de SQL na consulta {i}: {e}")

    conn.close()

if __name__ == "__main__":
    print(f"*** INICIANDO TESTE DE CONSULTAS SQL VIA PYTHON ({DB_USER}@{DB_HOST}) ***")
    
    # 1. Certifique-se de que o schema e dados estão carregados
    # ESTES COMANDOS DEVEM TER SIDO EXECUTADOS ANTES:
    # psql -d joyce_edutech -f [caminho]/sql/schema.sql
    # python python/gerador_dados.py
    # psql -d joyce_edutech -f sql/dados.sql
    
    conn = conectar_bd()
    if conn:
        executar_consultas_e_mostrar(conn, 'sql/consultas.sql')
        print("-" * 50)
        print("✅ Execução de todas as consultas finalizada e resultados exibidos.")