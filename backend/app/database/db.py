import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from pathlib import Path
import os

class Database:
    def __init__(self, db_path: str = "ia_chamados.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inicializa o banco de dados com o schema"""
        schema_path = Path(__file__).parent / "schema.sql"
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Retorna uma conexão com o banco"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ==================== ANÁLISES ====================
    
    def registrar_analise(
        self,
        ticket_numero: str,
        dados_movidesk: Dict[str, Any],
        resultado_ia: Dict[str, Any],
        tempo_ms: int,
        usuario: Optional[str] = None
    ) -> int:
        """Registra uma análise completa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analises 
            (ticket_numero, usuario_nome, titulo_ticket, cliente_nome,
             tipo_identificado, modulo_identificado, chamado_gerado,
             tempo_processamento_ms, tokens_usados)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_numero,
            usuario,
            dados_movidesk.get('titulo', ''),
            dados_movidesk.get('cliente', ''),
            resultado_ia.get('tipo', ''),
            resultado_ia.get('modulo', ''),
            resultado_ia.get('chamado_texto', ''),
            tempo_ms,
            resultado_ia.get('tokens', 0)
        ))
        
        conn.commit()
        analise_id = cursor.lastrowid
        conn.close()
        
        return analise_id
    
    def marcar_como_copiado(self, analise_id: int):
        """Marca que o suporte copiou o texto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE analises 
            SET foi_copiado = TRUE 
            WHERE id = ?
        """, (analise_id,))
        
        conn.commit()
        conn.close()
    
    def get_analise_por_id(self, analise_id: int) -> Optional[Dict]:
        """Busca uma análise por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM analises WHERE id = ?", (analise_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    # ==================== FEEDBACKS ====================
    
    def registrar_feedback(
        self,
        analise_id: int,
        foi_util: bool,
        nota: Optional[int] = None,
        comentario: Optional[str] = None,
        texto_final: Optional[str] = None
    ) -> int:
        """Registra feedback do suporte"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO feedbacks 
            (analise_id, foi_util, nota, comentario, texto_final_usado)
            VALUES (?, ?, ?, ?, ?)
        """, (analise_id, foi_util, nota, comentario, texto_final))
        
        conn.commit()
        feedback_id = cursor.lastrowid
        conn.close()
        
        return feedback_id
    
    # ==================== CACHE ====================
    
    def get_cache_ticket(self, ticket_numero: str) -> Optional[Dict]:
        """Busca ticket no cache se ainda válido"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT dados_movidesk, expira_em 
            FROM tickets_cache 
            WHERE ticket_numero = ?
        """, (ticket_numero,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            expira_em = datetime.fromisoformat(row['expira_em'])
            if expira_em > datetime.now():
                return json.loads(row['dados_movidesk'])
        
        return None
    
    def salvar_cache_ticket(
        self,
        ticket_numero: str,
        dados: Dict[str, Any],
        horas_validade: int = 24
    ):
        """Salva ticket no cache"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        expira_em = datetime.now() + timedelta(hours=horas_validade)
        
        cursor.execute("""
            INSERT OR REPLACE INTO tickets_cache 
            (ticket_numero, dados_movidesk, data_cache, expira_em)
            VALUES (?, ?, ?, ?)
        """, (
            ticket_numero,
            json.dumps(dados, ensure_ascii=False),
            datetime.now().isoformat(),
            expira_em.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def limpar_cache_expirado(self):
        """Remove cache expirado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM tickets_cache 
            WHERE expira_em < ?
        """, (datetime.now().isoformat(),))
        
        conn.commit()
        deletados = cursor.rowcount
        conn.close()
        
        return deletados
    
    # ==================== ESTATÍSTICAS ====================
    
    def get_estatisticas_periodo(self, dias: int = 7) -> Dict[str, Any]:
        """Retorna estatísticas dos últimos N dias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        data_inicio = datetime.now() - timedelta(days=dias)
        
        # Total de análises
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM analises
            WHERE data_analise >= ?
        """, (data_inicio.isoformat(),))
        total_analises = cursor.fetchone()['total']
        
        # Inconsistências detectadas
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM analises
            WHERE data_analise >= ?
            AND tipo_identificado = 'inconsistencia'
        """, (data_inicio.isoformat(),))
        total_inconsistencias = cursor.fetchone()['total']
        
        # Feedback positivo
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM feedbacks f
            JOIN analises a ON f.analise_id = a.id
            WHERE a.data_analise >= ?
            AND f.foi_util = TRUE
        """, (data_inicio.isoformat(),))
        feedback_positivo = cursor.fetchone()['total']
        
        # Total de feedbacks
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM feedbacks f
            JOIN analises a ON f.analise_id = a.id
            WHERE a.data_analise >= ?
        """, (data_inicio.isoformat(),))
        total_feedbacks = cursor.fetchone()['total']
        
        # Tempo médio
        cursor.execute("""
            SELECT AVG(tempo_processamento_ms) as media
            FROM analises
            WHERE data_analise >= ?
        """, (data_inicio.isoformat(),))
        tempo_medio = cursor.fetchone()['media'] or 0
        
        # Módulos mais comuns
        cursor.execute("""
            SELECT modulo_identificado, COUNT(*) as total
            FROM analises
            WHERE data_analise >= ?
            AND modulo_identificado IS NOT NULL
            AND modulo_identificado != ''
            GROUP BY modulo_identificado
            ORDER BY total DESC
            LIMIT 5
        """, (data_inicio.isoformat(),))
        modulos = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        taxa_aprovacao = 0
        if total_feedbacks > 0:
            taxa_aprovacao = (feedback_positivo / total_feedbacks) * 100
        
        return {
            'total_analises': total_analises,
            'total_inconsistencias': total_inconsistencias,
            'taxa_aprovacao': round(taxa_aprovacao, 1),
            'tempo_medio_ms': round(tempo_medio, 2),
            'modulos_top': modulos,
            'periodo_dias': dias
        }
    
    def get_analises_recentes(self, limit: int = 10) -> List[Dict]:
        """Retorna análises mais recentes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id,
                ticket_numero,
                usuario_nome,
                data_analise,
                tipo_identificado,
                modulo_identificado,
                chamado_gerado,
                foi_copiado
            FROM analises
            ORDER BY data_analise DESC
            LIMIT ?
        """, (limit,))
        
        analises = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return analises

