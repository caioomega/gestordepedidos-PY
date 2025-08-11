"""
Demonstração completa do Sistema de Gestão de Pedidos
Este script cria dados de exemplo e demonstra todas as funcionalidades
"""

from database import Database
from cliente_manager import ClienteManager
from produto_manager import ProdutoManager
from pedido_manager import PedidoManager
from models import StatusPedido
import random
from datetime import datetime, timedelta

def criar_dados_demo():
    """Cria dados de demonstração completos"""
    print("=== CRIANDO DADOS DE DEMONSTRAÇÃO ===\n")
    
    # Inicializar sistema
    db = Database("demo_data")
    cliente_manager = ClienteManager(db)
    produto_manager = ProdutoManager(db)
    pedido_manager = PedidoManager(db)
    
    print("1. Criando clientes de exemplo...")
    
    # Clientes de exemplo
    clientes_demo = [
        ("João Silva", "joao.silva@email.com", "(11) 99999-1111", "Rua das Flores, 123 - São Paulo, SP"),
        ("Maria Santos", "maria.santos@email.com", "(21) 98888-2222", "Av. Copacabana, 456 - Rio de Janeiro, RJ"),
        ("Pedro Oliveira", "pedro.oliveira@email.com", "(31) 97777-3333", "Rua da Liberdade, 789 - Belo Horizonte, MG"),
        ("Ana Costa", "ana.costa@email.com", "(41) 96666-4444", "Av. Paulista, 1000 - Curitiba, PR"),
        ("Carlos Ferreira", "carlos.ferreira@email.com", "(51) 95555-5555", "Rua Gaúcha, 200 - Porto Alegre, RS"),
        ("Lucia Mendes", "lucia.mendes@email.com", "(61) 94444-6666", "SQN 123, Bloco A - Brasília, DF"),
        ("Roberto Lima", "roberto.lima@email.com", "(85) 93333-7777", "Rua do Sol, 300 - Fortaleza, CE"),
        ("Fernanda Rocha", "fernanda.rocha@email.com", "(71) 92222-8888", "Av. Oceânica, 400 - Salvador, BA"),
    ]
    
    clientes_criados = []
    for nome, email, telefone, endereco in clientes_demo:
        sucesso, mensagem, cliente = cliente_manager.criar_cliente(nome, email, telefone, endereco)
        print(f"  {mensagem}")
        if sucesso:
            clientes_criados.append(cliente)
    
    print(f"\n2. Criando produtos de exemplo...")
    
    # Produtos de exemplo
    produtos_demo = [
        ("Notebook Dell Inspiron", "Notebook Dell Inspiron 15 com Intel i5, 8GB RAM, SSD 256GB", 2899.99, 15),
        ("Mouse Logitech MX Master", "Mouse sem fio ergonômico com precisão avançada", 299.90, 50),
        ("Teclado Mecânico RGB", "Teclado mecânico com iluminação RGB e switches Cherry MX", 459.99, 25),
        ("Monitor LG 27\"", "Monitor LED IPS 27 polegadas 4K Ultra HD", 1299.00, 8),
        ("Webcam Logitech C920", "Webcam Full HD 1080p com microfone integrado", 189.90, 30),
        ("Headset Gamer HyperX", "Headset gamer com som surround 7.1 e microfone", 349.99, 20),
        ("SSD Samsung 1TB", "SSD NVMe M.2 1TB com alta velocidade de transferência", 599.99, 12),
        ("Placa de Vídeo RTX 4060", "Placa de vídeo NVIDIA GeForce RTX 4060 8GB", 2199.99, 5),
        ("Memória RAM 16GB", "Memória DDR4 16GB 3200MHz para desktop", 299.99, 40),
        ("Fonte 650W", "Fonte de alimentação modular 650W 80+ Gold", 399.99, 18),
        ("Gabinete Gamer", "Gabinete mid-tower com painel lateral em vidro", 249.99, 10),
        ("Cooler CPU", "Cooler para processador com ventilador RGB", 129.99, 35),
        ("Mousepad Gamer", "Mousepad gamer extra grande com base antiderrapante", 79.99, 60),
        ("Cabo HDMI 2.1", "Cabo HDMI 2.1 4K 60Hz - 2 metros", 49.99, 100),
        ("Hub USB 3.0", "Hub USB 3.0 com 7 portas e fonte de alimentação", 89.99, 45),
    ]
    
    produtos_criados = []
    for nome, descricao, preco, estoque in produtos_demo:
        sucesso, mensagem, produto = produto_manager.criar_produto(nome, descricao, preco, estoque)
        print(f"  {mensagem}")
        if sucesso:
            produtos_criados.append(produto)
    
    print(f"\n3. Criando pedidos de exemplo...")
    
    # Criar pedidos variados
    for i in range(20):  # 20 pedidos de exemplo
        cliente = random.choice(clientes_criados)
        
        sucesso, mensagem, pedido = pedido_manager.criar_pedido(
            cliente.id_cliente, 
            f"Pedido de demonstração #{i+1}"
        )
        
        if sucesso:
            # Adicionar 1-4 itens aleatórios ao pedido
            num_itens = random.randint(1, 4)
            produtos_pedido = random.sample(produtos_criados, min(num_itens, len(produtos_criados)))
            
            for produto in produtos_pedido:
                quantidade = random.randint(1, 3)
                pedido_manager.adicionar_item_pedido(pedido.id_pedido, produto.id_produto, quantidade)
            
            # Simular diferentes status de pedidos
            if i < 5:  # Primeiros 5 ficam pendentes
                pass
            elif i < 10:  # Próximos 5 são processados
                pedido_manager.alterar_status_pedido(pedido.id_pedido, StatusPedido.PROCESSANDO)
            elif i < 15:  # Próximos 5 são enviados
                pedido_manager.alterar_status_pedido(pedido.id_pedido, StatusPedido.PROCESSANDO)
                pedido_manager.alterar_status_pedido(pedido.id_pedido, StatusPedido.ENVIADO)
            elif i < 18:  # Próximos 3 são entregues
                pedido_manager.alterar_status_pedido(pedido.id_pedido, StatusPedido.PROCESSANDO)
                pedido_manager.alterar_status_pedido(pedido.id_pedido, StatusPedido.ENVIADO)
                pedido_manager.alterar_status_pedido(pedido.id_pedido, StatusPedido.ENTREGUE)
            else:  # Últimos 2 são cancelados
                pedido_manager.cancelar_pedido(pedido.id_pedido, "Cancelado para demonstração")
            
            print(f"  Pedido #{pedido.id_pedido} criado para {cliente.nome}")
    
    print(f"\n4. Ajustando alguns estoques para demonstração...")
    
    # Deixar alguns produtos com estoque baixo ou zerado
    if len(produtos_criados) >= 3:
        produto_manager.ajustar_estoque(produtos_criados[0].id_produto, 2, "definir")  # Estoque baixo
        produto_manager.ajustar_estoque(produtos_criados[1].id_produto, 0, "definir")  # Sem estoque
        produto_manager.ajustar_estoque(produtos_criados[2].id_produto, 1, "definir")  # Estoque crítico
        print("  Estoques ajustados para demonstração de alertas")
    
    print(f"\n=== DADOS DE DEMONSTRAÇÃO CRIADOS COM SUCESSO ===")
    print(f"Clientes: {len(clientes_criados)}")
    print(f"Produtos: {len(produtos_criados)}")
    print(f"Pedidos: 20 (com diferentes status)")
    print(f"\nAgora você pode executar o sistema principal com 'python main.py'")
    print(f"Os dados estão salvos na pasta 'demo_data'")

