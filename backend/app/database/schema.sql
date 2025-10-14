-- ============================================
-- SCHEMA DO BANCO DE DADOS - IA CHAMADOS
-- ============================================

-- 1️⃣ LOGS DE ANÁLISE (Principal)
CREATE TABLE IF NOT EXISTS analises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_numero VARCHAR(50) NOT NULL,
    usuario_nome VARCHAR(100),
    data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Dados do Movidesk
    titulo_ticket TEXT,
    cliente_nome VARCHAR(200),
    
    -- Resultado da IA
    tipo_identificado VARCHAR(50),
    modulo_identificado VARCHAR(100),
    chamado_gerado TEXT,
    
    -- Métricas
    tempo_processamento_ms INTEGER,
    tokens_usados INTEGER,
    
    -- Status
    foi_copiado BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_ticket_numero ON analises(ticket_numero);
CREATE INDEX IF NOT EXISTS idx_data_analise ON analises(data_analise);
CREATE INDEX IF NOT EXISTS idx_modulo ON analises(modulo_identificado);

-- 2️⃣ FEEDBACK DO SUPORTE
CREATE TABLE IF NOT EXISTS feedbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analise_id INTEGER NOT NULL,
    data_feedback TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    foi_util BOOLEAN,
    nota INTEGER CHECK(nota >= 1 AND nota <= 5),
    comentario TEXT,
    texto_final_usado TEXT,
    
    FOREIGN KEY (analise_id) REFERENCES analises(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_analise_id ON feedbacks(analise_id);

-- 3️⃣ CACHE DE TICKETS
CREATE TABLE IF NOT EXISTS tickets_cache (
    ticket_numero VARCHAR(50) PRIMARY KEY,
    dados_movidesk TEXT,
    data_cache TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expira_em TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_expira_em ON tickets_cache(expira_em);

-- 4️⃣ ESTATÍSTICAS DIÁRIAS
CREATE TABLE IF NOT EXISTS estatisticas_diarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL UNIQUE,
    total_analises INTEGER DEFAULT 0,
    total_inconsistencias INTEGER DEFAULT 0,
    total_feedback_positivo INTEGER DEFAULT 0,
    media_tempo_processamento_ms FLOAT,
    modulo_mais_comum VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_data_stats ON estatisticas_diarias(data);

