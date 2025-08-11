from database import Database
from cliente_manager import ClienteManager

def testar_sistema_clientes():
    """Testa todas as funcionalidades do sistema de clientes"""
    print("=== TESTE DO SISTEMA DE CLIENTES ===\n")
    
    # Inicializar sistema
    db = Database("test_data")
    cliente_manager = ClienteManager(db)
    
    print("1. Testando criação de clientes...")
    
    # Criar clientes de teste
    clientes_teste = [
        ("João Silva", "joao@email.com", "(11) 99999-1111", "Rua A, 123 - São Paulo, SP"),
        ("Maria Santos", "maria@email.com", "11987654321", "Av. B, 456 - Rio de Janeiro, RJ"),
        ("Pedro Oliveira", "pedro@email.com", "(21) 98765-4321", "Rua C, 789 - Belo Horizonte, MG"),
    ]
    
    clientes_criados = []
    for nome, email, telefone, endereco in clientes_teste:
        sucesso, mensagem, cliente = cliente_manager.criar_cliente(nome, email, telefone, endereco)
        print(f"  {mensagem}")
        if sucesso:
            clientes_criados.append(cliente)
    
    print(f"\n2. Testando validações...")
    
    # Testar validações
    testes_validacao = [
        ("", "email@test.com", "11999999999", "Endereço válido"),  # Nome inválido
        ("Nome Válido", "email_inválido", "11999999999", "Endereço válido"),  # Email inválido
        ("Nome Válido", "novo@email.com", "123", "Endereço válido"),  # Telefone inválido
        ("Nome Válido", "novo2@email.com", "11999999999", ""),  # Endereço inválido
        ("Nome Válido", "joao@email.com", "11999999999", "Endereço válido"),  # Email duplicado
    ]
    
    for nome, email, telefone, endereco in testes_validacao:
        sucesso, mensagem, _ = cliente_manager.criar_cliente(nome, email, telefone, endereco)
        print(f"  Validação: {mensagem}")
    
    print(f"\n3. Testando busca de clientes...")
    
    # Testar buscas
    if clientes_criados:
        primeiro_cliente = clientes_criados[0]
        
        # Busca por ID
        cliente_encontrado = cliente_manager.buscar_cliente_por_id(primeiro_cliente.id_cliente)
        print(f"  Busca por ID {primeiro_cliente.id_cliente}: {'Encontrado' if cliente_encontrado else 'Não encontrado'}")
        
        # Busca por nome
        clientes_nome = cliente_manager.buscar_clientes_por_nome("Silva")
        print(f"  Busca por nome 'Silva': {len(clientes_nome)} cliente(s) encontrado(s)")
        
        # Busca por email
        cliente_email = cliente_manager.buscar_cliente_por_email(primeiro_cliente.email)
        print(f"  Busca por email: {'Encontrado' if cliente_email else 'Não encontrado'}")
    
    print(f"\n4. Testando listagem de clientes...")
    todos_clientes = cliente_manager.listar_todos_clientes()
    print(f"  Total de clientes cadastrados: {len(todos_clientes)}")
    
    for cliente in todos_clientes:
        print(f"  - {cliente.nome} ({cliente.email})")
    
    print(f"\n5. Testando atualização de cliente...")
    if clientes_criados:
        primeiro_cliente = clientes_criados[0]
        sucesso, mensagem = cliente_manager.atualizar_cliente(
            primeiro_cliente.id_cliente,
            "João Silva Atualizado",
            primeiro_cliente.email,
            "(11) 99999-2222",
            "Nova Rua, 999 - São Paulo, SP"
        )
        print(f"  {mensagem}")
    
    print(f"\n6. Testando estatísticas...")
    stats = cliente_manager.obter_estatisticas_clientes()
    print(f"  Total de clientes: {stats['total_clientes']}")
    print(f"  Clientes com pedidos: {stats['clientes_com_pedidos']}")
    print(f"  Clientes sem pedidos: {stats['clientes_sem_pedidos']}")
    
    print(f"\n7. Testando formatação para exibição...")
    if clientes_criados:
        primeiro_cliente_atualizado = cliente_manager.buscar_cliente_por_id(clientes_criados[0].id_cliente)
        if primeiro_cliente_atualizado:
            print("  Dados formatados:")
            print(cliente_manager.formatar_cliente_para_exibicao(primeiro_cliente_atualizado))
    
    print("=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    testar_sistema_clientes()