def exibir_estatisticas_demo():
    """Exibe estatísticas dos dados de demonstração"""
    print("\n=== ESTATÍSTICAS DOS DADOS DE DEMONSTRAÇÃO ===\n")
    
    db = Database("demo_data")
    cliente_manager = ClienteManager(db)
    produto_manager = ProdutoManager(db)
    pedido_manager = PedidoManager(db)
    
    # Estatísticas de clientes
    stats_clientes = cliente_manager.obter_estatisticas_clientes()
    print("CLIENTES:")
    print(f"  Total: {stats_clientes['total_clientes']}")
    print(f"  Com pedidos: {stats_clientes['clientes_com_pedidos']}")
    print(f"  Sem pedidos: {stats_clientes['clientes_sem_pedidos']}")
    
    # Estatísticas de produtos
    stats_produtos = produto_manager.obter_estatisticas_produtos()
    print(f"\nPRODUTOS:")
    print(f"  Total: {stats_produtos['total_produtos']}")
    print(f"  Ativos: {stats_produtos['produtos_ativos']}")
    print(f"  Sem estoque: {stats_produtos['produtos_sem_estoque']}")
    print(f"  Estoque baixo: {stats_produtos['produtos_estoque_baixo']}")
    print(f"  Valor total estoque: R$ {stats_produtos['valor_total_estoque']:.2f}")
    
    # Estatísticas de pedidos
    stats_pedidos = pedido_manager.obter_estatisticas_pedidos()
    print(f"\nPEDIDOS:")
    print(f"  Total: {stats_pedidos['total_pedidos']}")
    print(f"  Receita total: R$ {stats_pedidos['receita_total']:.2f}")
    print(f"  Ticket médio: R$ {stats_pedidos['ticket_medio']:.2f}")
    
    print(f"\n  Por status:")
    for status, quantidade in stats_pedidos['pedidos_por_status'].items():
        print(f"    {status.capitalize()}: {quantidade}")
    
    # Relatório de vendas
    print(f"\n=== RELATÓRIO DE VENDAS (ÚLTIMOS 30 DIAS) ===")
    relatorio = pedido_manager.gerar_relatorio_vendas(30)
    print(relatorio)

if __name__ == "__main__":
    print("Sistema de Gestão de Pedidos - Demonstração Completa")
    print("=" * 60)
    
    opcao = input("1. Criar dados de demonstração\n2. Exibir estatísticas\n3. Ambos\nEscolha: ").strip()
    
    if opcao in ['1', '3']:
        criar_dados_demo()
    
    if opcao in ['2', '3']:
        exibir_estatisticas_demo()
    
    print(f"\nPara usar o sistema completo, execute: python main.py")
