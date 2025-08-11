import re
from typing import List, Optional
from models import Cliente
from database import Database

class ClienteManager:
    def __init__(self, database: Database):
        self.db = database
    
    def _validar_email(self, email: str) -> bool:
        """Valida formato do email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None
    
    def _validar_telefone(self, telefone: str) -> bool:
        """Valida formato do telefone (aceita vários formatos brasileiros)"""
        # Remove caracteres não numéricos
        telefone_limpo = re.sub(r'[^\d]', '', telefone)
        # Aceita telefones com 10 ou 11 dígitos
        return len(telefone_limpo) in [10, 11]
    
    def _validar_dados_cliente(self, nome: str, email: str, telefone: str, endereco: str) -> List[str]:
        """Valida todos os dados do cliente e retorna lista de erros"""
        erros = []
        
        if not nome or len(nome.strip()) < 2:
            erros.append("Nome deve ter pelo menos 2 caracteres")
        
        if not email or not self._validar_email(email):
            erros.append("Email deve ter formato válido")
        
        if not telefone or not self._validar_telefone(telefone):
            erros.append("Telefone deve ter formato válido (10 ou 11 dígitos)")
        
        if not endereco or len(endereco.strip()) < 5:
            erros.append("Endereço deve ter pelo menos 5 caracteres")
        
        return erros
    
    def _email_ja_existe(self, email: str, id_cliente_atual: Optional[int] = None) -> bool:
        """Verifica se email já está cadastrado"""
        clientes = self.db.carregar_clientes()
        for cliente in clientes:
            if cliente.email.lower() == email.lower() and cliente.id_cliente != id_cliente_atual:
                return True
        return False
    
    def criar_cliente(self, nome: str, email: str, telefone: str, endereco: str) -> tuple[bool, str, Optional[Cliente]]:
        """
        Cria um novo cliente
        Retorna: (sucesso, mensagem, cliente_criado)
        """
        # Validar dados
        erros = self._validar_dados_cliente(nome, email, telefone, endereco)
        if erros:
            return False, "Erros de validação: " + "; ".join(erros), None
        
        # Verificar email único
        if self._email_ja_existe(email):
            return False, "Email já cadastrado no sistema", None
        
        # Criar cliente
        id_cliente = self.db.obter_proximo_id("cliente")
        cliente = Cliente(id_cliente, nome.strip(), email.lower(), telefone, endereco.strip())
        
        # Salvar no banco
        self.db.salvar_cliente(cliente)
        
        return True, f"Cliente {nome} cadastrado com sucesso (ID: {id_cliente})", cliente
    
    def atualizar_cliente(self, id_cliente: int, nome: str, email: str, telefone: str, endereco: str) -> tuple[bool, str]:
        """
        Atualiza dados de um cliente existente
        Retorna: (sucesso, mensagem)
        """
        # Verificar se cliente existe
        cliente_existente = self.db.buscar_cliente(id_cliente)
        if not cliente_existente:
            return False, f"Cliente com ID {id_cliente} não encontrado"
        
        # Validar dados
        erros = self._validar_dados_cliente(nome, email, telefone, endereco)
        if erros:
            return False, "Erros de validação: " + "; ".join(erros)
        
        # Verificar email único (exceto para o próprio cliente)
        if self._email_ja_existe(email, id_cliente):
            return False, "Email já cadastrado para outro cliente"
        
        # Atualizar dados
        cliente_existente.nome = nome.strip()
        cliente_existente.email = email.lower()
        cliente_existente.telefone = telefone
        cliente_existente.endereco = endereco.strip()
        
        # Salvar no banco
        self.db.salvar_cliente(cliente_existente)
        
        return True, f"Cliente {nome} atualizado com sucesso"
    
    def buscar_cliente_por_id(self, id_cliente: int) -> Optional[Cliente]:
        """Busca cliente por ID"""
        return self.db.buscar_cliente(id_cliente)
    
    def buscar_clientes_por_nome(self, nome: str) -> List[Cliente]:
        """Busca clientes por nome (busca parcial, case-insensitive)"""
        clientes = self.db.carregar_clientes()
        nome_busca = nome.lower().strip()
        
        return [
            cliente for cliente in clientes 
            if nome_busca in cliente.nome.lower()
        ]
    
    def buscar_cliente_por_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        clientes = self.db.carregar_clientes()
        email_busca = email.lower().strip()
        
        for cliente in clientes:
            if cliente.email.lower() == email_busca:
                return cliente
        return None
    
    def listar_todos_clientes(self) -> List[Cliente]:
        """Lista todos os clientes ordenados por nome"""
        clientes = self.db.carregar_clientes()
        return sorted(clientes, key=lambda c: c.nome.lower())
    
    def remover_cliente(self, id_cliente: int) -> tuple[bool, str]:
        """
        Remove um cliente (verifica se não tem pedidos associados)
        Retorna: (sucesso, mensagem)
        """
        # Verificar se cliente existe
        cliente = self.db.buscar_cliente(id_cliente)
        if not cliente:
            return False, f"Cliente com ID {id_cliente} não encontrado"
        
        # Verificar se tem pedidos associados
        pedidos = self.db.carregar_pedidos()
        pedidos_cliente = [p for p in pedidos if p.cliente.id_cliente == id_cliente]
        
        if pedidos_cliente:
            return False, f"Não é possível remover cliente {cliente.nome}. Existem {len(pedidos_cliente)} pedidos associados"
        
        # Remover cliente
        if self.db.remover_cliente(id_cliente):
            return True, f"Cliente {cliente.nome} removido com sucesso"
        else:
            return False, "Erro ao remover cliente"
    
    def obter_estatisticas_clientes(self) -> dict:
        """Retorna estatísticas dos clientes"""
        clientes = self.db.carregar_clientes()
        pedidos = self.db.carregar_pedidos()
        
        # Contar pedidos por cliente
        pedidos_por_cliente = {}
        valor_total_por_cliente = {}
        
        for pedido in pedidos:
            id_cliente = pedido.cliente.id_cliente
            pedidos_por_cliente[id_cliente] = pedidos_por_cliente.get(id_cliente, 0) + 1
            valor_total_por_cliente[id_cliente] = valor_total_por_cliente.get(id_cliente, 0) + pedido.total
        
        # Encontrar cliente com mais pedidos
        cliente_mais_pedidos = None
        max_pedidos = 0
        
        for cliente in clientes:
            num_pedidos = pedidos_por_cliente.get(cliente.id_cliente, 0)
            if num_pedidos > max_pedidos:
                max_pedidos = num_pedidos
                cliente_mais_pedidos = cliente
        
        # Encontrar cliente com maior valor total
        cliente_maior_valor = None
        max_valor = 0
        
        for cliente in clientes:
            valor_total = valor_total_por_cliente.get(cliente.id_cliente, 0)
            if valor_total > max_valor:
                max_valor = valor_total
                cliente_maior_valor = cliente
        
        return {
            'total_clientes': len(clientes),
            'clientes_com_pedidos': len([c for c in clientes if c.id_cliente in pedidos_por_cliente]),
            'clientes_sem_pedidos': len([c for c in clientes if c.id_cliente not in pedidos_por_cliente]),
            'cliente_mais_pedidos': {
                'cliente': cliente_mais_pedidos.nome if cliente_mais_pedidos else None,
                'quantidade_pedidos': max_pedidos
            },
            'cliente_maior_valor': {
                'cliente': cliente_maior_valor.nome if cliente_maior_valor else None,
                'valor_total': max_valor
            }
        }
    
    def formatar_cliente_para_exibicao(self, cliente: Cliente) -> str:
        """Formata dados do cliente para exibição"""
        return f"""
ID: {cliente.id_cliente}
Nome: {cliente.nome}
Email: {cliente.email}
Telefone: {cliente.telefone}
Endereço: {cliente.endereco}
Data de Cadastro: {cliente.data_cadastro.strftime('%d/%m/%Y %H:%M')}
"""
