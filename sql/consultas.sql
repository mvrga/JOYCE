-- #################################################################
-- # ARQUIVO: sql/consultas.sql
-- # AUTOR: [SEU NOME AQUI]
-- # OBJETIVO: 12 Consultas SQL Requeridas, otimizadas para clareza e defesa de código.
-- #################################################################


-- 1. [REQUISITO BÁSICO: LISTAGEM]
-- OBJETIVO: Listar todos os cursos, exibindo o título, o nome da categoria e o nome do instrutor responsável.
-- TÉCNICA: Uso de JOINs múltiplos para conectar a tabela central (Cursos) às tabelas de dimensão (Categorias e Instrutores).

SELECT 
    curso.titulo AS titulo_do_curso,
    categoria.nome AS nome_da_categoria,
    instrutor.nome AS nome_do_instrutor,
    curso.preco
FROM 
    cursos AS curso
JOIN 
    categorias AS categoria ON curso.categoria_id = categoria.id
JOIN 
    instrutores AS instrutor ON curso.instrutor_id = instrutor.id
ORDER BY 
    curso.titulo;


-- 2. [REQUISITO BÁSICO: FILTRO POR ALUNO]
-- OBJETIVO: Listar todos os alunos que estão matriculados em um curso específico (usaremos o Curso de ID = 1 como exemplo).
-- TÉCNICA: JOIN em Matrículas (tabela N:M) para filtrar Alunos.
-- NOTA: O uso de apelidos de coluna e tabela torna o código mais fácil de ler.

SELECT
    aluno.nome AS nome_do_aluno,
    aluno.email,
    matricula.data_matricula
FROM 
    alunos AS aluno
JOIN 
    matriculas AS matricula ON aluno.id = matricula.aluno_id
WHERE 
    matricula.curso_id = 1 -- Filtro simples para um curso específico
ORDER BY 
    aluno.nome;


-- 3. [REQUISITO AVANÇADO: ARRECADAÇÃO TOTAL]
-- OBJETIVO: Calcular o valor total arrecadado por curso, usando o valor_pago registrado na matrícula.
-- TÉCNICA: Agregação (SUM) e Agrupamento (GROUP BY). Essencial para relatórios financeiros.

SELECT
    curso.titulo AS titulo_do_curso,
    SUM(matricula.valor_pago) AS total_arrecadado_reais
FROM 
    cursos AS curso
JOIN 
    matriculas AS matricula ON curso.id = matricula.curso_id
GROUP BY 
    curso.titulo -- Agrupa os resultados por título para somar o valor de todas as matrículas daquele curso
ORDER BY 
    total_arrecadado_reais DESC;


-- 4. [REQUISITO AVANÇADO: RANKING DE AVALIAÇÕES]
-- OBJETIVO: Apresentar um ranking dos 5 cursos com a melhor média de avaliações.
-- TÉCNICA: Agregação (AVG), Filtro de Agrupamento (HAVING) e Ordenação (LIMIT). Demonstra controle sobre dados agregados.

SELECT
    curso.titulo AS curso,
    AVG(avaliacao.nota) AS media_avaliacao_do_curso,
    COUNT(avaliacao.id) AS total_de_avaliacoes
FROM 
    cursos AS curso
JOIN 
    matriculas AS matricula ON curso.id = matricula.curso_id
JOIN 
    avaliacoes AS avaliacao ON matricula.id = avaliacao.matricula_id
GROUP BY 
    curso.titulo
HAVING 
    COUNT(avaliacao.id) >= 3 -- Garante que o ranking seja justo, filtrando cursos com pelo menos 3 avaliações
ORDER BY 
    media_avaliacao_do_curso DESC
LIMIT 5;


-- 5. [REQUISITO DE EXCLUSÃO]
-- OBJETIVO: Encontrar os instrutores que foram cadastrados, mas que NÃO têm nenhum curso publicado.
-- TÉCNICA: LEFT JOIN + WHERE (IS NULL). Clássico para encontrar "buracos" nos dados ou entidades não utilizadas.

SELECT 
    instrutor.nome AS instrutor_sem_cursos,
    instrutor.email
FROM 
    instrutores AS instrutor
LEFT JOIN 
    cursos AS curso ON instrutor.id = curso.instrutor_id
WHERE 
    curso.id IS NULL -- O curso.id será NULL se não houver correspondência (ou seja, não há cursos)
ORDER BY 
    instrutor.nome;


-- 6. [REQUISITO COMPLEXO: PROGRESSO]
-- OBJETIVO: Calcular o percentual de conclusão de aulas para uma matrícula específica (Ex: Aluno ID=1, Curso ID=2).
-- TÉCNICA: Common Table Expressions (CTEs) ou Subqueries. Usaremos CTEs (WITH) para maior clareza e modularidade, ideal para a defesa.

