import json
import os
from typing import List, Dict, Optional
from models import Cliente, Produto, Pedido, Cotacao

class Database:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.clientes_file = os.path.join(data_dir, "clientes.json")
        self.produtos_file = os.path.join(data_dir, "produtos.json")
        self.pedidos_file = os.path.join(data_dir, "pedidos.json")
        self.cotacoes_file = os.path.join(data_dir, "cotacoes.json")
        self.contadores_file = os.path.join(data_dir, "contadores.json")
        
        # Criar diretório se não existir
        os.makedirs(data_dir, exist_ok=True)
        
        # Inicializar arquivos se não existirem
        self._inicializar_arquivos()
    
    def _inicializar_arquivos(self):
        arquivos_iniciais = {
            self.clientes_file: [],
            self.produtos_file: [],
            self.pedidos_file: [],
            self.cotacoes_file: [],
            self.contadores_file: {"cliente": 1, "produto": 1, "pedido": 1, "cotacao": 1}
        }
        
        for arquivo, conteudo_inicial in arquivos_iniciais.items():
            if not os.path.exists(arquivo):
                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump(conteudo_inicial, f, ensure_ascii=False, indent=2)
    
    def _carregar_json(self, arquivo: str) -> List[Dict] | Dict:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return [] if arquivo != self.contadores_file else {"cliente": 1, "produto": 1, "pedido": 1, "cotacao": 1}
    
    def _salvar_json(self, arquivo: str, dados):
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    def obter_proximo_id(self, tipo: str) -> int:
        contadores = self._carregar_json(self.contadores_file)
        proximo_id = contadores.get(tipo, 1)
        contadores[tipo] = proximo_id + 1
        self._salvar_json(self.contadores_file, contadores)
        return proximo_id
    
    # Métodos para Clientes
    def salvar_cliente(self, cliente: Cliente):
        clientes_data = self._carregar_json(self.clientes_file)
        
        # Verificar se já existe (atualizar) ou adicionar novo
        for i, cliente_data in enumerate(clientes_data):
            if cliente_data['id_cliente'] == cliente.id_cliente:
                clientes_data[i] = cliente.to_dict()
                break
        else:
            clientes_data.append(cliente.to_dict())
        
        self._salvar_json(self.clientes_file, clientes_data)
    
    def carregar_clientes(self) -> List[Cliente]:
        clientes_data = self._carregar_json(self.clientes_file)
        return [Cliente.from_dict(data) for data in clientes_data]
    
    def buscar_cliente(self, id_cliente: int) -> Optional[Cliente]:
        clientes = self.carregar_clientes()
        for cliente in clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        return None
    
    def remover_cliente(self, id_cliente: int) -> bool:
        clientes_data = self._carregar_json(self.clientes_file)
        clientes_filtrados = [c for c in clientes_data if c['id_cliente'] != id_cliente]
        
        if len(clientes_filtrados) < len(clientes_data):
            self._salvar_json(self.clientes_file, clientes_filtrados)
            return True
        return False
    
    # Métodos para Produtos
    def salvar_produto(self, produto: Produto):
        produtos_data = self._carregar_json(self.produtos_file)
        
        for i, produto_data in enumerate(produtos_data):
            if produto_data['id_produto'] == produto.id_produto:
                produtos_data[i] = produto.to_dict()
                break
        else:
            produtos_data.append(produto.to_dict())
        
        self._salvar_json(self.produtos_file, produtos_data)
    
    def carregar_produtos(self) -> List[Produto]:
        produtos_data = self._carregar_json(self.produtos_file)
        return [Produto.from_dict(data) for data in produtos_data]
    
    def buscar_produto(self, id_produto: int) -> Optional[Produto]:
        produtos = self.carregar_produtos()
        for produto in produtos:
            if produto.id_produto == id_produto:
                return produto
        return None
    
    def remover_produto(self, id_produto: int) -> bool:
        produtos_data = self._carregar_json(self.produtos_file)
        produtos_filtrados = [p for p in produtos_data if p['id_produto'] != id_produto]
        
        if len(produtos_filtrados) < len(produtos_data):
            self._salvar_json(self.produtos_file, produtos_filtrados)
            return True
        return False
    
    # Métodos para Pedidos
    def salvar_pedido(self, pedido: Pedido):
        pedidos_data = self._carregar_json(self.pedidos_file)
        
        for i, pedido_data in enumerate(pedidos_data):
            if pedido_data['id_pedido'] == pedido.id_pedido:
                pedidos_data[i] = pedido.to_dict()
                break
        else:
            pedidos_data.append(pedido.to_dict())
        
        self._salvar_json(self.pedidos_file, pedidos_data)
    
    def carregar_pedidos(self) -> List[Pedido]:
        pedidos_data = self._carregar_json(self.pedidos_file)
        return [Pedido.from_dict(data) for data in pedidos_data]
    
    def buscar_pedido(self, id_pedido: int) -> Optional[Pedido]:
        pedidos = self.carregar_pedidos()
        for pedido in pedidos:
            if pedido.id_pedido == id_pedido:
                return pedido
        return None
    
    def remover_pedido(self, id_pedido: int) -> bool:
        pedidos_data = self._carregar_json(self.pedidos_file)
        pedidos_filtrados = [p for p in pedidos_data if p['id_pedido'] != id_pedido]
        
        if len(pedidos_filtrados) < len(pedidos_data):
            self._salvar_json(self.pedidos_file, pedidos_filtrados)
            return True
        return False
    
    # Métodos para Cotações
    def salvar_cotacao(self, cotacao: Cotacao):
        cotacoes_data = self._carregar_json(self.cotacoes_file)
        
        for i, cotacao_data in enumerate(cotacoes_data):
            if cotacao_data['id_cotacao'] == cotacao.id_cotacao:
                cotacoes_data[i] = cotacao.to_dict()
                break
        else:
            cotacoes_data.append(cotacao.to_dict())
        
        self._salvar_json(self.cotacoes_file, cotacoes_data)
    
    def carregar_cotacoes(self) -> List[Cotacao]:
        cotacoes_data = self._carregar_json(self.cotacoes_file)
        return [Cotacao.from_dict(data) for data in cotacoes_data]
    
    def buscar_cotacao(self, id_cotacao: int) -> Optional[Cotacao]:
        cotacoes = self.carregar_cotacoes()
        for cotacao in cotacoes:
            if cotacao.id_cotacao == id_cotacao:
                return cotacao
        return None
    
    def remover_cotacao(self, id_cotacao: int) -> bool:
        cotacoes_data = self._carregar_json(self.cotacoes_file)
        cotacoes_filtradas = [c for c in cotacoes_data if c['id_cotacao'] != id_cotacao]
        
        if len(cotacoes_filtradas) < len(cotacoes_data):
            self._salvar_json(self.cotacoes_file, cotacoes_filtradas)
            return True
        return False
