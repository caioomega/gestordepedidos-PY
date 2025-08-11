from typing import List, Optional, Tuple
from models import Produto
from database import Database

class ProdutoManager:
    def __init__(self, database: Database):
        self.db = database
    
    def _validar_dados_produto(self, nome: str, descricao: str, preco: float, estoque: int) -> List[str]:
        """Valida todos os dados do produto e retorna lista de erros"""
        erros = []
        
        if not nome or len(nome.strip()) < 2:
            erros.append("Nome deve ter pelo menos 2 caracteres")
        
        if not descricao or len(descricao.strip()) < 5:
            erros.append("Descrição deve ter pelo menos 5 caracteres")
        
        if preco <= 0:
            erros.append("Preço deve ser maior que zero")
        
        if estoque < 0:
            erros.append("Estoque não pode ser negativo")
        
        return erros
    
    def _nome_ja_existe(self, nome: str, id_produto_atual: Optional[int] = None) -> bool:
        """Verifica se nome do produto já está cadastrado"""
        produtos = self.db.carregar_produtos()
        for produto in produtos:
            if produto.nome.lower() == nome.lower().strip() and produto.id_produto != id_produto_atual:
                return True
        return False
    
    def criar_produto(self, nome: str, descricao: str, preco: float, estoque: int) -> Tuple[bool, str, Optional[Produto]]:
        """
        Cria um novo produto
        Retorna: (sucesso, mensagem, produto_criado)
        """
        # Validar dados
        erros = self._validar_dados_produto(nome, descricao, preco, estoque)
        if erros:
            return False, "Erros de validação: " + "; ".join(erros), None
        
        # Verificar nome único
        if self._nome_ja_existe(nome):
            return False, "Produto com este nome já cadastrado no sistema", None
        
        # Criar produto
        id_produto = self.db.obter_proximo_id("produto")
        produto = Produto(id_produto, nome.strip(), descricao.strip(), preco, estoque)
        
        # Salvar no banco
        self.db.salvar_produto(produto)
        
        return True, f"Produto {nome} cadastrado com sucesso (ID: {id_produto})", produto
    
    def atualizar_produto(self, id_produto: int, nome: str, descricao: str, preco: float, estoque: int) -> Tuple[bool, str]:
        """
        Atualiza dados de um produto existente
        Retorna: (sucesso, mensagem)
        """
        # Verificar se produto existe
        produto_existente = self.db.buscar_produto(id_produto)
        if not produto_existente:
            return False, f"Produto com ID {id_produto} não encontrado"
        
        # Validar dados
        erros = self._validar_dados_produto(nome, descricao, preco, estoque)
        if erros:
            return False, "Erros de validação: " + "; ".join(erros)
        
        # Verificar nome único (exceto para o próprio produto)
        if self._nome_ja_existe(nome, id_produto):
            return False, "Produto com este nome já cadastrado"
        
        # Atualizar dados
        produto_existente.nome = nome.strip()
        produto_existente.descricao = descricao.strip()
        produto_existente.preco = preco
        produto_existente.estoque = estoque
        
        # Salvar no banco
        self.db.salvar_produto(produto_existente)
        
        return True, f"Produto {nome} atualizado com sucesso"
    
    def buscar_produto_por_id(self, id_produto: int) -> Optional[Produto]:
        """Busca produto por ID"""
        return self.db.buscar_produto(id_produto)
    
    def buscar_produtos_por_nome(self, nome: str) -> List[Produto]:
        """Busca produtos por nome (busca parcial, case-insensitive)"""
        produtos = self.db.carregar_produtos()
        nome_busca = nome.lower().strip()
        
        return [
            produto for produto in produtos 
            if nome_busca in produto.nome.lower()
        ]
    
    def listar_todos_produtos(self, apenas_ativos: bool = True) -> List[Produto]:
        """Lista todos os produtos ordenados por nome"""
        produtos = self.db.carregar_produtos()
        
        if apenas_ativos:
            produtos = [p for p in produtos if p.ativo]
        
        return sorted(produtos, key=lambda p: p.nome.lower())
    
    def listar_produtos_com_estoque_baixo(self, limite_estoque: int = 5) -> List[Produto]:
        """Lista produtos com estoque abaixo do limite especificado"""
        produtos = self.db.carregar_produtos()
        return [
            produto for produto in produtos 
            if produto.ativo and produto.estoque <= limite_estoque
        ]
    
    def listar_produtos_sem_estoque(self) -> List[Produto]:
        """Lista produtos sem estoque"""
        produtos = self.db.carregar_produtos()
        return [
            produto for produto in produtos 
            if produto.ativo and produto.estoque == 0
        ]
    
    def ativar_produto(self, id_produto: int) -> Tuple[bool, str]:
        """Ativa um produto"""
        produto = self.db.buscar_produto(id_produto)
        if not produto:
            return False, f"Produto com ID {id_produto} não encontrado"
        
        if produto.ativo:
            return False, f"Produto {produto.nome} já está ativo"
        
        produto.ativo = True
        self.db.salvar_produto(produto)
        
        return True, f"Produto {produto.nome} ativado com sucesso"
    
    def desativar_produto(self, id_produto: int) -> Tuple[bool, str]:
        """Desativa um produto (não permite mais vendas)"""
        produto = self.db.buscar_produto(id_produto)
        if not produto:
            return False, f"Produto com ID {id_produto} não encontrado"
        
        if not produto.ativo:
            return False, f"Produto {produto.nome} já está desativado"
        
        produto.ativo = False
        self.db.salvar_produto(produto)
        
        return True, f"Produto {produto.nome} desativado com sucesso"
    
    def ajustar_estoque(self, id_produto: int, quantidade: int, operacao: str = "adicionar") -> Tuple[bool, str]:
        """
        Ajusta estoque do produto
        operacao: 'adicionar', 'remover', 'definir'
        """
        produto = self.db.buscar_produto(id_produto)
        if not produto:
            return False, f"Produto com ID {id_produto} não encontrado"
        
        estoque_anterior = produto.estoque
        
        if operacao == "adicionar":
            produto.estoque += quantidade
        elif operacao == "remover":
            if produto.estoque < quantidade:
                return False, f"Estoque insuficiente. Disponível: {produto.estoque}, Solicitado: {quantidade}"
            produto.estoque -= quantidade
        elif operacao == "definir":
            if quantidade < 0:
                return False, "Estoque não pode ser negativo"
            produto.estoque = quantidade
        else:
            return False, "Operação inválida. Use: 'adicionar', 'remover' ou 'definir'"
        
        self.db.salvar_produto(produto)
        
        return True, f"Estoque do produto {produto.nome} ajustado de {estoque_anterior} para {produto.estoque}"
    
    def remover_produto(self, id_produto: int) -> Tuple[bool, str]:
        """
        Remove um produto (verifica se não está em pedidos)
        Retorna: (sucesso, mensagem)
        """
        # Verificar se produto existe
        produto = self.db.buscar_produto(id_produto)
        if not produto:
            return False, f"Produto com ID {id_produto} não encontrado"
        
        # Verificar se está em pedidos
        pedidos = self.db.carregar_pedidos()
        produto_em_pedidos = False
        
        for pedido in pedidos:
            for item in pedido.itens:
                if item.produto.id_produto == id_produto:
                    produto_em_pedidos = True
                    break
            if produto_em_pedidos:
                break
        
        if produto_em_pedidos:
            return False, f"Não é possível remover produto {produto.nome}. Existem pedidos associados"
        
        # Remover produto
        if self.db.remover_produto(id_produto):
            return True, f"Produto {produto.nome} removido com sucesso"
        else:
            return False, "Erro ao remover produto"
    
    def obter_estatisticas_produtos(self) -> dict:
        """Retorna estatísticas dos produtos"""
        produtos = self.db.carregar_produtos()
        pedidos = self.db.carregar_pedidos()
        
        # Estatísticas básicas
        produtos_ativos = [p for p in produtos if p.ativo]
        produtos_inativos = [p for p in produtos if not p.ativo]
        produtos_sem_estoque = [p for p in produtos_ativos if p.estoque == 0]
        produtos_estoque_baixo = [p for p in produtos_ativos if 0 < p.estoque <= 5]
        
        # Valor total do estoque
        valor_total_estoque = sum(p.preco * p.estoque for p in produtos_ativos)
        
        # Produto mais vendido
        vendas_por_produto = {}
        for pedido in pedidos:
            for item in pedido.itens:
                id_produto = item.produto.id_produto
                vendas_por_produto[id_produto] = vendas_por_produto.get(id_produto, 0) + item.quantidade
        
        produto_mais_vendido = None
        max_vendas = 0
        
        if vendas_por_produto:
            id_mais_vendido = max(vendas_por_produto, key=vendas_por_produto.get)
            max_vendas = vendas_por_produto[id_mais_vendido]
            produto_mais_vendido = self.db.buscar_produto(id_mais_vendido)
        
        # Produto mais caro e mais barato
        produto_mais_caro = max(produtos_ativos, key=lambda p: p.preco) if produtos_ativos else None
        produto_mais_barato = min(produtos_ativos, key=lambda p: p.preco) if produtos_ativos else None
        
        return {
            'total_produtos': len(produtos),
            'produtos_ativos': len(produtos_ativos),
            'produtos_inativos': len(produtos_inativos),
            'produtos_sem_estoque': len(produtos_sem_estoque),
            'produtos_estoque_baixo': len(produtos_estoque_baixo),
            'valor_total_estoque': valor_total_estoque,
            'produto_mais_vendido': {
                'produto': produto_mais_vendido.nome if produto_mais_vendido else None,
                'quantidade_vendida': max_vendas
            },
            'produto_mais_caro': {
                'produto': produto_mais_caro.nome if produto_mais_caro else None,
                'preco': produto_mais_caro.preco if produto_mais_caro else 0
            },
            'produto_mais_barato': {
                'produto': produto_mais_barato.nome if produto_mais_barato else None,
                'preco': produto_mais_barato.preco if produto_mais_barato else 0
            }
        }
    
    def formatar_produto_para_exibicao(self, produto: Produto) -> str:
        """Formata dados do produto para exibição"""
        status = "ATIVO" if produto.ativo else "INATIVO"
        status_estoque = ""
        
        if produto.estoque == 0:
            status_estoque = " [SEM ESTOQUE]"
        elif produto.estoque <= 5:
            status_estoque = " [ESTOQUE BAIXO]"
        
        return f"""
ID: {produto.id_produto}
Nome: {produto.nome}
Descrição: {produto.descricao}
Preço: R$ {produto.preco:.2f}
Estoque: {produto.estoque} unidades{status_estoque}
Status: {status}
"""
    
    def gerar_relatorio_estoque(self) -> str:
        """Gera relatório completo de estoque"""
        produtos = self.listar_todos_produtos(apenas_ativos=True)
        
        if not produtos:
            return "Nenhum produto ativo cadastrado."
        
        relatorio = "=== RELATÓRIO DE ESTOQUE ===\n\n"
        
        # Produtos com estoque normal
        produtos_ok = [p for p in produtos if p.estoque > 5]
        if produtos_ok:
            relatorio += "PRODUTOS COM ESTOQUE ADEQUADO:\n"
            for produto in produtos_ok:
                relatorio += f"- {produto.nome}: {produto.estoque} unidades (R$ {produto.preco:.2f})\n"
            relatorio += "\n"
        
        # Produtos com estoque baixo
        produtos_baixo = [p for p in produtos if 0 < p.estoque <= 5]
        if produtos_baixo:
            relatorio += "⚠️  PRODUTOS COM ESTOQUE BAIXO:\n"
            for produto in produtos_baixo:
                relatorio += f"- {produto.nome}: {produto.estoque} unidades (R$ {produto.preco:.2f})\n"
            relatorio += "\n"
        
        # Produtos sem estoque
        produtos_sem = [p for p in produtos if p.estoque == 0]
        if produtos_sem:
            relatorio += "🚨 PRODUTOS SEM ESTOQUE:\n"
            for produto in produtos_sem:
                relatorio += f"- {produto.nome}: R$ {produto.preco:.2f}\n"
            relatorio += "\n"
        
        # Resumo
        valor_total = sum(p.preco * p.estoque for p in produtos)
        relatorio += f"RESUMO:\n"
        relatorio += f"Total de produtos ativos: {len(produtos)}\n"
        relatorio += f"Produtos com estoque adequado: {len(produtos_ok)}\n"
        relatorio += f"Produtos com estoque baixo: {len(produtos_baixo)}\n"
        relatorio += f"Produtos sem estoque: {len(produtos_sem)}\n"
        relatorio += f"Valor total do estoque: R$ {valor_total:.2f}\n"
        
        return relatorio
