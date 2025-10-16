import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class FirebaseService:
    def __init__(self):
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Inicializa o Firebase Admin SDK"""
        try:
            # Verifica se já foi inicializado
            if not firebase_admin._apps:
                # Tenta usar service account key se disponível
                service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
                
                if service_account_path and os.path.exists(service_account_path):
                    # Usa arquivo de service account
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                    print("✅ Firebase inicializado com service account")
                else:
                    # Tenta usar variáveis de ambiente
                    service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
                    
                    if service_account_json:
                        # Parse do JSON das variáveis de ambiente
                        service_account_info = json.loads(service_account_json)
                        cred = credentials.Certificate(service_account_info)
                        firebase_admin.initialize_app(cred)
                        print("✅ Firebase inicializado com variáveis de ambiente")
                    else:
                        # Modo de desenvolvimento - usa credenciais padrão
                        # ou pode usar Application Default Credentials (ADC)
                        firebase_admin.initialize_app()
                        print("✅ Firebase inicializado com credenciais padrão")
            
            # Inicializa o Firestore
            self.db = firestore.client()
            print("✅ Firestore conectado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar Firebase: {str(e)}")
            print("⚠️  Sistema continuará usando SQLite como fallback")
            self.db = None
    
    def is_connected(self) -> bool:
        """Verifica se o Firebase está conectado"""
        return self.db is not None
    
    # ==================== ANÁLISES ====================
    
    def registrar_analise(
        self,
        ticket_numero: str,
        dados_movidesk: Dict[str, Any],
        resultado_ia: Dict[str, Any],
        tempo_ms: int,
        usuario: Optional[str] = None
    ) -> Optional[str]:
        """Registra uma análise no Firebase"""
        if not self.is_connected():
            return None
            
        try:
            analise_data = {
                'ticket_numero': ticket_numero,
                'usuario_nome': usuario,
                'titulo_ticket': dados_movidesk.get('titulo', ''),
                'cliente_nome': dados_movidesk.get('cliente', ''),
                'tipo_identificado': resultado_ia.get('tipo', ''),
                'modulo_identificado': resultado_ia.get('modulo', ''),
                'chamado_gerado': resultado_ia.get('chamado_texto', ''),
                'tempo_processamento_ms': tempo_ms,
                'tokens_usados': resultado_ia.get('tokens', 0),
                'data_analise': firestore.SERVER_TIMESTAMP,
                'foi_copiado': False,
                'metadata': resultado_ia.get('metadata', {}),
                'dados_movidesk_completos': dados_movidesk  # Salva dados completos para referência
            }
            
            # Salva na coleção 'analises'
            doc_ref = self.db.collection('analises').add(analise_data)
            analise_id = doc_ref[1].id
            
            print(f"✅ Análise salva no Firebase com ID: {analise_id}")
            return analise_id
            
        except Exception as e:
            print(f"❌ Erro ao salvar análise no Firebase: {str(e)}")
            return None
    
    def marcar_como_copiado(self, analise_id: str):
        """Marca que o suporte copiou o texto"""
        if not self.is_connected():
            return False
            
        try:
            self.db.collection('analises').document(analise_id).update({
                'foi_copiado': True,
                'data_copiado': firestore.SERVER_TIMESTAMP
            })
            print(f"✅ Análise {analise_id} marcada como copiada")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao marcar como copiado: {str(e)}")
            return False
    
    def get_analise_por_id(self, analise_id: str) -> Optional[Dict]:
        """Busca uma análise por ID"""
        if not self.is_connected():
            return None
            
        try:
            doc = self.db.collection('analises').document(analise_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar análise: {str(e)}")
            return None
    
    # ==================== FEEDBACKS ====================
    
    def registrar_feedback(
        self,
        analise_id: str,
        foi_util: bool,
        nota: Optional[int] = None,
        comentario: Optional[str] = None,
        texto_final: Optional[str] = None
    ) -> Optional[str]:
        """Registra feedback do suporte"""
        if not self.is_connected():
            return None
            
        try:
            feedback_data = {
                'analise_id': analise_id,
                'foi_util': foi_util,
                'nota': nota,
                'comentario': comentario,
                'texto_final_usado': texto_final,
                'data_feedback': firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.db.collection('feedbacks').add(feedback_data)
            feedback_id = doc_ref[1].id
            
            print(f"✅ Feedback salvo no Firebase com ID: {feedback_id}")
            return feedback_id
            
        except Exception as e:
            print(f"❌ Erro ao salvar feedback: {str(e)}")
            return None
    
    # ==================== ESTATÍSTICAS ====================
    
    def get_estatisticas_periodo(self, dias: int = 7) -> Dict[str, Any]:
        """Retorna estatísticas dos últimos N dias"""
        if not self.is_connected():
            return self._get_empty_stats()
            
        try:
            # Calcula data de início
            from datetime import timedelta
            data_inicio = datetime.now() - timedelta(days=dias)
            
            # Busca análises do período
            analises_ref = self.db.collection('analises').where('data_analise', '>=', data_inicio)
            analises = analises_ref.stream()
            
            total_analises = 0
            total_inconsistencias = 0
            tempo_total = 0
            modulos_count = {}
            
            for doc in analises:
                data = doc.to_dict()
                total_analises += 1
                
                if data.get('tipo_identificado') == 'inconsistencia':
                    total_inconsistencias += 1
                
                tempo_total += data.get('tempo_processamento_ms', 0)
                
                modulo = data.get('modulo_identificado')
                if modulo:
                    modulos_count[modulo] = modulos_count.get(modulo, 0) + 1
            
            # Busca feedbacks
            feedbacks_ref = self.db.collection('feedbacks')
            feedbacks = feedbacks_ref.stream()
            
            total_feedbacks = 0
            feedback_positivo = 0
            
            for doc in feedbacks:
                data = doc.to_dict()
                total_feedbacks += 1
                if data.get('foi_util'):
                    feedback_positivo += 1
            
            tempo_medio = tempo_total / total_analises if total_analises > 0 else 0
            taxa_aprovacao = (feedback_positivo / total_feedbacks * 100) if total_feedbacks > 0 else 0
            
            # Top 5 módulos
            modulos_top = sorted(modulos_count.items(), key=lambda x: x[1], reverse=True)[:5]
            modulos_top = [{'modulo_identificado': k, 'total': v} for k, v in modulos_top]
            
            return {
                'total_analises': total_analises,
                'total_inconsistencias': total_inconsistencias,
                'taxa_aprovacao': round(taxa_aprovacao, 1),
                'tempo_medio_ms': round(tempo_medio, 2),
                'modulos_top': modulos_top,
                'periodo_dias': dias
            }
            
        except Exception as e:
            print(f"❌ Erro ao buscar estatísticas: {str(e)}")
            return self._get_empty_stats()
    
    def get_analises_recentes(self, limit: int = 10) -> List[Dict]:
        """Retorna análises mais recentes"""
        if not self.is_connected():
            return []
            
        try:
            analises_ref = self.db.collection('analises').order_by('data_analise', direction=firestore.Query.DESCENDING).limit(limit)
            analises = analises_ref.stream()
            
            result = []
            for doc in analises:
                data = doc.to_dict()
                data['id'] = doc.id
                result.append(data)
            
            return result
            
        except Exception as e:
            print(f"❌ Erro ao buscar análises recentes: {str(e)}")
            return []
    
    def _get_empty_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas vazias quando Firebase não está disponível"""
        return {
            'total_analises': 0,
            'total_inconsistencias': 0,
            'taxa_aprovacao': 0,
            'tempo_medio_ms': 0,
            'modulos_top': [],
            'periodo_dias': 7
        }
    
    # ==================== CACHE ====================
    
    def get_cache_ticket(self, ticket_numero: str) -> Optional[Dict]:
        """Busca ticket no cache do Firebase"""
        if not self.is_connected():
            return None
            
        try:
            cache_ref = self.db.collection('tickets_cache').document(ticket_numero)
            doc = cache_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                expira_em = data.get('expira_em')
                
                if expira_em and expira_em > datetime.now():
                    return data.get('dados_movidesk')
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar cache: {str(e)}")
            return None
    
    def salvar_cache_ticket(
        self,
        ticket_numero: str,
        dados: Dict[str, Any],
        horas_validade: int = 24
    ):
        """Salva ticket no cache do Firebase"""
        if not self.is_connected():
            return False
            
        try:
            from datetime import timedelta
            expira_em = datetime.now() + timedelta(hours=horas_validade)
            
            cache_data = {
                'dados_movidesk': dados,
                'data_cache': firestore.SERVER_TIMESTAMP,
                'expira_em': expira_em
            }
            
            self.db.collection('tickets_cache').document(ticket_numero).set(cache_data)
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar cache: {str(e)}")
            return False

# Instância global do serviço
firebase_service = FirebaseService()
