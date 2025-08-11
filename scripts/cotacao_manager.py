from database import Database
from models import Cotacao, ItemCotacao
from cliente_manager import ClienteManager
from datetime import datetime, timedelta

class CotacaoManager:
    def __init__(self, database):
        self.db = database
        self.cliente_manager = ClienteManager(database)
    
    def criar_cotacao(self, id_cliente, validade_dias=30, desconto_percentual=0.0, observacoes=""):
        """Cria uma nova cotação"""
        novo_id = self.db.obter_proximo_id('cotacao')
        
        data_atual = datetime.now().strftime("%Y-%m-%d")
        
        cotacao = Cotacao(novo_id, id_cliente, data_atual, validade_dias, 
                         desconto_percentual, observacoes)
        
        self.db.salvar_cotacao(cotacao)
        
        return cotacao
    
    def listar_todas_cotacoes(self):
        """Lista todas as cotações"""
        return self.db.carregar_cotacoes()
    
    def buscar_cotacao_por_id(self, id_cotacao):
        """Busca cotação por ID"""
        return self.db.buscar_cotacao(id_cotacao)
    
    def atualizar_cotacao(self, cotacao):
        """Atualiza uma cotação existente"""
        self.db.salvar_cotacao(cotacao)
        return True
    
    def excluir_cotacao(self, id_cotacao):
        """Exclui uma cotação"""
        return self.db.remover_cotacao(id_cotacao)
    
    def alterar_status_cotacao(self, id_cotacao, novo_status):
        """Altera o status de uma cotação"""
        cotacao = self.buscar_cotacao_por_id(id_cotacao)
        if cotacao:
            cotacao.status = novo_status
            return self.atualizar_cotacao(cotacao)
        return False
    
    def verificar_cotacoes_expiradas(self):
        """Verifica e atualiza cotações expiradas"""
        cotacoes = self.listar_todas_cotacoes()
        hoje = datetime.now().date()
        
        for cotacao in cotacoes:
            if cotacao.status == "Pendente":
                data_cotacao = datetime.strptime(cotacao.data_cotacao, "%Y-%m-%d").date()
                data_vencimento = data_cotacao + timedelta(days=cotacao.validade_dias)
                
                if hoje > data_vencimento:
                    self.alterar_status_cotacao(cotacao.id_cotacao, "Expirada")
    
    def obter_estatisticas(self):
        """Obtém estatísticas das cotações"""
        cotacoes = self.listar_todas_cotacoes()
        
        total_cotacoes = len(cotacoes)
        pendentes = len([c for c in cotacoes if c.status == "Pendente"])
        aprovadas = len([c for c in cotacoes if c.status == "Aprovada"])
        rejeitadas = len([c for c in cotacoes if c.status == "Rejeitada"])
        expiradas = len([c for c in cotacoes if c.status == "Expirada"])
        
        valor_total_pendentes = sum(c.total for c in cotacoes if c.status == "Pendente")
        valor_total_aprovadas = sum(c.total for c in cotacoes if c.status == "Aprovada")
        
        return {
            'total_cotacoes': total_cotacoes,
            'pendentes': pendentes,
            'aprovadas': aprovadas,
            'rejeitadas': rejeitadas,
            'expiradas': expiradas,
            'valor_total_pendentes': valor_total_pendentes,
            'valor_total_aprovadas': valor_total_aprovadas
        }
    
    def filtrar_cotacoes_por_status(self, status):
        """Filtra cotações por status"""
        cotacoes = self.listar_todas_cotacoes()
        return [c for c in cotacoes if c.status == status]
    
    def filtrar_cotacoes_por_cliente(self, id_cliente):
        """Filtra cotações por cliente"""
        cotacoes = self.listar_todas_cotacoes()
        return [c for c in cotacoes if c.id_cliente == id_cliente]
    
    def filtrar_cotacoes_por_periodo(self, data_inicio, data_fim):
        """Filtra cotações por período"""
        cotacoes = self.listar_todas_cotacoes()
        resultado = []
        
        for cotacao in cotacoes:
            data_cotacao = datetime.strptime(cotacao.data_cotacao, "%Y-%m-%d").date()
            if data_inicio <= data_cotacao <= data_fim:
                resultado.append(cotacao)
        
        return resultado
