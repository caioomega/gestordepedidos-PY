from database import Database
from produto_manager import ProdutoManager

def testar_sistema_produtos():
    """Testa todas as funcionalidades do sistema de produtos"""
    print("=== TESTE DO SISTEMA DE PRODUTOS ===\n")
    
    # Inicializar sistema
    db = Database("test_data")
    produto_manager = ProdutoManager(db)
    
    print("1. Testando criação de produtos...")
    
    # Criar produtos de teste
    produtos_teste = [
        ("Notebook Dell", "Notebook Dell Inspiron 15 com 8GB RAM e SSD 256GB", 2500.00, 10),
        ("Mouse Logitech", "Mouse óptico sem fio Logitech M170", 45.90, 25),
        ("Teclado Mecânico", "Teclado mecânico RGB com switches blue", 299.99, 5),
        ("Monitor 24\"", "Monitor LED 24 polegadas Full HD", 899.00, 3),
        ("Webcam HD", "Webcam 1080p com microfone integrado", 159.90, 0),
    ]
    
    produtos_criados = []
    for nome, descricao, preco, estoque in produtos_teste:
        sucesso, mensagem, produto = produto_manager.criar_produto(nome, descricao, preco, estoque)
        print(f"  {mensagem}")
        if sucesso:
            produtos_criados.append(produto)
    
    print(f"\n2. Testando validações...")
    
    # Testar validações
    testes_validacao = [
        ("", "Descrição válida", 100.0, 10),  # Nome inválido
        ("Produto Válido", "Desc", 100.0, 10),  # Descrição inválida
        ("Produto Válido", "Descrição válida", -50.0, 10),  # Preço inválido
        ("Produto Válido", "Descrição válida", 100.0, -5),  # Estoque inválido
        ("Notebook Dell", "Descrição válida", 100.0, 10),  # Nome duplicado
    ]
    
    for nome, descricao, preco, estoque in testes_validacao:
        sucesso, mensagem, _ = produto_manager.criar_produto(nome, descricao, preco, estoque)
        print(f"  Validação: {mensagem}")
    
    print(f"\n3. Testando busca de produtos...")
    
    # Testar buscas
    if produtos_criados:
        primeiro_produto = produtos_criados[0]
        
        # Busca por ID
        produto_encontrado = produto_manager.buscar_produto_por_id(primeiro_produto.id_produto)
        print(f"  Busca por ID {primeiro_produto.id_produto}: {'Encontrado' if produto_encontrado else 'Não encontrado'}")
        
        # Busca por nome
        produtos_nome = produto_manager.buscar_produtos_por_nome("Mouse")
        print(f"  Busca por nome 'Mouse': {len(produtos_nome)} produto(s) encontrado(s)")
    
    print(f"\n4. Testando listagem de produtos...")
    todos_produtos = produto_manager.listar_todos_produtos()
    print(f"  Total de produtos ativos: {len(todos_produtos)}")
    
    for produto in todos_produtos:
        print(f"  - {produto.nome} (R$ {produto.preco:.2f}) - Estoque: {produto.estoque}")
    
    print(f"\n5. Testando controle de estoque...")
    
    # Produtos com estoque baixo
    produtos_estoque_baixo = produto_manager.listar_produtos_com_estoque_baixo()
    print(f"  Produtos com estoque baixo: {len(produtos_estoque_baixo)}")
    for produto in produtos_estoque_baixo:
        print(f"    - {produto.nome}: {produto.estoque} unidades")
    
    # Produtos sem estoque
    produtos_sem_estoque = produto_manager.listar_produtos_sem_estoque()
    print(f"  Produtos sem estoque: {len(produtos_sem_estoque)}")
    for produto in produtos_sem_estoque:
        print(f"    - {produto.nome}")
    
    print(f"\n6. Testando ajuste de estoque...")
    if produtos_criados:
        primeiro_produto = produtos_criados[0]
        
        # Adicionar estoque
        sucesso, mensagem = produto_manager.ajustar_estoque(primeiro_produto.id_produto, 5, "adicionar")
        print(f"  Adicionar estoque: {mensagem}")
        
        # Remover estoque
        sucesso, mensagem = produto_manager.ajustar_estoque(primeiro_produto.id_produto, 3, "remover")
        print(f"  Remover estoque: {mensagem}")
        
        # Definir estoque
        sucesso, mensagem = produto_manager.ajustar_estoque(primeiro_produto.id_produto, 20, "definir")
        print(f"  Definir estoque: {mensagem}")
    
    print(f"\n7. Testando ativação/desativação...")
    if produtos_criados:
        segundo_produto = produtos_criados[1] if len(produtos_criados) > 1 else produtos_criados[0]
        
        # Desativar produto
        sucesso, mensagem = produto_manager.desativar_produto(segundo_produto.id_produto)
        print(f"  Desativar: {mensagem}")
        
        # Tentar desativar novamente
        sucesso, mensagem = produto_manager.desativar_produto(segundo_produto.id_produto)
        print(f"  Desativar novamente: {mensagem}")
        
        # Reativar produto
        sucesso, mensagem = produto_manager.ativar_produto(segundo_produto.id_produto)
        print(f"  Reativar: {mensagem}")
    
    print(f"\n8. Testando estatísticas...")
    stats = produto_manager.obter_estatisticas_produtos()
    print(f"  Total de produtos: {stats['total_produtos']}")
    print(f"  Produtos ativos: {stats['produtos_ativos']}")
    print(f"  Produtos sem estoque: {stats['produtos_sem_estoque']}")
    print(f"  Produtos com estoque baixo: {stats['produtos_estoque_baixo']}")
    print(f"  Valor total do estoque: R$ {stats['valor_total_estoque']:.2f}")
    
    if stats['produto_mais_caro']['produto']:
        print(f"  Produto mais caro: {stats['produto_mais_caro']['produto']} (R$ {stats['produto_mais_caro']['preco']:.2f})")
    
    if stats['produto_mais_barato']['produto']:
        print(f"  Produto mais barato: {stats['produto_mais_barato']['produto']} (R$ {stats['produto_mais_barato']['preco']:.2f})")
    
    print(f"\n9. Testando formatação para exibição...")
    if produtos_criados:
        primeiro_produto_atualizado = produto_manager.buscar_produto_por_id(produtos_criados[0].id_produto)
        if primeiro_produto_atualizado:
            print("  Dados formatados:")
            print(produto_manager.formatar_produto_para_exibicao(primeiro_produto_atualizado))
    
    print(f"\n10. Testando relatório de estoque...")
    relatorio = produto_manager.gerar_relatorio_estoque()
    print(relatorio)
    
    print("=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    testar_sistema_produtos()
