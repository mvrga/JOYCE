# #################################################################
# # ARQUIVO: python/normalization_checker.py
# # OBJETIVO: Verificar se o schema.sql contém as chaves e dependências
# #           necessárias para atender às 3 Formas Normais (3FN).
# #################################################################

import re

# Regras de 3FN: O que o script procura no schema.sql
REGRAS_3FN = {
    # Tabela Cursos: Deve depender apenas da PK (curso.id). A categoria e instrutor
    # são atributos de OUTRAS tabelas, por isso precisam de FKs.
    'cursos': [
        (r'categoria_id\s+INTEGER\s+NOT\s+NULL\s+REFERENCES\s+categorias', 'FK_CATEGORIA'),
        (r'instrutor_id\s+INTEGER\s+NOT\s+NULL\s+REFERENCES\s+instrutores', 'FK_INSTRUTOR')
    ],
    # Tabela Matriculas: Tabela M:N, precisa de 2 FKs e uma restrição UNIQUE
    'matriculas': [
        (r'aluno_id\s+INTEGER\s+NOT\s+NULL\s+REFERENCES\s+alunos', 'FK_ALUNO'),
        (r'curso_id\s+INTEGER\s+NOT\s+NULL\s+REFERENCES\s+cursos', 'FK_CURSO'),
        (r'UNIQUE\s+\(aluno_id,\s*curso_id\)', 'RESTRICAO_UNICA_MN')
    ],
    # Tabela Progresso_Aulas: Tabela dependente, precisa de FKs para Matrículas e Aulas, e uma restrição UNIQUE.
    'progresso_aulas': [
        (r'matricula_id\s+INTEGER\s+NOT\s+NULL\s+REFERENCES\s+matriculas', 'FK_MATRICULA'),
        (r'aula_id\s+INTEGER\s+NOT\s+NULL\s+REFERENCES\s+aulas', 'FK_AULA'),
        (r'UNIQUE\s+\(matricula_id,\s*aula_id\)', 'RESTRICAO_UNICA_PROGRESSO')
    ],
    # Tabela Avaliacoes: Deve ter uma FK UNIQUE para Matrículas (relação 1:1)
    'avaliacoes': [
        (r'matricula_id\s+INTEGER\s+UNIQUE\s+NOT\s+NULL\s+REFERENCES\s+matriculas', 'FK_MATRICULA_UNICA')
    ]
}

def verificar_normalizacao(schema_file):
    """Lê o schema SQL e verifica a presença das regras de 3FN em tabelas críticas."""
    print(f"\n--- INICIANDO VERIFICADOR DE NORMALIZAÇÃO (3FN) em {schema_file} ---")
    try:
        with open(schema_file, 'r') as f:
            schema_content = f.read()
    except FileNotFoundError:
        print("ERRO: Arquivo sql/schema.sql não encontrado.")
        return False

    passou_geral = True
    
    # Processa o conteúdo para facilitar a busca por tabelas
    schema_content_limpo = schema_content.replace('\n', ' ').replace('(', ' (').lower()

    for tabela, regras in REGRAS_3FN.items():
        print(f"\n-> Verificando Tabela: {tabela.upper()}")
        tabela_passou = True
        
        # Encontra o bloco de criação da tabela
        bloco_tabela_match = re.search(f'create table {tabela} \s*\((.*?)\);', schema_content_limpo)
        
        if not bloco_tabela_match:
            print(f"  [AVISO] Tabela {tabela.upper()} não encontrada no schema.")
            continue
            
        bloco_tabela = bloco_tabela_match.group(1)

        for regex_pattern, regra_nome in regras:
            if re.search(regex_pattern.lower(), bloco_tabela):
                print(f"  ✅ [PASSOU] Regra {regra_nome} encontrada.")
            else:
                print(f"  ❌ [FALHOU] Regra {regra_nome} (3FN) não encontrada! Reveja a dependência de chaves.")
                tabela_passou = False
                passou_geral = False

        if tabela_passou:
            print(f"  ✅ Tabela {tabela.upper()} confirmada como 3FN (com base nas regras de FKs).")

    if passou_geral:
        print("\n*** ✅ SUCESSO! SEU SCHEMA PASSA NAS VERIFICAÇÕES DE 3FN. ***")
    else:
        print("\n*** ❌ FALHA! REGRAS DE NORMALIZAÇÃO PENDENTES. REVEJA O SCHEMA. ***")
    
    return passou_geral

if __name__ == "__main__":
    verificar_normalizacao('../sql/schema.sql')