WITH total_aulas_curso AS (
    -- 1. Calcula o total de aulas do curso
    SELECT 
        curso_id, 
        COUNT(aula.id) AS total_aulas
    FROM 
        modulos AS modulo
    JOIN 
        aulas AS aula ON modulo.id = aula.modulo_id
    GROUP BY 
        curso_id
),
aulas_concluidas_matricula AS (
    -- 2. Conta quantas aulas o aluno realmente concluiu para aquela matrícula
    SELECT
        matricula_id,
        COUNT(progresso.id) AS aulas_concluidas
    FROM 
        progresso_aulas AS progresso
    WHERE 
        progresso.concluida = TRUE
    GROUP BY 
        matricula_id
)
SELECT
    aluno.nome AS nome_aluno,
    curso.titulo AS curso_matriculado,
    (CAST(concluidas.aulas_concluidas AS NUMERIC) * 100.0 / total.total_aulas) AS percentual_conclusao
FROM 
    alunos AS aluno
JOIN 
    matriculas AS matricula ON aluno.id = matricula.aluno_id
JOIN 
    aulas_concluidas_matricula AS concluidas ON matricula.id = concluidas.matricula_id
JOIN 
    total_aulas_curso AS total ON matricula.curso_id = total.curso_id
WHERE 
    aluno.id = 1 AND matricula.curso_id = 2; -- Filtra a matrícula específica (Aluno 1 no Curso 2)


-- 7. [REQUISITO DE EXCLUSÃO AVANÇADO]
-- OBJETIVO: Listar todos os cursos que não têm nenhuma matrícula registrada.
-- TÉCNICA: Subquery com NOT IN. Alternativa mais legível do que o LEFT JOIN IS NULL neste caso.

SELECT 
    curso.titulo
FROM 
    cursos AS curso
WHERE 
    curso.id NOT IN (
        -- Subconsulta: Puxa o ID de todos os cursos que possuem matrículas
        SELECT DISTINCT curso_id FROM matriculas
    );


-- 8. [REQUISITO BÁSICO: ORDENAÇÃO POR DATA]
-- OBJETIVO: Encontrar o aluno mais antigo da plataforma (aquele que se cadastrou primeiro).
-- TÉCNICA: ORDER BY ASC + LIMIT 1. Rápido e direto para encontrar o primeiro/último registro.

SELECT
    nome AS aluno_mais_antigo,
    data_cadastro
FROM 
    alunos
ORDER BY 
    data_cadastro ASC -- ASC (Ascendente) traz os mais antigos primeiro
LIMIT 1;


-- 9. [REQUISITO DE HIERARQUIA]
-- OBJETIVO: Listar os módulos e o número total de aulas em cada um, para um curso específico (Ex: Curso ID = 5).
-- TÉCNICA: JOIN e Agregação (COUNT) para mostrar a estrutura hierárquica (Curso > Módulo > Aula).

SELECT
    modulo.titulo AS titulo_do_modulo,
    COUNT(aula.id) AS numero_de_aulas
FROM 
    modulos AS modulo
JOIN 
    aulas AS aula ON modulo.id = aula.modulo_id
WHERE 
    modulo.curso_id = 5 -- Filtra pelo curso desejado
GROUP BY 
    modulo.titulo
ORDER BY 
    modulo.titulo;


-- 10. [REQUISITO AVANÇADO: AGRUPAMENTO POR DIMENSÃO SUPERIOR]
-- OBJETIVO: Listar a média de avaliações por INSTRUTOR, e não por curso. (Avalia a performance do instrutor em todos os cursos dele).
-- TÉCNICA: Múltiplos JOINs para ligar a Avaliação ao Instrutor e Agrupamento no nível do Instrutor.

SELECT
    instrutor.nome AS instrutor,
    AVG(avaliacao.nota) AS media_avaliacao_geral
FROM 
    instrutores AS instrutor
JOIN 
    cursos AS curso ON instrutor.id = curso.instrutor_id
JOIN 
    matriculas AS matricula ON curso.id = matricula.curso_id
JOIN 
    avaliacoes AS avaliacao ON matricula.id = avaliacao.matricula_id
GROUP BY 
    instrutor.nome
ORDER BY 
    media_avaliacao_geral DESC;


-- 11. [REQUISITO DE FILTRO POR ATRIBUTO]
-- OBJETIVO: Listar todos os alunos que estão matriculados em pelo menos um curso de nível 'avancado'.
-- TÉCNICA: JOINs e DISTINCT para evitar nomes de alunos repetidos, seguidos por filtro simples (WHERE).

SELECT DISTINCT
    aluno.nome AS nome_do_aluno,
    aluno.email
FROM 
    alunos AS aluno
JOIN 
    matriculas AS matricula ON aluno.id = matricula.aluno_id
JOIN 
    cursos AS curso ON matricula.curso_id = curso.id
WHERE 
    curso.nivel = 'avancado' -- Filtro de nível
ORDER BY 
    aluno.nome;


-- 12. [REQUISITO DE DATA/TEMPO]
-- OBJETIVO: Listar a data da última matrícula registrada em cada curso.
-- TÉCNICA: Agregação (MAX) em um campo de data e Agrupamento (GROUP BY) por curso.

SELECT
    curso.titulo AS nome_do_curso,
    MAX(matricula.data_matricula) AS data_da_ultima_matricula
FROM 
    cursos AS curso
JOIN 
    matriculas AS matricula ON curso.id = matricula.curso_id
GROUP BY 
    curso.titulo
ORDER BY 
    data_da_ultima_matricula DESC;