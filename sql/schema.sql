-- #################################################################
-- # ARQUIVO: sql/schema.sql
-- # Modelagem do Banco de Dados para EduTech (9 Tabelas - DDL)
-- #################################################################

-- 1. ALUNOS (Entidade: Usuário Consumidor)
CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_nascimento DATE,
    data_cadastro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 2. INSTRUTORES (Entidade: Usuário Criador de Conteúdo)
CREATE TABLE instrutores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    especialidade VARCHAR(100),
    biografia TEXT
);

-- 3. CATEGORIAS (Entidade: Organização dos Cursos)
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT
);

-- 4. CURSOS (Entidade: O Produto)
CREATE TABLE cursos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    
    -- FKs para 3NF
    categoria_id INTEGER NOT NULL REFERENCES categorias(id),
    instrutor_id INTEGER NOT NULL REFERENCES instrutores(id),
    
    preco NUMERIC(10, 2) NOT NULL CHECK (preco >= 0.00),
    carga_horaria INTEGER NOT NULL CHECK (carga_horaria > 0),
    
    nivel VARCHAR(20) NOT NULL CHECK (nivel IN ('iniciante', 'intermediario', 'avancado')), 
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 5. MODULOS (Relacionamento 1:M com Cursos)
CREATE TABLE modulos (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL REFERENCES cursos(id),
    titulo VARCHAR(100) NOT NULL,
    ordem INTEGER NOT NULL, 
    descricao TEXT,
    
    UNIQUE (curso_id, ordem) 
);

-- 6. AULAS (Relacionamento 1:M com Módulos)
CREATE TABLE aulas (
    id SERIAL PRIMARY KEY,
    modulo_id INTEGER NOT NULL REFERENCES modulos(id),
    titulo VARCHAR(100) NOT NULL,
    ordem INTEGER NOT NULL,
    duracao_minutos INTEGER NOT NULL CHECK (duracao_minutos > 0),
    
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('video', 'texto', 'quiz')),
    
    UNIQUE (modulo_id, ordem)
);

-- 7. MATRICULAS (Tabela de Junção M:N entre Alunos e Cursos)
CREATE TABLE matriculas (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES alunos(id),
    curso_id INTEGER NOT NULL REFERENCES cursos(id),
    
    data_matricula TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    data_conclusao DATE, 
    
    status VARCHAR(15) NOT NULL CHECK (status IN ('ativa', 'concluida', 'cancelada')),
    valor_pago NUMERIC(10, 2) NOT NULL CHECK (valor_pago >= 0.00),
    
    UNIQUE (aluno_id, curso_id)
);

-- 8. PROGRESSO_AULAS (Acompanha o Aluno na Matrícula)
CREATE TABLE progresso_aulas (
    id SERIAL PRIMARY KEY,
    matricula_id INTEGER NOT NULL REFERENCES matriculas(id),
    aula_id INTEGER NOT NULL REFERENCES aulas(id),
    
    concluida BOOLEAN DEFAULT FALSE NOT NULL,
    data_conclusao TIMESTAMP WITH TIME ZONE,
    tempo_assistido_minutos INTEGER DEFAULT 0 CHECK (tempo_assistido_minutos >= 0),
    
    UNIQUE (matricula_id, aula_id) 
);

-- 9. AVALIACOES (Aluno avalia Curso)
CREATE TABLE avaliacoes (
    id SERIAL PRIMARY KEY,
    matricula_id INTEGER UNIQUE NOT NULL REFERENCES matriculas(id), 
    curso_id INTEGER NOT NULL REFERENCES cursos(id),
    
    nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5), 
    comentario TEXT,
    data_avaliacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
