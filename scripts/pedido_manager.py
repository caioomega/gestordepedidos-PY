from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict
from models import Pedido, Cliente, Produto, StatusPedido, ItemPedido
from database import Database
from cliente_manager import ClienteManager
from produto_manager import ProdutoManager

class PedidoManager:
    def __init__(self, database: Database):
        self.db = database
        self.cliente_manager = ClienteManager(database)
        self.produto_manager = ProdutoManager(database)
    
    def criar_pedido(self, id_cliente: int, observacoes: str = "") -> Tuple[bool, str, Optional[Pedido]]:
        """
        Cria um novo pedido vazio
        Retorna: (sucesso, mensagem, pedido_criado)
        """
        # Verificar se cliente existe
        cliente = self.cliente_manager.buscar_cliente_por_id(id_cliente)
        if not cliente:
            return False, f"Cliente com ID {id_cliente} não encontrado", None
        
        # Criar pedido
        id_pedido = self.db.obter_proximo_id("pedido")
        pedido = Pedido(id_pedido, cliente)
        pedido.observacoes = observacoes.strip()
        
        # Salvar no banco
        self.db.salvar_pedido(pedido)
        
        return True, f"Pedido {id_pedido} criado com sucesso para {cliente.nome}", pedido
    
    def adicionar_item_pedido(self, id_pedido: int, id_produto: int, quantidade: int) -> Tuple[bool, str]:
        """
        Adiciona item ao pedido
        Retorna: (sucesso, mensagem)
        """
        # Buscar pedido
        pedido = self.db.buscar_pedido(id_pedido)
        if not pedido:
            return False, f"Pedido {id_pedido} não encontrado"
        
        # Verificar se pedido pode ser editado
        if pedido.status in [StatusPedido.ENVIADO, StatusPedido.ENTREGUE, StatusPedido.CANCELADO]:
            return False, f"Não é possível editar pedido com status {pedido.status.value}"
        
        # Buscar produto
        produto = self.produto_manager.buscar_produto_por_id(id_produto)
        if not produto:
            return False, f"Produto com ID {id_produto} não encontrado"
        
        # Verificar se produto está ativo
        if not produto.ativo:
            return False, f"Produto {produto.nome} está desativado"
        
        # Verificar quantidade
        if quantidade <= 0:
            return False, "Quantidade deve ser maior que zero"
        
        # Verificar estoque disponível
        quantidade_atual_pedido = 0
        for item in pedido.itens:
            if item.produto.id_produto == id_produto:
                quantidade_atual_pedido = item.quantidade
                break
        
        quantidade_total_necessaria = quantidade_atual_pedido + quantidade
        if produto.estoque < quantidade_total_necessaria:
            return False, f"Estoque insuficiente. Disponível: {produto.estoque}, Necessário: {quantidade_total_necessaria}"
        
        try:
            # Adicionar item ao pedido
            pedido.adicionar_item(produto, quantidade)
            
            # Salvar pedido
            self.db.salvar_pedido(pedido)
            
            return True, f"Item {produto.nome} (x{quantidade}) adicionado ao pedido {id_pedido}"
        
        except ValueError as e:
            return False, str(e)
    
    def remover_item_pedido(self, id_pedido: int, id_produto: int) -> Tuple[bool, str]:
        """
        Remove item do pedido
        Retorna: (sucesso, mensagem)
        """
        # Buscar pedido
        pedido = self.db.buscar_pedido(id_pedido)
        if not pedido:
            return False, f"Pedido {id_pedido} não encontrado"
        
        # Verificar se pedido pode ser editado
        if pedido.status in [StatusPedido.ENVIADO, StatusPedido.ENTREGUE, StatusPedido.CANCELADO]:
            return False, f"Não é possível editar pedido com status {pedido.status.value}"
        
        # Verificar se item existe no pedido
        item_existe = any(item.produto.id_produto == id_produto for item in pedido.itens)
        if not item_existe:
            return False, f"Produto não encontrado no pedido {id_pedido}"
        
        # Remover item
        nome_produto = None
        for item in pedido.itens:
            if item.produto.id_produto == id_produto:
                nome_produto = item.produto.nome
                break
        
        pedido.remover_item(id_produto)
        
        # Salvar pedido
        self.db.salvar_pedido(pedido)
        
        return True, f"Item {nome_produto} removido do pedido {id_pedido}"
    
    def alterar_status_pedido(self, id_pedido: int, novo_status: StatusPedido) -> Tuple[bool, str]:
        """
        Altera status do pedido e gerencia estoque
        Retorna: (sucesso, mensagem)
        """
        # Buscar pedido
        pedido = self.db.buscar_pedido(id_pedido)
        if not pedido:
            return False, f"Pedido {id_pedido} não encontrado"
        
        status_anterior = pedido.status
        
        # Verificar transições válidas
        transicoes_validas = {
            StatusPedido.PENDENTE: [StatusPedido.PROCESSANDO, StatusPedido.CANCELADO],
            StatusPedido.PROCESSANDO: [StatusPedido.ENVIADO, StatusPedido.CANCELADO],
            StatusPedido.ENVIADO: [StatusPedido.ENTREGUE],
            StatusPedido.ENTREGUE: [],  # Status final
            StatusPedido.CANCELADO: []  # Status final
        }
        
        if novo_status not in transicoes_validas[status_anterior]:
            return False, f"Transição inválida de {status_anterior.value} para {novo_status.value}"
        
        # Gerenciar estoque baseado na mudança de status
        if status_anterior == StatusPedido.PENDENTE and novo_status == StatusPedido.PROCESSANDO:
            # Reservar estoque
            for item in pedido.itens:
                produto = self.produto_manager.buscar_produto_por_id(item.produto.id_produto)
                if produto and produto.estoque < item.quantidade:
                    return False, f"Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque}"
                
                # Reduzir estoque
                sucesso, mensagem = self.produto_manager.ajustar_estoque(
                    item.produto.id_produto, item.quantidade, "remover"
                )
                if not sucesso:
                    return False, f"Erro ao reservar estoque: {mensagem}"
        
        elif status_anterior == StatusPedido.PROCESSANDO and novo_status == StatusPedido.CANCELADO:
            # Devolver estoque
            for item in pedido.itens:
                self.produto_manager.ajustar_estoque(
                    item.produto.id_produto, item.quantidade, "adicionar"
                )
        
        elif status_anterior == StatusPedido.PENDENTE and novo_status == StatusPedido.CANCELADO:
            # Pedido cancelado antes de processar - não precisa devolver estoque
            pass
        
        # Alterar status
        pedido.alterar_status(novo_status)
        
        # Salvar pedido
        self.db.salvar_pedido(pedido)
        
        return True, f"Status do pedido {id_pedido} alterado de {status_anterior.value} para {novo_status.value}"
    
    def buscar_pedido_por_id(self, id_pedido: int) -> Optional[Pedido]:
        """Busca pedido por ID"""
        return self.db.buscar_pedido(id_pedido)
    
    def listar_pedidos_por_cliente(self, id_cliente: int) -> List[Pedido]:
        """Lista todos os pedidos de um cliente"""
        pedidos = self.db.carregar_pedidos()
        return [
            pedido for pedido in pedidos 
            if pedido.cliente.id_cliente == id_cliente
        ]
    
    def listar_pedidos_por_status(self, status: StatusPedido) -> List[Pedido]:
        """Lista pedidos por status"""
        pedidos = self.db.carregar_pedidos()
        return [pedido for pedido in pedidos if pedido.status == status]
    
    def listar_pedidos_por_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[Pedido]:
        """Lista pedidos em um período específico"""
        pedidos = self.db.carregar_pedidos()
        return [
            pedido for pedido in pedidos 
            if data_inicio <= pedido.data_pedido <= data_fim
        ]
    
    def listar_todos_pedidos(self, ordenar_por: str = "data") -> List[Pedido]:
        """
        Lista todos os pedidos
        ordenar_por: 'data', 'cliente', 'status', 'valor'
        """
        pedidos = self.db.carregar_pedidos()
        
        if ordenar_por == "data":
            return sorted(pedidos, key=lambda p: p.data_pedido, reverse=True)
        elif ordenar_por == "cliente":
            return sorted(pedidos, key=lambda p: p.cliente.nome.lower())
        elif ordenar_por == "status":
            return sorted(pedidos, key=lambda p: p.status.value)
        elif ordenar_por == "valor":
            return sorted(pedidos, key=lambda p: p.total, reverse=True)
        else:
            return pedidos
    
    def obter_estatisticas_pedidos(self) -> Dict:
        """Retorna estatísticas completas dos pedidos"""
        pedidos = self.db.carregar_pedidos()
        
        if not pedidos:
            return {
                'total_pedidos': 0,
                'pedidos_por_status': {},
                'receita_total': 0,
                'receita_por_mes': {},
                'ticket_medio': 0,
                'cliente_mais_pedidos': None,
                'produto_mais_vendido': None
            }
        
        # Estatísticas básicas
        total_pedidos = len(pedidos)
        
        # Pedidos por status
        pedidos_por_status = {}
        for status in StatusPedido:
            pedidos_por_status[status.value] = len([p for p in pedidos if p.status == status])
        
        # Receita total (apenas pedidos entregues)
        pedidos_entregues = [p for p in pedidos if p.status == StatusPedido.ENTREGUE]
        receita_total = sum(p.total for p in pedidos_entregues)
        
        # Receita por mês
        receita_por_mes = {}
        for pedido in pedidos_entregues:
            mes_ano = pedido.data_pedido.strftime("%Y-%m")
            receita_por_mes[mes_ano] = receita_por_mes.get(mes_ano, 0) + pedido.total
        
        # Ticket médio
        ticket_medio = receita_total / len(pedidos_entregues) if pedidos_entregues else 0
        
        # Cliente com mais pedidos
        pedidos_por_cliente = {}
        for pedido in pedidos:
            id_cliente = pedido.cliente.id_cliente
            pedidos_por_cliente[id_cliente] = pedidos_por_cliente.get(id_cliente, 0) + 1
        
        cliente_mais_pedidos = None
        if pedidos_por_cliente:
            id_cliente_top = max(pedidos_por_cliente, key=pedidos_por_cliente.get)
            cliente_mais_pedidos = {
                'cliente': next(p.cliente.nome for p in pedidos if p.cliente.id_cliente == id_cliente_top),
                'quantidade_pedidos': pedidos_por_cliente[id_cliente_top]
            }
        
        # Produto mais vendido
        vendas_por_produto = {}
        for pedido in pedidos_entregues:
            for item in pedido.itens:
                id_produto = item.produto.id_produto
                vendas_por_produto[id_produto] = vendas_por_produto.get(id_produto, 0) + item.quantidade
        
        produto_mais_vendido = None
        if vendas_por_produto:
            id_produto_top = max(vendas_por_produto, key=vendas_por_produto.get)
            produto_mais_vendido = {
                'produto': next(
                    item.produto.nome 
                    for pedido in pedidos_entregues 
                    for item in pedido.itens 
                    if item.produto.id_produto == id_produto_top
                ),
                'quantidade_vendida': vendas_por_produto[id_produto_top]
            }
        
        return {
            'total_pedidos': total_pedidos,
            'pedidos_por_status': pedidos_por_status,
            'receita_total': receita_total,
            'receita_por_mes': receita_por_mes,
            'ticket_medio': ticket_medio,
            'cliente_mais_pedidos': cliente_mais_pedidos,
            'produto_mais_vendido': produto_mais_vendido
        }
    
    def gerar_relatorio_vendas(self, periodo_dias: int = 30) -> str:
        """Gera relatório de vendas dos últimos N dias"""
        data_limite = datetime.now() - timedelta(days=periodo_dias)
        pedidos_periodo = self.listar_pedidos_por_periodo(data_limite, datetime.now())
        pedidos_entregues = [p for p in pedidos_periodo if p.status == StatusPedido.ENTREGUE]
        
        if not pedidos_entregues:
            return f"Nenhuma venda nos últimos {periodo_dias} dias."
        
        relatorio = f"=== RELATÓRIO DE VENDAS - ÚLTIMOS {periodo_dias} DIAS ===\n\n"
        
        # Resumo geral
        total_vendas = len(pedidos_entregues)
        receita_total = sum(p.total for p in pedidos_entregues)
        ticket_medio = receita_total / total_vendas
        
        relatorio += f"RESUMO GERAL:\n"
        relatorio += f"Total de vendas: {total_vendas}\n"
        relatorio += f"Receita total: R$ {receita_total:.2f}\n"
        relatorio += f"Ticket médio: R$ {ticket_medio:.2f}\n\n"
        
        # Vendas por dia
        vendas_por_dia = {}
        for pedido in pedidos_entregues:
            data = pedido.data_pedido.strftime("%d/%m/%Y")
            if data not in vendas_por_dia:
                vendas_por_dia[data] = {'quantidade': 0, 'valor': 0}
            vendas_por_dia[data]['quantidade'] += 1
            vendas_por_dia[data]['valor'] += pedido.total
        
        relatorio += f"VENDAS POR DIA:\n"
        for data in sorted(vendas_por_dia.keys(), key=lambda x: datetime.strptime(x, "%d/%m/%Y"), reverse=True):
            info = vendas_por_dia[data]
            relatorio += f"{data}: {info['quantidade']} vendas - R$ {info['valor']:.2f}\n"
        
        relatorio += f"\n"
        
        # Produtos mais vendidos
        produtos_vendidos = {}
        for pedido in pedidos_entregues:
            for item in pedido.itens:
                nome = item.produto.nome
                if nome not in produtos_vendidos:
                    produtos_vendidos[nome] = {'quantidade': 0, 'receita': 0}
                produtos_vendidos[nome]['quantidade'] += item.quantidade
                produtos_vendidos[nome]['receita'] += item.subtotal
        
        relatorio += f"PRODUTOS MAIS VENDIDOS:\n"
        produtos_ordenados = sorted(
            produtos_vendidos.items(), 
            key=lambda x: x[1]['quantidade'], 
            reverse=True
        )
        
        for produto, info in produtos_ordenados[:10]:  # Top 10
            relatorio += f"- {produto}: {info['quantidade']} unidades - R$ {info['receita']:.2f}\n"
        
        return relatorio
    
    def formatar_pedido_para_exibicao(self, pedido: Pedido) -> str:
        """Formata dados do pedido para exibição"""
        relatorio = f"""
=== PEDIDO #{pedido.id_pedido} ===
Cliente: {pedido.cliente.nome} ({pedido.cliente.email})
Data: {pedido.data_pedido.strftime('%d/%m/%Y %H:%M')}
Status: {pedido.status.value.upper()}
"""
        
        if pedido.observacoes:
            relatorio += f"Observações: {pedido.observacoes}\n"
        
        relatorio += f"\nITENS:\n"
        
        if not pedido.itens:
            relatorio += "  Nenhum item adicionado\n"
        else:
            for item in pedido.itens:
                relatorio += f"  - {item.produto.nome}\n"
                relatorio += f"    Quantidade: {item.quantidade}\n"
                relatorio += f"    Preço unitário: R$ {item.preco_unitario:.2f}\n"
                relatorio += f"    Subtotal: R$ {item.subtotal:.2f}\n\n"
        
        relatorio += f"TOTAL: R$ {pedido.total:.2f}\n"
        
        return relatorio
    
    def cancelar_pedido(self, id_pedido: int, motivo: str = "") -> Tuple[bool, str]:
        """Cancela um pedido"""
        pedido = self.db.buscar_pedido(id_pedido)
        if not pedido:
            return False, f"Pedido {id_pedido} não encontrado"
        
        if pedido.status in [StatusPedido.ENTREGUE, StatusPedido.CANCELADO]:
            return False, f"Não é possível cancelar pedido com status {pedido.status.value}"
        
        # Adicionar motivo às observações
        if motivo:
            pedido.observacoes += f"\n[CANCELADO] {motivo}"
        
        return self.alterar_status_pedido(id_pedido, StatusPedido.CANCELADO)
