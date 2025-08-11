from datetime import datetime, timedelta
from database import Database
from cliente_manager import ClienteManager
from produto_manager import ProdutoManager
from pedido_manager import PedidoManager
from models import StatusPedido

def testar_sistema_pedidos():
    """Testa todas as funcionalidades do sistema de pedidos"""
    print("=== TESTE DO SISTEMA DE PEDIDOS ===\n")
    
    # Inicializar sistema
    db = Database("test_data")
    cliente_manager = ClienteManager(db)
    produto_manager = ProdutoManager(db)
    pedido_manager = PedidoManager(db)
    
    print("1. Preparando dados de teste...")
    
    # Criar cliente de teste
    sucesso, mensagem, cliente = cliente_manager.criar_cliente(
        "João Teste", "joao.teste@email.com", "(11) 99999-9999", "Rua Teste, 123"
    )
    print(f"  Cliente: {mensagem}")
    
    # Criar produtos de teste
    produtos_teste = [
        ("Produto A", "Descrição do Produto A", 100.0, 10),
        ("Produto B", "Descrição do Produto B", 50.0, 5),
        ("Produto C", "Descrição do Produto C", 200.0, 2),
    ]
    
    produtos_criados = []
    for nome, desc, preco, estoque in produtos_teste:
        sucesso, mensagem, produto = produto_manager.criar_produto(nome, desc, preco, estoque)
        print(f"  Produto: {mensagem}")
        if sucesso:
            produtos_criados.append(produto)
    
    print(f"\n2. Testando criação de pedidos...")
    
    if cliente and produtos_criados:
        # Criar pedido
        sucesso, mensagem, pedido = pedido_manager.criar_pedido(
            cliente.id_cliente, "Pedido de teste"
        )
        print(f"  {mensagem}")
        
        if sucesso:
            print(f"\n3. Testando adição de itens...")
            
            # Adicionar itens ao pedido
            for i, produto in enumerate(produtos_criados[:2]):  # Apenas 2 produtos
                quantidade = i + 1
                sucesso_item, mensagem_item = pedido_manager.adicionar_item_pedido(
                    pedido.id_pedido, produto.id_produto, quantidade
                )
                print(f"    {mensagem_item}")
            
            # Tentar adicionar quantidade excessiva
            sucesso_item, mensagem_item = pedido_manager.adicionar_item_pedido(
                pedido.id_pedido, produtos_criados[2].id_produto, 10  # Mais que o estoque
            )
            print(f"    Teste estoque: {mensagem_item}")
            
            print(f"\n4. Testando exibição do pedido...")
            pedido_atualizado = pedido_manager.buscar_pedido_por_id(pedido.id_pedido)
            if pedido_atualizado:
                print(pedido_manager.formatar_pedido_para_exibicao(pedido_atualizado))
            
            print(f"\n5. Testando alteração de status...")
            
            # Processar pedido
            sucesso, mensagem = pedido_manager.alterar_status_pedido(
                pedido.id_pedido, StatusPedido.PROCESSANDO
            )
            print(f"    Processar: {mensagem}")
            
            # Verificar estoque após processamento
            for produto in produtos_criados[:2]:
                produto_atualizado = produto_manager.buscar_produto_por_id(produto.id_produto)
                if produto_atualizado:
                    print(f"    Estoque {produto.nome}: {produto_atualizado.estoque}")
            
            # Enviar pedido
            sucesso, mensagem = pedido_manager.alterar_status_pedido(
                pedido.id_pedido, StatusPedido.ENVIADO
            )
            print(f"    Enviar: {mensagem}")
            
            # Entregar pedido
            sucesso, mensagem = pedido_manager.alterar_status_pedido(
                pedido.id_pedido, StatusPedido.ENTREGUE
            )
            print(f"    Entregar: {mensagem}")
            
            print(f"\n6. Testando remoção de item...")
            
            # Criar outro pedido para testar remoção
            sucesso, mensagem, pedido2 = pedido_manager.criar_pedido(
                cliente.id_cliente, "Segundo pedido"
            )
            print(f"    {mensagem}")
            
            if sucesso:
                # Adicionar item
                pedido_manager.adicionar_item_pedido(
                    pedido2.id_pedido, produtos_criados[0].id_produto, 1
                )
                
                # Remover item
                sucesso, mensagem = pedido_manager.remover_item_pedido(
                    pedido2.id_pedido, produtos_criados[0].id_produto
                )
                print(f"    Remover item: {mensagem}")
            
            print(f"\n7. Testando cancelamento...")
            
            if pedido2:
                # Adicionar item novamente
                pedido_manager.adicionar_item_pedido(
                    pedido2.id_pedido, produtos_criados[0].id_produto, 1
                )
                
                # Processar para testar devolução de estoque
                pedido_manager.alterar_status_pedido(pedido2.id_pedido, StatusPedido.PROCESSANDO)
                
                # Cancelar
                sucesso, mensagem = pedido_manager.cancelar_pedido(
                    pedido2.id_pedido, "Teste de cancelamento"
                )
                print(f"    Cancelar: {mensagem}")
                
                # Verificar se estoque foi devolvido
                produto_teste = produto_manager.buscar_produto_por_id(produtos_criados[0].id_produto)
                if produto_teste:
                    print(f"    Estoque após cancelamento: {produto_teste.estoque}")
    
    print(f"\n8. Testando listagens...")
    
    # Listar todos os pedidos
    todos_pedidos = pedido_manager.listar_todos_pedidos()
    print(f"    Total de pedidos: {len(todos_pedidos)}")
    
    # Listar por status
    pedidos_entregues = pedido_manager.listar_pedidos_por_status(StatusPedido.ENTREGUE)
    print(f"    Pedidos entregues: {len(pedidos_entregues)}")
    
    # Listar por cliente
    if cliente:
        pedidos_cliente = pedido_manager.listar_pedidos_por_cliente(cliente.id_cliente)
        print(f"    Pedidos do cliente {cliente.nome}: {len(pedidos_cliente)}")
    
    # Listar por período
    data_inicio = datetime.now() - timedelta(days=1)
    data_fim = datetime.now() + timedelta(days=1)
    pedidos_periodo = pedido_manager.listar_pedidos_por_periodo(data_inicio, data_fim)
    print(f"    Pedidos nas últimas 24h: {len(pedidos_periodo)}")
    
    print(f"\n9. Testando estatísticas...")
    
    stats = pedido_manager.obter_estatisticas_pedidos()
    print(f"    Total de pedidos: {stats['total_pedidos']}")
    print(f"    Receita total: R$ {stats['receita_total']:.2f}")
    print(f"    Ticket médio: R$ {stats['ticket_medio']:.2f}")
    
    if stats['cliente_mais_pedidos']:
        print(f"    Cliente com mais pedidos: {stats['cliente_mais_pedidos']['cliente']} ({stats['cliente_mais_pedidos']['quantidade_pedidos']} pedidos)")
    
    if stats['produto_mais_vendido']:
        print(f"    Produto mais vendido: {stats['produto_mais_vendido']['produto']} ({stats['produto_mais_vendido']['quantidade_vendida']} unidades)")
    
    print(f"\n    Pedidos por status:")
    for status, quantidade in stats['pedidos_por_status'].items():
        print(f"      {status}: {quantidade}")
    
    print(f"\n10. Testando relatório de vendas...")
    
    relatorio = pedido_manager.gerar_relatorio_vendas(30)
    print(relatorio)
    
    print("=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    testar_sistema_pedidos()
