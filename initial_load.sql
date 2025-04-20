-- Extensão para gerar UUIDs automaticamente
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de usuários
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL
);
ALTER TABLE usuarios ADD CONSTRAINT nome_unico UNIQUE (nome);

-- Tabela de resultados de jogos
CREATE TABLE resultados_jogos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id),
    data DATE NOT NULL,
    torneio VARCHAR(150) NOT NULL,
    compras NUMERIC(12, 2) DEFAULT 0.00,
    premiacao NUMERIC(12, 2) DEFAULT 0.00,
    
    -- Restrições
    CONSTRAINT resultado_unico UNIQUE (usuario_id, data, torneio)
);

INSERT INTO usuarios (nome) VALUES ('ALBERTO MAGNO');
INSERT INTO usuarios (nome) VALUES ('ANDERSON JOSE DA SILVA PORTELA');
INSERT INTO usuarios (nome) VALUES ('BRUNO ZEBRAL');
INSERT INTO usuarios (nome) VALUES ('BRUNO ESTEVES');
INSERT INTO usuarios (nome) VALUES ('CARLOS BRANT');
INSERT INTO usuarios (nome) VALUES ('DANILO BURLE');
INSERT INTO usuarios (nome) VALUES ('DAVID BRAINERD');
INSERT INTO usuarios (nome) VALUES ('DIEGO ARANDA');
INSERT INTO usuarios (nome) VALUES ('FABIO RODRIGO');
INSERT INTO usuarios (nome) VALUES ('GABRIEL VAZ');
INSERT INTO usuarios (nome) VALUES ('GUILHERME ANDRADE');
INSERT INTO usuarios (nome) VALUES ('GUSTAVO RODRIGUES');
INSERT INTO usuarios (nome) VALUES ('HENRIQUE ANGELO');
INSERT INTO usuarios (nome) VALUES ('IGOR LUIZ');
INSERT INTO usuarios (nome) VALUES ('ITHALO ALVES');
INSERT INTO usuarios (nome) VALUES ('JEFERSON GUSTAVO');
INSERT INTO usuarios (nome) VALUES ('JP CURVELLO');
INSERT INTO usuarios (nome) VALUES ('JONATAS CASTRO');
INSERT INTO usuarios (nome) VALUES ('LUCAS AUGUSTO');
INSERT INTO usuarios (nome) VALUES ('LUCAS LlOYD');
INSERT INTO usuarios (nome) VALUES ('LUIS HENRIQUE ARCANJO');
INSERT INTO usuarios (nome) VALUES ('MATEUS MARTINS');
INSERT INTO usuarios (nome) VALUES ('MATEUS BRITO');
INSERT INTO usuarios (nome) VALUES ('MIGUEL GARCIA');
INSERT INTO usuarios (nome) VALUES ('OTAVIO CASEMIRO DE SA');
INSERT INTO usuarios (nome) VALUES ('PEDRO RIBAS');
INSERT INTO usuarios (nome) VALUES ('PEDRO LIMA');
INSERT INTO usuarios (nome) VALUES ('RAFAEL MARTINS');
INSERT INTO usuarios (nome) VALUES ('RAFAEL MOURA');
INSERT INTO usuarios (nome) VALUES ('RAINER ASSIS');
INSERT INTO usuarios (nome) VALUES ('RODRIGO PAPINI');
INSERT INTO usuarios (nome) VALUES ('WELINGTON FERREIRA DE SOUZA');
INSERT INTO usuarios (nome) VALUES ('WILLIAN ISRAEL');
INSERT INTO usuarios (nome) VALUES ('LUIZ GUSTAVO ASSUNCAO');
INSERT INTO usuarios (nome) VALUES ('PEDRO BEAUMONTE');
INSERT INTO usuarios (nome) VALUES ('LUIZ CARLOS');
INSERT INTO usuarios (nome) VALUES ('IGOR HENRIQUE');
INSERT INTO usuarios (nome) VALUES ('DIEGO ALMEIDA');
INSERT INTO usuarios (nome) VALUES ('JEFERSON CESAR');