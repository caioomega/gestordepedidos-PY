import os
from datetime import datetime, timedelta
from typing import Optional
from database import Database
from cliente_manager import ClienteManager
from produto_manager import ProdutoManager
from pedido_manager import PedidoManager
from models import StatusPedido

class InterfaceUsuario:
    def __init__(self):
        self.db = Database("data")
        self.cliente_manager = ClienteManager(self.db)
        self.produto_manager = ProdutoManager(self.db)
        self.pedido_manager = PedidoManager(self.db)
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausar(self):
        """Pausa a execução até o usuário pressionar Enter"""
        input("\nPressione Enter para continuar...")
    
    def obter_entrada_numerica(self, prompt: str, minimo: Optional[int] = None, maximo: Optional[int] = None) -> Optional[int]:
        """Obtém entrada numérica do usuário com validação"""
        while True:
            try:
                entrada = input(prompt).strip()
                if not entrada:
                    return None
                
                numero = int(entrada)
                
                if minimo is not None and numero < minimo:
                    print(f"Valor deve ser maior ou igual a {minimo}")
                    continue
                
                if maximo is not None and numero > maximo:
                    print(f"Valor deve ser menor ou igual a {maximo}")
                    continue
                
                return numero
            
            except ValueError:
                print("Por favor, digite um número válido")
    
    def obter_entrada_decimal(self, prompt: str, minimo: Optional[float] = None) -> Optional[float]:
        """Obtém entrada decimal do usuário com validação"""
        while True:
            try:
                entrada = input(prompt).strip()
                if not entrada:
                    return None
                
                numero = float(entrada)
                
                if minimo is not None and numero < minimo:
                    print(f"Valor deve ser maior ou igual a {minimo}")
                    continue
                
                return numero
            
            except ValueError:
                print("Por favor, digite um número válido")
    
    def exibir_menu_principal(self):
        """Exibe o menu principal do sistema"""
        print("=" * 50)
        print("    SISTEMA DE GESTÃO DE PEDIDOS")
        print("=" * 50)
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Produtos")
        print("3. Gerenciar Pedidos")
        print("4. Relatórios")
        print("5. Estatísticas")
        print("0. Sair")
        print("=" * 50)
    
    def menu_clientes(self):
        """Menu de gerenciamento de clientes"""
        while True:
            self.limpar_tela()
            print("=" * 40)
            print("    GERENCIAR CLIENTES")
            print("=" * 40)
            print("1. Cadastrar Cliente")
            print("2. Listar Clientes")
            print("3. Buscar Cliente")
            print("4. Atualizar Cliente")
            print("5. Remover Cliente")
            print("6. Estatísticas de Clientes")
            print("0. Voltar")
            print("=" * 40)
            
            opcao = self.obter_entrada_numerica("Escolha uma opção: ", 0, 6)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_cliente()
            elif opcao == 2:
                self.listar_clientes()
            elif opcao == 3:
                self.buscar_cliente()
            elif opcao == 4:
                self.atualizar_cliente()
            elif opcao == 5:
                self.remover_cliente()
            elif opcao == 6:
                self.estatisticas_clientes()
    
    def cadastrar_cliente(self):
        """Cadastra um novo cliente"""
        self.limpar_tela()
        print("=== CADASTRAR CLIENTE ===\n")
        
        nome = input("Nome: ").strip()
        if not nome:
            print("Nome é obrigatório!")
            self.pausar()
            return
        
        email = input("Email: ").strip()
        if not email:
            print("Email é obrigatório!")
            self.pausar()
            return
        
        telefone = input("Telefone: ").strip()
        if not telefone:
            print("Telefone é obrigatório!")
            self.pausar()
            return
        
        endereco = input("Endereço: ").strip()
        if not endereco:
            print("Endereço é obrigatório!")
            self.pausar()
            return
        
        sucesso, mensagem, cliente = self.cliente_manager.criar_cliente(nome, email, telefone, endereco)
        
        print(f"\n{mensagem}")
        
        if sucesso and cliente:
            print(self.cliente_manager.formatar_cliente_para_exibicao(cliente))
        
        self.pausar()
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        self.limpar_tela()
        print("=== LISTA DE CLIENTES ===\n")
        
        clientes = self.cliente_manager.listar_todos_clientes()
        
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            print(f"Total de clientes: {len(clientes)}\n")
            for cliente in clientes:
                print(f"ID: {cliente.id_cliente} | {cliente.nome} | {cliente.email} | {cliente.telefone}")
        
        self.pausar()
    
    def buscar_cliente(self):
        """Busca cliente por ID ou nome"""
        self.limpar_tela()
        print("=== BUSCAR CLIENTE ===\n")
        print("1. Buscar por ID")
        print("2. Buscar por nome")
        print("3. Buscar por email")
        
        opcao = self.obter_entrada_numerica("Escolha uma opção: ", 1, 3)
        
        if opcao == 1:
            id_cliente = self.obter_entrada_numerica("ID do cliente: ", 1)
            if id_cliente:
                cliente = self.cliente_manager.buscar_cliente_por_id(id_cliente)
                if cliente:
                    print(self.cliente_manager.formatar_cliente_para_exibicao(cliente))
                else:
                    print("Cliente não encontrado.")
        
        elif opcao == 2:
            nome = input("Nome (ou parte do nome): ").strip()
            if nome:
                clientes = self.cliente_manager.buscar_clientes_por_nome(nome)
                if clientes:
                    print(f"\nEncontrados {len(clientes)} cliente(s):\n")
                    for cliente in clientes:
                        print(f"ID: {cliente.id_cliente} | {cliente.nome} | {cliente.email}")
                else:
                    print("Nenhum cliente encontrado.")
        
        elif opcao == 3:
            email = input("Email: ").strip()
            if email:
                cliente = self.cliente_manager.buscar_cliente_por_email(email)
                if cliente:
                    print(self.cliente_manager.formatar_cliente_para_exibicao(cliente))
                else:
                    print("Cliente não encontrado.")
        
        self.pausar()
    
    def atualizar_cliente(self):
        """Atualiza dados de um cliente"""
        self.limpar_tela()
        print("=== ATUALIZAR CLIENTE ===\n")
        
        id_cliente = self.obter_entrada_numerica("ID do cliente: ", 1)
        if not id_cliente:
            return
        
        cliente = self.cliente_manager.buscar_cliente_por_id(id_cliente)
        if not cliente:
            print("Cliente não encontrado.")
            self.pausar()
            return
        
        print("Dados atuais:")
        print(self.cliente_manager.formatar_cliente_para_exibicao(cliente))
        
        print("Digite os novos dados (Enter para manter o atual):")
        
        nome = input(f"Nome [{cliente.nome}]: ").strip() or cliente.nome
        email = input(f"Email [{cliente.email}]: ").strip() or cliente.email
        telefone = input(f"Telefone [{cliente.telefone}]: ").strip() or cliente.telefone
        endereco = input(f"Endereço [{cliente.endereco}]: ").strip() or cliente.endereco
        
        sucesso, mensagem = self.cliente_manager.atualizar_cliente(id_cliente, nome, email, telefone, endereco)
        print(f"\n{mensagem}")
        
        self.pausar()
    
    def remover_cliente(self):
        """Remove um cliente"""
        self.limpar_tela()
        print("=== REMOVER CLIENTE ===\n")
        
        id_cliente = self.obter_entrada_numerica("ID do cliente: ", 1)
        if not id_cliente:
            return
        
        cliente = self.cliente_manager.buscar_cliente_por_id(id_cliente)
        if not cliente:
            print("Cliente não encontrado.")
            self.pausar()
            return
        
        print("Cliente a ser removido:")
        print(self.cliente_manager.formatar_cliente_para_exibicao(cliente))
        
        confirmacao = input("Confirma a remoção? (s/N): ").strip().lower()
        
        if confirmacao == 's':
            sucesso, mensagem = self.cliente_manager.remover_cliente(id_cliente)
            print(f"\n{mensagem}")
        else:
            print("Remoção cancelada.")
        
        self.pausar()
    
    def estatisticas_clientes(self):
        """Exibe estatísticas dos clientes"""
        self.limpar_tela()
        print("=== ESTATÍSTICAS DE CLIENTES ===\n")
        
        stats = self.cliente_manager.obter_estatisticas_clientes()
        
        print(f"Total de clientes: {stats['total_clientes']}")
        print(f"Clientes com pedidos: {stats['clientes_com_pedidos']}")
        print(f"Clientes sem pedidos: {stats['clientes_sem_pedidos']}")
        
        if stats['cliente_mais_pedidos']['cliente']:
            print(f"Cliente com mais pedidos: {stats['cliente_mais_pedidos']['cliente']} ({stats['cliente_mais_pedidos']['quantidade_pedidos']} pedidos)")
        
        if stats['cliente_maior_valor']['cliente']:
            print(f"Cliente com maior valor total: {stats['cliente_maior_valor']['cliente']} (R$ {stats['cliente_maior_valor']['valor_total']:.2f})")
        
        self.pausar()
    
    def menu_produtos(self):
        """Menu de gerenciamento de produtos"""
        while True:
            self.limpar_tela()
            print("=" * 40)
            print("    GERENCIAR PRODUTOS")
            print("=" * 40)
            print("1. Cadastrar Produto")
            print("2. Listar Produtos")
            print("3. Buscar Produto")
            print("4. Atualizar Produto")
            print("5. Ajustar Estoque")
            print("6. Ativar/Desativar Produto")
            print("7. Relatório de Estoque")
            print("8. Estatísticas de Produtos")
            print("0. Voltar")
            print("=" * 40)
            
            opcao = self.obter_entrada_numerica("Escolha uma opção: ", 0, 8)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.cadastrar_produto()
            elif opcao == 2:
                self.listar_produtos()
            elif opcao == 3:
                self.buscar_produto()
            elif opcao == 4:
                self.atualizar_produto()
            elif opcao == 5:
                self.ajustar_estoque()
            elif opcao == 6:
                self.ativar_desativar_produto()
            elif opcao == 7:
                self.relatorio_estoque()
            elif opcao == 8:
                self.estatisticas_produtos()
    
    def cadastrar_produto(self):
        """Cadastra um novo produto"""
        self.limpar_tela()
        print("=== CADASTRAR PRODUTO ===\n")
        
        nome = input("Nome: ").strip()
        if not nome:
            print("Nome é obrigatório!")
            self.pausar()
            return
        
        descricao = input("Descrição: ").strip()
        if not descricao:
            print("Descrição é obrigatória!")
            self.pausar()
            return
        
        preco = self.obter_entrada_decimal("Preço: R$ ", 0.01)
        if preco is None:
            print("Preço é obrigatório!")
            self.pausar()
            return
        
        estoque = self.obter_entrada_numerica("Estoque inicial: ", 0)
        if estoque is None:
            print("Estoque é obrigatório!")
            self.pausar()
            return
        
        sucesso, mensagem, produto = self.produto_manager.criar_produto(nome, descricao, preco, estoque)
        
        print(f"\n{mensagem}")
        
        if sucesso and produto:
            print(self.produto_manager.formatar_produto_para_exibicao(produto))
        
        self.pausar()
    
    def listar_produtos(self):
        """Lista todos os produtos"""
        self.limpar_tela()
        print("=== LISTA DE PRODUTOS ===\n")
        print("1. Apenas produtos ativos")
        print("2. Todos os produtos")
        
        opcao = self.obter_entrada_numerica("Escolha uma opção: ", 1, 2)
        
        produtos = self.produto_manager.listar_todos_produtos(apenas_ativos=(opcao == 1))
        
        if not produtos:
            print("Nenhum produto encontrado.")
        else:
            print(f"\nTotal de produtos: {len(produtos)}\n")
            for produto in produtos:
                status = "ATIVO" if produto.ativo else "INATIVO"
                estoque_info = f" [SEM ESTOQUE]" if produto.estoque == 0 else f" [BAIXO]" if produto.estoque <= 5 else ""
                print(f"ID: {produto.id_produto} | {produto.nome} | R$ {produto.preco:.2f} | Estoque: {produto.estoque}{estoque_info} | {status}")
        
        self.pausar()
    
    def buscar_produto(self):
        """Busca produto por ID ou nome"""
        self.limpar_tela()
        print("=== BUSCAR PRODUTO ===\n")
        print("1. Buscar por ID")
        print("2. Buscar por nome")
        
        opcao = self.obter_entrada_numerica("Escolha uma opção: ", 1, 2)
        
        if opcao == 1:
            id_produto = self.obter_entrada_numerica("ID do produto: ", 1)
            if id_produto:
                produto = self.produto_manager.buscar_produto_por_id(id_produto)
                if produto:
                    print(self.produto_manager.formatar_produto_para_exibicao(produto))
                else:
                    print("Produto não encontrado.")
        
        elif opcao == 2:
            nome = input("Nome (ou parte do nome): ").strip()
            if nome:
                produtos = self.produto_manager.buscar_produtos_por_nome(nome)
                if produtos:
                    print(f"\nEncontrados {len(produtos)} produto(s):\n")
                    for produto in produtos:
                        status = "ATIVO" if produto.ativo else "INATIVO"
                        print(f"ID: {produto.id_produto} | {produto.nome} | R$ {produto.preco:.2f} | Estoque: {produto.estoque} | {status}")
                else:
                    print("Nenhum produto encontrado.")
        
        self.pausar()
    
    def atualizar_produto(self):
        """Atualiza dados de um produto"""
        self.limpar_tela()
        print("=== ATUALIZAR PRODUTO ===\n")
        
        id_produto = self.obter_entrada_numerica("ID do produto: ", 1)
        if not id_produto:
            return
        
        produto = self.produto_manager.buscar_produto_por_id(id_produto)
        if not produto:
            print("Produto não encontrado.")
            self.pausar()
            return
        
        print("Dados atuais:")
        print(self.produto_manager.formatar_produto_para_exibicao(produto))
        
        print("Digite os novos dados (Enter para manter o atual):")
        
        nome = input(f"Nome [{produto.nome}]: ").strip() or produto.nome
        descricao = input(f"Descrição [{produto.descricao}]: ").strip() or produto.descricao
        
        preco_str = input(f"Preço [R$ {produto.preco:.2f}]: ").strip()
        preco = float(preco_str) if preco_str else produto.preco
        
        estoque_str = input(f"Estoque [{produto.estoque}]: ").strip()
        estoque = int(estoque_str) if estoque_str else produto.estoque
        
        sucesso, mensagem = self.produto_manager.atualizar_produto(id_produto, nome, descricao, preco, estoque)
        print(f"\n{mensagem}")
        
        self.pausar()
    
    def ajustar_estoque(self):
        """Ajusta estoque de um produto"""
        self.limpar_tela()
        print("=== AJUSTAR ESTOQUE ===\n")
        
        id_produto = self.obter_entrada_numerica("ID do produto: ", 1)
        if not id_produto:
            return
        
        produto = self.produto_manager.buscar_produto_por_id(id_produto)
        if not produto:
            print("Produto não encontrado.")
            self.pausar()
            return
        
        print(f"Produto: {produto.nome}")
        print(f"Estoque atual: {produto.estoque}")
        
        print("\n1. Adicionar ao estoque")
        print("2. Remover do estoque")
        print("3. Definir estoque")
        
        opcao = self.obter_entrada_numerica("Escolha uma opção: ", 1, 3)
        
        if opcao == 1:
            quantidade = self.obter_entrada_numerica("Quantidade a adicionar: ", 1)
            if quantidade:
                sucesso, mensagem = self.produto_manager.ajustar_estoque(id_produto, quantidade, "adicionar")
        
        elif opcao == 2:
            quantidade = self.obter_entrada_numerica("Quantidade a remover: ", 1)
            if quantidade:
                sucesso, mensagem = self.produto_manager.ajustar_estoque(id_produto, quantidade, "remover")
        
        elif opcao == 3:
            quantidade = self.obter_entrada_numerica("Novo estoque: ", 0)
            if quantidade is not None:
                sucesso, mensagem = self.produto_manager.ajustar_estoque(id_produto, quantidade, "definir")
        
        if 'sucesso' in locals():
            print(f"\n{mensagem}")
        
        self.pausar()
    
    def ativar_desativar_produto(self):
        """Ativa ou desativa um produto"""
        self.limpar_tela()
        print("=== ATIVAR/DESATIVAR PRODUTO ===\n")
        
        id_produto = self.obter_entrada_numerica("ID do produto: ", 1)
        if not id_produto:
            return
        
        produto = self.produto_manager.buscar_produto_por_id(id_produto)
        if not produto:
            print("Produto não encontrado.")
            self.pausar()
            return
        
        status_atual = "ATIVO" if produto.ativo else "INATIVO"
        print(f"Produto: {produto.nome}")
        print(f"Status atual: {status_atual}")
        
        if produto.ativo:
            confirmacao = input("Desativar produto? (s/N): ").strip().lower()
            if confirmacao == 's':
                sucesso, mensagem = self.produto_manager.desativar_produto(id_produto)
                print(f"\n{mensagem}")
        else:
            confirmacao = input("Ativar produto? (s/N): ").strip().lower()
            if confirmacao == 's':
                sucesso, mensagem = self.produto_manager.ativar_produto(id_produto)
                print(f"\n{mensagem}")
        
        self.pausar()
    
    def relatorio_estoque(self):
        """Exibe relatório de estoque"""
        self.limpar_tela()
        print("=== RELATÓRIO DE ESTOQUE ===\n")
        
        relatorio = self.produto_manager.gerar_relatorio_estoque()
        print(relatorio)
        
        self.pausar()
    
    def estatisticas_produtos(self):
        """Exibe estatísticas dos produtos"""
        self.limpar_tela()
        print("=== ESTATÍSTICAS DE PRODUTOS ===\n")
        
        stats = self.produto_manager.obter_estatisticas_produtos()
        
        print(f"Total de produtos: {stats['total_produtos']}")
        print(f"Produtos ativos: {stats['produtos_ativos']}")
        print(f"Produtos inativos: {stats['produtos_inativos']}")
        print(f"Produtos sem estoque: {stats['produtos_sem_estoque']}")
        print(f"Produtos com estoque baixo: {stats['produtos_estoque_baixo']}")
        print(f"Valor total do estoque: R$ {stats['valor_total_estoque']:.2f}")
        
        if stats['produto_mais_vendido']['produto']:
            print(f"Produto mais vendido: {stats['produto_mais_vendido']['produto']} ({stats['produto_mais_vendido']['quantidade_vendida']} unidades)")
        
        if stats['produto_mais_caro']['produto']:
            print(f"Produto mais caro: {stats['produto_mais_caro']['produto']} (R$ {stats['produto_mais_caro']['preco']:.2f})")
        
        if stats['produto_mais_barato']['produto']:
            print(f"Produto mais barato: {stats['produto_mais_barato']['produto']} (R$ {stats['produto_mais_barato']['preco']:.2f})")
        
        self.pausar()
    
    def menu_pedidos(self):
        """Menu de gerenciamento de pedidos"""
        while True:
            self.limpar_tela()
            print("=" * 40)
            print("    GERENCIAR PEDIDOS")
            print("=" * 40)
            print("1. Criar Pedido")
            print("2. Listar Pedidos")
            print("3. Buscar Pedido")
            print("4. Adicionar Item ao Pedido")
            print("5. Remover Item do Pedido")
            print("6. Alterar Status do Pedido")
            print("7. Cancelar Pedido")
            print("0. Voltar")
            print("=" * 40)
            
            opcao = self.obter_entrada_numerica("Escolha uma opção: ", 0, 7)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.criar_pedido()
            elif opcao == 2:
                self.listar_pedidos()
            elif opcao == 3:
                self.buscar_pedido()
            elif opcao == 4:
                self.adicionar_item_pedido()
            elif opcao == 5:
                self.remover_item_pedido()
            elif opcao == 6:
                self.alterar_status_pedido()
            elif opcao == 7:
                self.cancelar_pedido()
    
    def criar_pedido(self):
        """Cria um novo pedido"""
        self.limpar_tela()
        print("=== CRIAR PEDIDO ===\n")
        
        # Listar clientes disponíveis
        clientes = self.cliente_manager.listar_todos_clientes()
        if not clientes:
            print("Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
            self.pausar()
            return
        
        print("Clientes disponíveis:")
        for cliente in clientes[:10]:  # Mostrar apenas os primeiros 10
            print(f"ID: {cliente.id_cliente} | {cliente.nome} | {cliente.email}")
        
        if len(clientes) > 10:
            print(f"... e mais {len(clientes) - 10} clientes")
        
        id_cliente = self.obter_entrada_numerica("\nID do cliente: ", 1)
        if not id_cliente:
            return
        
        observacoes = input("Observações (opcional): ").strip()
        
        sucesso, mensagem, pedido = self.pedido_manager.criar_pedido(id_cliente, observacoes)
        
        print(f"\n{mensagem}")
        
        if sucesso and pedido:
            print(f"\nPedido criado com ID: {pedido.id_pedido}")
            print("Agora você pode adicionar itens ao pedido.")
        
        self.pausar()
    
    def listar_pedidos(self):
        """Lista pedidos com filtros"""
        self.limpar_tela()
        print("=== LISTAR PEDIDOS ===\n")
        print("1. Todos os pedidos")
        print("2. Por status")
        print("3. Por cliente")
        print("4. Por período")
        
        opcao = self.obter_entrada_numerica("Escolha uma opção: ", 1, 4)
        
        pedidos = []
        
        if opcao == 1:
            pedidos = self.pedido_manager.listar_todos_pedidos()
        
        elif opcao == 2:
            print("\nStatus disponíveis:")
            for i, status in enumerate(StatusPedido, 1):
                print(f"{i}. {status.value}")
            
            status_opcao = self.obter_entrada_numerica("Escolha o status: ", 1, len(StatusPedido))
            if status_opcao:
                status = list(StatusPedido)[status_opcao - 1]
                pedidos = self.pedido_manager.listar_pedidos_por_status(status)
        
        elif opcao == 3:
            id_cliente = self.obter_entrada_numerica("ID do cliente: ", 1)
            if id_cliente:
                pedidos = self.pedido_manager.listar_pedidos_por_cliente(id_cliente)
        
        elif opcao == 4:
            dias = self.obter_entrada_numerica("Últimos quantos dias: ", 1)
            if dias:
                data_inicio = datetime.now() - timedelta(days=dias)
                data_fim = datetime.now()
                pedidos = self.pedido_manager.listar_pedidos_por_periodo(data_inicio, data_fim)
        
        if pedidos:
            print(f"\nEncontrados {len(pedidos)} pedido(s):\n")
            for pedido in pedidos:
                print(f"ID: {pedido.id_pedido} | Cliente: {pedido.cliente.nome} | Status: {pedido.status.value} | Total: R$ {pedido.total:.2f} | Data: {pedido.data_pedido.strftime('%d/%m/%Y')}")
        else:
            print("Nenhum pedido encontrado.")
        
        self.pausar()
    
    def buscar_pedido(self):
        """Busca e exibe detalhes de um pedido"""
        self.limpar_tela()
        print("=== BUSCAR PEDIDO ===\n")
        
        id_pedido = self.obter_entrada_numerica("ID do pedido: ", 1)
        if not id_pedido:
            return
        
        pedido = self.pedido_manager.buscar_pedido_por_id(id_pedido)
        if pedido:
            print(self.pedido_manager.formatar_pedido_para_exibicao(pedido))
        else:
            print("Pedido não encontrado.")
        
        self.pausar()
    
    def adicionar_item_pedido(self):
        """Adiciona item a um pedido"""
        self.limpar_tela()
        print("=== ADICIONAR ITEM AO PEDIDO ===\n")
        
        id_pedido = self.obter_entrada_numerica("ID do pedido: ", 1)
        if not id_pedido:
            return
        
        # Verificar se pedido existe
        pedido = self.pedido_manager.buscar_pedido_por_id(id_pedido)
        if not pedido:
            print("Pedido não encontrado.")
            self.pausar()
            return
        
        print(f"Pedido #{id_pedido} - Cliente: {pedido.cliente.nome}")
        print(f"Status: {pedido.status.value}")
        
        # Listar produtos disponíveis
        produtos = self.produto_manager.listar_todos_produtos(apenas_ativos=True)
        if not produtos:
            print("Nenhum produto ativo disponível.")
            self.pausar()
            return
        
        print("\nProdutos disponíveis:")
        for produto in produtos[:10]:  # Mostrar apenas os primeiros 10
            print(f"ID: {produto.id_produto} | {produto.nome} | R$ {produto.preco:.2f} | Estoque: {produto.estoque}")
        
        if len(produtos) > 10:
            print(f"... e mais {len(produtos) - 10} produtos")
        
        id_produto = self.obter_entrada_numerica("\nID do produto: ", 1)
        if not id_produto:
            return
        
        quantidade = self.obter_entrada_numerica("Quantidade: ", 1)
        if not quantidade:
            return
        
        sucesso, mensagem = self.pedido_manager.adicionar_item_pedido(id_pedido, id_produto, quantidade)
        print(f"\n{mensagem}")
        
        self.pausar()
    
    def remover_item_pedido(self):
        """Remove item de um pedido"""
        self.limpar_tela()
        print("=== REMOVER ITEM DO PEDIDO ===\n")
        
        id_pedido = self.obter_entrada_numerica("ID do pedido: ", 1)
        if not id_pedido:
            return
        
        # Verificar se pedido existe e mostrar itens
        pedido = self.pedido_manager.buscar_pedido_por_id(id_pedido)
        if not pedido:
            print("Pedido não encontrado.")
            self.pausar()
            return
        
        if not pedido.itens:
            print("Pedido não possui itens.")
            self.pausar()
            return
        
        print(f"Pedido #{id_pedido} - Itens:")
        for item in pedido.itens:
            print(f"ID: {item.produto.id_produto} | {item.produto.nome} | Qtd: {item.quantidade} | Subtotal: R$ {item.subtotal:.2f}")
        
        id_produto = self.obter_entrada_numerica("\nID do produto a remover: ", 1)
        if not id_produto:
            return
        
        sucesso, mensagem = self.pedido_manager.remover_item_pedido(id_pedido, id_produto)
        print(f"\n{mensagem}")
        
        self.pausar()
    
    def alterar_status_pedido(self):
        """Altera status de um pedido"""
        self.limpar_tela()
        print("=== ALTERAR STATUS DO PEDIDO ===\n")
        
        id_pedido = self.obter_entrada_numerica("ID do pedido: ", 1)
        if not id_pedido:
            return
        
        pedido = self.pedido_manager.buscar_pedido_por_id(id_pedido)
        if not pedido:
            print("Pedido não encontrado.")
            self.pausar()
            return
        
        print(f"Pedido #{id_pedido}")
        print(f"Status atual: {pedido.status.value}")
        
        print("\nStatus disponíveis:")
        for i, status in enumerate(StatusPedido, 1):
            print(f"{i}. {status.value}")
        
        status_opcao = self.obter_entrada_numerica("Escolha o novo status: ", 1, len(StatusPedido))
        if not status_opcao:
            return
        
        novo_status = list(StatusPedido)[status_opcao - 1]
        
        sucesso, mensagem = self.pedido_manager.alterar_status_pedido(id_pedido, novo_status)
        print(f"\n{mensagem}")
        
        self.pausar()
    
    def cancelar_pedido(self):
        """Cancela um pedido"""
        self.limpar_tela()
        print("=== CANCELAR PEDIDO ===\n")
        
        id_pedido = self.obter_entrada_numerica("ID do pedido: ", 1)
        if not id_pedido:
            return
        
        pedido = self.pedido_manager.buscar_pedido_por_id(id_pedido)
        if not pedido:
            print("Pedido não encontrado.")
            self.pausar()
            return
        
        print(f"Pedido #{id_pedido}")
        print(f"Cliente: {pedido.cliente.nome}")
        print(f"Status atual: {pedido.status.value}")
        print(f"Total: R$ {pedido.total:.2f}")
        
        confirmacao = input("\nConfirma o cancelamento? (s/N): ").strip().lower()
        
        if confirmacao == 's':
            motivo = input("Motivo do cancelamento (opcional): ").strip()
            sucesso, mensagem = self.pedido_manager.cancelar_pedido(id_pedido, motivo)
            print(f"\n{mensagem}")
        else:
            print("Cancelamento não realizado.")
        
        self.pausar()
    
    def menu_relatorios(self):
        """Menu de relatórios"""
        while True:
            self.limpar_tela()
            print("=" * 40)
            print("    RELATÓRIOS")
            print("=" * 40)
            print("1. Relatório de Vendas")
            print("2. Relatório de Estoque")
            print("3. Relatório de Clientes")
            print("4. Relatório Completo")
            print("0. Voltar")
            print("=" * 40)
            
            opcao = self.obter_entrada_numerica("Escolha uma opção: ", 0, 4)
            
            if opcao == 0:
                break
            elif opcao == 1:
                self.relatorio_vendas()
            elif opcao == 2:
                self.relatorio_estoque()
            elif opcao == 3:
                self.relatorio_clientes()
            elif opcao == 4:
                self.relatorio_completo()
    
    def relatorio_vendas(self):
        """Gera relatório de vendas"""
        self.limpar_tela()
        print("=== RELATÓRIO DE VENDAS ===\n")
        
        periodo = self.obter_entrada_numerica("Período (últimos quantos dias): ", 1) or 30
        
        relatorio = self.pedido_manager.gerar_relatorio_vendas(periodo)
        print(relatorio)
        
        self.pausar()
    
    def relatorio_clientes(self):
        """Gera relatório de clientes"""
        self.limpar_tela()
        print("=== RELATÓRIO DE CLIENTES ===\n")
        
        stats = self.cliente_manager.obter_estatisticas_clientes()
        clientes = self.cliente_manager.listar_todos_clientes()
        
        print(f"RESUMO DE CLIENTES:")
        print(f"Total de clientes cadastrados: {stats['total_clientes']}")
        print(f"Clientes com pedidos: {stats['clientes_com_pedidos']}")
        print(f"Clientes sem pedidos: {stats['clientes_sem_pedidos']}")
        
        if stats['cliente_mais_pedidos']['cliente']:
            print(f"Cliente com mais pedidos: {stats['cliente_mais_pedidos']['cliente']} ({stats['cliente_mais_pedidos']['quantidade_pedidos']} pedidos)")
        
        if stats['cliente_maior_valor']['cliente']:
            print(f"Cliente com maior valor: {stats['cliente_maior_valor']['cliente']} (R$ {stats['cliente_maior_valor']['valor_total']:.2f})")
        
        print(f"\nLISTA COMPLETA DE CLIENTES:")
        for cliente in clientes:
            pedidos_cliente = self.pedido_manager.listar_pedidos_por_cliente(cliente.id_cliente)
            total_pedidos = len(pedidos_cliente)
            valor_total = sum(p.total for p in pedidos_cliente if p.status.value == 'entregue')
            
            print(f"- {cliente.nome} ({cliente.email})")
            print(f"  Pedidos: {total_pedidos} | Valor total: R$ {valor_total:.2f}")
            print(f"  Cadastro: {cliente.data_cadastro.strftime('%d/%m/%Y')}")
            print()
        
        self.pausar()
    
    def relatorio_completo(self):
        """Gera relatório completo do sistema"""
        self.limpar_tela()
        print("=== RELATÓRIO COMPLETO DO SISTEMA ===\n")
        
        # Estatísticas gerais
        stats_clientes = self.cliente_manager.obter_estatisticas_clientes()
        stats_produtos = self.produto_manager.obter_estatisticas_produtos()
        stats_pedidos = self.pedido_manager.obter_estatisticas_pedidos()
        
        print("RESUMO GERAL:")
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Total de clientes: {stats_clientes['total_clientes']}")
        print(f"Total de produtos: {stats_produtos['total_produtos']}")
        print(f"Total de pedidos: {stats_pedidos['total_pedidos']}")
        print(f"Receita total: R$ {stats_pedidos['receita_total']:.2f}")
        print(f"Valor do estoque: R$ {stats_produtos['valor_total_estoque']:.2f}")
        
        print(f"\nCLIENTES:")
        print(f"- Com pedidos: {stats_clientes['clientes_com_pedidos']}")
        print(f"- Sem pedidos: {stats_clientes['clientes_sem_pedidos']}")
        
        print(f"\nPRODUTOS:")
        print(f"- Ativos: {stats_produtos['produtos_ativos']}")
        print(f"- Inativos: {stats_produtos['produtos_inativos']}")
        print(f"- Sem estoque: {stats_produtos['produtos_sem_estoque']}")
        print(f"- Estoque baixo: {stats_produtos['produtos_estoque_baixo']}")
        
        print(f"\nPEDIDOS POR STATUS:")
        for status, quantidade in stats_pedidos['pedidos_por_status'].items():
            print(f"- {status.capitalize()}: {quantidade}")
        
        print(f"\nVENDAS:")
        print(f"- Ticket médio: R$ {stats_pedidos['ticket_medio']:.2f}")
        
        if stats_pedidos['produto_mais_vendido']:
            print(f"- Produto mais vendido: {stats_pedidos['produto_mais_vendido']['produto']} ({stats_pedidos['produto_mais_vendido']['quantidade_vendida']} unidades)")
        
        if stats_pedidos['cliente_mais_pedidos']:
            print(f"- Cliente com mais pedidos: {stats_pedidos['cliente_mais_pedidos']['cliente']} ({stats_pedidos['cliente_mais_pedidos']['quantidade_pedidos']} pedidos)")
        
        # Alertas
        print(f"\nALERTAS:")
        produtos_sem_estoque = self.produto_manager.listar_produtos_sem_estoque()
        if produtos_sem_estoque:
            print(f"- {len(produtos_sem_estoque)} produto(s) sem estoque")
        
        produtos_estoque_baixo = self.produto_manager.listar_produtos_com_estoque_baixo()
        if produtos_estoque_baixo:
            print(f"- {len(produtos_estoque_baixo)} produto(s) com estoque baixo")
        
        pedidos_pendentes = self.pedido_manager.listar_pedidos_por_status(StatusPedido.PENDENTE)
        if pedidos_pendentes:
            print(f"- {len(pedidos_pendentes)} pedido(s) pendente(s)")
        
        self.pausar()
    
    def menu_estatisticas(self):
        """Menu de estatísticas"""
        self.limpar_tela()
        print("=== ESTATÍSTICAS GERAIS ===\n")
        
        stats_clientes = self.cliente_manager.obter_estatisticas_clientes()
        stats_produtos = self.produto_manager.obter_estatisticas_produtos()
        stats_pedidos = self.pedido_manager.obter_estatisticas_pedidos()
        
        print("CLIENTES:")
        print(f"  Total: {stats_clientes['total_clientes']}")
        print(f"  Com pedidos: {stats_clientes['clientes_com_pedidos']}")
        print(f"  Sem pedidos: {stats_clientes['clientes_sem_pedidos']}")
        
        print(f"\nPRODUTOS:")
        print(f"  Total: {stats_produtos['total_produtos']}")
        print(f"  Ativos: {stats_produtos['produtos_ativos']}")
        print(f"  Sem estoque: {stats_produtos['produtos_sem_estoque']}")
        print(f"  Valor total estoque: R$ {stats_produtos['valor_total_estoque']:.2f}")
        
        print(f"\nPEDIDOS:")
        print(f"  Total: {stats_pedidos['total_pedidos']}")
        print(f"  Receita total: R$ {stats_pedidos['receita_total']:.2f}")
        print(f"  Ticket médio: R$ {stats_pedidos['ticket_medio']:.2f}")
        
        print(f"\nTOP PERFORMERS:")
        if stats_pedidos['produto_mais_vendido']['produto']:
            print(f"  Produto mais vendido: {stats_pedidos['produto_mais_vendido']['produto']}")
        
        if stats_pedidos['cliente_mais_pedidos']['cliente']:
            print(f"  Cliente mais ativo: {stats_pedidos['cliente_mais_pedidos']['cliente']}")
        
        self.pausar()
    
    def executar(self):
        """Executa o sistema principal"""
        while True:
            self.limpar_tela()
            self.exibir_menu_principal()
            
            opcao = self.obter_entrada_numerica("Escolha uma opção: ", 0, 5)
            
            if opcao == 0:
                print("\nObrigado por usar o Sistema de Gestão de Pedidos!")
                break
            elif opcao == 1:
                self.menu_clientes()
            elif opcao == 2:
                self.menu_produtos()
            elif opcao == 3:
                self.menu_pedidos()
            elif opcao == 4:
                self.menu_relatorios()
            elif opcao == 5:
                self.menu_estatisticas()
