from datetime import datetime
from typing import List, Dict, Optional
import json
from enum import Enum

class StatusPedido(Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

class Cliente:
    def __init__(self, id_cliente: int, nome: str, email: str, telefone: str, endereco: str):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.data_cadastro = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'data_cadastro': self.data_cadastro.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        cliente = cls(
            data['id_cliente'],
            data['nome'],
            data['email'],
            data['telefone'],
            data['endereco']
        )
        cliente.data_cadastro = datetime.fromisoformat(data['data_cadastro'])
        return cliente

class Produto:
    def __init__(self, id_produto: int, nome: str, descricao: str, preco: float, estoque: int):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.ativo = True
    
    def to_dict(self) -> Dict:
        return {
            'id_produto': self.id_produto,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'estoque': self.estoque,
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        produto = cls(
            data['id_produto'],
            data['nome'],
            data['descricao'],
            data['preco'],
            data['estoque']
        )
        produto.ativo = data.get('ativo', True)
        return produto

class ItemPedido:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = produto.preco
        self.subtotal = self.preco_unitario * quantidade
    
    def to_dict(self) -> Dict:
        return {
            'produto': self.produto.to_dict(),
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        produto = Produto.from_dict(data['produto'])
        item = cls(produto, data['quantidade'])
        item.preco_unitario = data['preco_unitario']
        item.subtotal = data['subtotal']
        return item

class Pedido:
    def __init__(self, id_pedido: int, cliente: Cliente):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.itens: List[ItemPedido] = []
        self.data_pedido = datetime.now()
        self.status = StatusPedido.PENDENTE
        self.observacoes = ""
        self.total = 0.0
    
    def adicionar_item(self, produto: Produto, quantidade: int):
        if produto.estoque < quantidade:
            raise ValueError(f"Estoque insuficiente. Disponível: {produto.estoque}")
        
        # Verificar se o produto já existe no pedido
        for item in self.itens:
            if item.produto.id_produto == produto.id_produto:
                item.quantidade += quantidade
                item.subtotal = item.preco_unitario * item.quantidade
                self._calcular_total()
                return
        
        # Adicionar novo item
        item = ItemPedido(produto, quantidade)
        self.itens.append(item)
        self._calcular_total()
    
    def remover_item(self, id_produto: int):
        self.itens = [item for item in self.itens if item.produto.id_produto != id_produto]
        self._calcular_total()
    
    def _calcular_total(self):
        self.total = sum(item.subtotal for item in self.itens)
    
    def alterar_status(self, novo_status: StatusPedido):
        self.status = novo_status
    
    def to_dict(self) -> Dict:
        return {
            'id_pedido': self.id_pedido,
            'cliente': self.cliente.to_dict(),
            'itens': [item.to_dict() for item in self.itens],
            'data_pedido': self.data_pedido.isoformat(),
            'status': self.status.value,
            'observacoes': self.observacoes,
            'total': self.total
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        cliente = Cliente.from_dict(data['cliente'])
        pedido = cls(data['id_pedido'], cliente)
        pedido.itens = [ItemPedido.from_dict(item_data) for item_data in data['itens']]
        pedido.data_pedido = datetime.fromisoformat(data['data_pedido'])
        pedido.status = StatusPedido(data['status'])
        pedido.observacoes = data['observacoes']
        pedido.total = data['total']
        return pedido

class ItemCotacao:
    def __init__(self, produto: Produto, quantidade: int, preco_unitario: Optional[float] = None):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario if preco_unitario is not None else produto.preco
        self.subtotal = self.preco_unitario * quantidade
    
    def to_dict(self) -> Dict:
        return {
            'produto': self.produto.to_dict(),
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        produto = Produto.from_dict(data['produto'])
        item = cls(produto, data['quantidade'], data['preco_unitario'])
        item.subtotal = data['subtotal']
        return item

class Cotacao:
    def __init__(self, id_cotacao: int, id_cliente: int, data_cotacao: str, 
                 validade_dias: int = 30, desconto_percentual: float = 0.0, 
                 observacoes: str = ""):
        self.id_cotacao = id_cotacao
        self.id_cliente = id_cliente
        self.data_cotacao = data_cotacao
        self.validade_dias = validade_dias
        self.desconto_percentual = desconto_percentual
        self.observacoes = observacoes
        self.status = "Pendente"  # Pendente, Aprovada, Rejeitada, Expirada
        self.itens: List[ItemCotacao] = []
        self.subtotal = 0.0
        self.valor_desconto = 0.0
        self.total = 0.0
    
    def adicionar_item(self, produto: Produto, quantidade: int, preco_unitario: Optional[float] = None):
        """Adiciona item à cotação"""
        # Verificar se o produto já existe na cotação
        for item in self.itens:
            if item.produto.id_produto == produto.id_produto:
                item.quantidade += quantidade
                item.subtotal = item.preco_unitario * item.quantidade
                self._calcular_totais()
                return
        
        # Adicionar novo item
        item = ItemCotacao(produto, quantidade, preco_unitario)
        self.itens.append(item)
        self._calcular_totais()
    
    def remover_item(self, id_produto: int):
        """Remove item da cotação"""
        self.itens = [item for item in self.itens if item.produto.id_produto != id_produto]
        self._calcular_totais()
    
    def _calcular_totais(self):
        """Calcula subtotal, desconto e total"""
        self.subtotal = sum(item.subtotal for item in self.itens)
        self.valor_desconto = self.subtotal * (self.desconto_percentual / 100)
        self.total = self.subtotal - self.valor_desconto
    
    def alterar_desconto(self, novo_desconto_percentual: float):
        """Altera percentual de desconto"""
        self.desconto_percentual = novo_desconto_percentual
        self._calcular_totais()
    
    def to_dict(self) -> Dict:
        return {
            'id_cotacao': self.id_cotacao,
            'id_cliente': self.id_cliente,
            'data_cotacao': self.data_cotacao,
            'validade_dias': self.validade_dias,
            'desconto_percentual': self.desconto_percentual,
            'observacoes': self.observacoes,
            'status': self.status,
            'itens': [item.to_dict() for item in self.itens],
            'subtotal': self.subtotal,
            'valor_desconto': self.valor_desconto,
            'total': self.total
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        cotacao = cls(
            data['id_cotacao'],
            data['id_cliente'],
            data['data_cotacao'],
            data['validade_dias'],
            data['desconto_percentual'],
            data['observacoes']
        )
        cotacao.status = data['status']
        cotacao.itens = [ItemCotacao.from_dict(item_data) for item_data in data['itens']]
        cotacao.subtotal = data['subtotal']
        cotacao.valor_desconto = data['valor_desconto']
        cotacao.total = data['total']
        return cotacao
