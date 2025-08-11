import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from database import Database
from cliente_manager import ClienteManager
from produto_manager import ProdutoManager
from pedido_manager import PedidoManager
from models import StatusPedido
from cotacao_manager import CotacaoManager

plt.style.use('seaborn-v0_8')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

class SistemaGestorPedidosGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Gestor de Pedidos - Profissional")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.cores = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'success': '#F18F01',
            'warning': '#C73E1D',
            'light': '#F5F5F5',
            'dark': '#2C3E50',
            'accent': '#E74C3C'
        }
        
        self.setup_styles()
        
        # Inicializar banco de dados e managers
        self.db = Database()
        self.cliente_manager = ClienteManager(self.db)
        self.produto_manager = ProdutoManager(self.db)
        self.pedido_manager = PedidoManager(self.db)
        self.cotacao_manager = CotacaoManager(self.db)
        
        # Configurar interface
        self.setup_ui()
        self.carregar_dados_iniciais()

    def setup_styles(self):
        """Configura estilos modernos para a interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground=self.cores['primary'])
        style.configure('Subtitle.TLabel', font=('Segoe UI', 12, 'bold'), foreground=self.cores['dark'])
        style.configure('Card.TFrame', relief='raised', borderwidth=2, background=self.cores['light'])
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Dashboard.TLabel', font=('Segoe UI', 14, 'bold'), foreground='white')
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), background=self.cores['accent'], foreground='white')

    def setup_ui(self):
        """Configura a interface principal"""
        self.create_menu()
        self.create_main_container()
        self.create_notebook()
        self.create_dashboard_tab()
        self.create_clientes_tab()
        self.create_produtos_tab()
        self.create_pedidos_tab()
        self.create_cotacoes_tab()
        self.create_graficos_tab()
        self.create_relatorios_tab()
        
        self.status_bar = ttk.Label(self.root, text="Sistema iniciado - Pronto para uso", 
                                   relief=tk.SUNKEN, font=('Segoe UI', 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_main_container(self):
        """Cria container principal com padding moderno"""
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def create_menu(self):
        """Cria menu principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Backup Dados", command=self.backup_dados)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Sobre
        sobre_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sobre", menu=sobre_menu)
        sobre_menu.add_command(label="Informações", command=self.mostrar_sobre)

    def create_notebook(self):
        """Cria notebook com abas"""
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

    def create_dashboard_tab(self):
        """Cria aba de dashboard moderna com estatísticas"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="🏠 Dashboard")
        
        header_frame = ttk.Frame(dashboard_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        title_label = ttk.Label(header_frame, text="Dashboard Executivo", style='Title.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame, text="Visão geral do seu negócio", style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        stats_frame = ttk.Frame(dashboard_frame)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Card 1 - Total de Clientes
        self.create_stat_card(stats_frame, "👥 Total de Clientes", "0", self.cores['primary'], 0)
        
        # Card 2 - Total de Produtos
        self.create_stat_card(stats_frame, "📦 Total de Produtos", "0", self.cores['success'], 1)
        
        # Card 3 - Pedidos Ativos
        self.create_stat_card(stats_frame, "🚚 Pedidos Ativos", "0", self.cores['secondary'], 2)
        
        # Card 4 - Faturamento do Mês
        self.create_stat_card(stats_frame, "💰 Faturamento Mensal", "R$ 0,00", self.cores['warning'], 3)
        
        charts_frame = ttk.Frame(dashboard_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Frame esquerdo - Gráfico de vendas
        left_chart_frame = ttk.LabelFrame(charts_frame, text="📈 Vendas dos Últimos 7 Dias", padding=10)
        left_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.dashboard_vendas_frame = ttk.Frame(left_chart_frame)
        self.dashboard_vendas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame direito - Gráfico de status
        right_chart_frame = ttk.LabelFrame(charts_frame, text="📊 Status dos Pedidos", padding=10)
        right_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.dashboard_status_frame = ttk.Frame(right_chart_frame)
        self.dashboard_status_frame.pack(fill=tk.BOTH, expand=True)
        
        refresh_frame = ttk.Frame(dashboard_frame)
        refresh_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(refresh_frame, text="🔄 Atualizar Dashboard", 
                  command=self.atualizar_dashboard, style='Primary.TButton').pack(anchor='e')

    def create_stat_card(self, parent, title, value, color, column):
        """Cria um card de estatística"""
        card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card_frame.grid(row=0, column=column, padx=10, pady=5, sticky='ew')
        parent.grid_columnconfigure(column, weight=1)
        
        # Título
        title_label = tk.Label(card_frame, text=title, bg=color, fg='white', 
                              font=('Segoe UI', 11, 'bold'))
        title_label.pack(pady=(15, 5))
        
        # Valor
        value_label = tk.Label(card_frame, text=value, bg=color, fg='white', 
                              font=('Segoe UI', 18, 'bold'))
        value_label.pack(pady=(0, 15))
        
        # Armazenar referência para atualização
        setattr(self, f'stat_card_{column}', value_label)

    def atualizar_dashboard(self):
        """Atualiza as estatísticas do dashboard"""
        try:
            clientes = self.cliente_manager.listar_todos_clientes()
            produtos = self.produto_manager.listar_todos_produtos()
            pedidos = self.pedido_manager.listar_todos_pedidos()
            
            # Atualizar valores dos cards
            self.stat_card_0.config(text=str(len(clientes)))
            self.stat_card_1.config(text=str(len(produtos)))
            
            pedidos_ativos = [p for p in pedidos if p.status.value in ['Pendente', 'Processando', 'Enviado']]
            self.stat_card_2.config(text=str(len(pedidos_ativos)))
            
            # Faturamento do mês atual
            mes_atual = datetime.now().replace(day=1)
            faturamento = sum(p.total for p in pedidos 
                            if p.data_pedido >= mes_atual and p.status.value != 'Cancelado')
            self.stat_card_3.config(text=f"R$ {faturamento:,.2f}")
            
            self.criar_grafico_vendas_dashboard()
            self.criar_grafico_status_dashboard()
            
            self.status_bar.config(text="Dashboard atualizado com sucesso")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dashboard: {str(e)}")

    def criar_grafico_vendas_dashboard(self):
        """Cria gráfico de vendas para o dashboard"""
        for widget in self.dashboard_vendas_frame.winfo_children():
            widget.destroy()
        
        try:
            pedidos = self.pedido_manager.listar_todos_pedidos()
            data_limite = datetime.now() - timedelta(days=7)
            
            vendas_por_dia = defaultdict(float)
            for pedido in pedidos:
                if pedido.data_pedido >= data_limite and pedido.status.value != 'Cancelado':
                    data_str = pedido.data_pedido.strftime('%d/%m')
                    vendas_por_dia[data_str] += pedido.total
            
            if vendas_por_dia:
                fig, ax = plt.subplots(figsize=(6, 3))
                
                datas = sorted(vendas_por_dia.keys())
                valores = [vendas_por_dia[data] for data in datas]
                
                ax.plot(datas, valores, marker='o', linewidth=2, markersize=4, 
                       color=self.cores['primary'], markerfacecolor=self.cores['success'])
                ax.fill_between(datas, valores, alpha=0.3, color=self.cores['primary'])
                
                ax.set_ylabel('Vendas (R$)')
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                canvas = FigureCanvasTkAgg(fig, self.dashboard_vendas_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            else:
                ttk.Label(self.dashboard_vendas_frame, text="Sem dados de vendas", 
                         font=('Segoe UI', 10)).pack(expand=True)
                
        except Exception as e:
            ttk.Label(self.dashboard_vendas_frame, text=f"Erro: {str(e)}", 
                     font=('Segoe UI', 9)).pack(expand=True)

    def criar_grafico_status_dashboard(self):
        """Cria gráfico de status para o dashboard"""
        for widget in self.dashboard_status_frame.winfo_children():
            widget.destroy()
        
        try:
            pedidos = self.pedido_manager.listar_todos_pedidos()
            status_count = Counter([pedido.status.value for pedido in pedidos])
            
            if status_count:
                fig, ax = plt.subplots(figsize=(6, 3))
                
                labels = list(status_count.keys())
                sizes = list(status_count.values())
                colors = [self.cores['primary'], self.cores['success'], self.cores['warning'], 
                         self.cores['secondary'], self.cores['accent']]
                
                wedges, texts, autotexts = ax.pie(sizes, labels=labels, 
                                                 colors=colors[:len(labels)], 
                                                 autopct='%1.0f%%', startangle=90)
                
                plt.tight_layout()
                
                canvas = FigureCanvasTkAgg(fig, self.dashboard_status_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            else:
                ttk.Label(self.dashboard_status_frame, text="Sem pedidos", 
                         font=('Segoe UI', 10)).pack(expand=True)
                
        except Exception as e:
            ttk.Label(self.dashboard_status_frame, text=f"Erro: {str(e)}", 
                     font=('Segoe UI', 9)).pack(expand=True)

    def create_clientes_tab(self):
        """Cria aba de clientes"""
        clientes_frame = ttk.Frame(self.notebook)
        self.notebook.add(clientes_frame, text="👥 Clientes")
        
        # Adicionar widgets para a aba de clientes aqui
        self.clientes_tree = ttk.Treeview(clientes_frame, columns=("ID", "Nome", "Email"), show="headings")
        self.clientes_tree.heading("ID", text="ID")
        self.clientes_tree.heading("Nome", text="Nome")
        self.clientes_tree.heading("Email", text="Email")
        self.clientes_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        buttons_frame = ttk.Frame(clientes_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Novo Cliente", command=self.novo_cliente_rapido).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Editar Cliente", command=self.editar_cliente_selecionado).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Remover Cliente", command=self.remover_cliente_selecionado).pack(side=tk.LEFT, padx=5)

    def create_produtos_tab(self):
        """Cria aba de produtos"""
        produtos_frame = ttk.Frame(self.notebook)
        self.notebook.add(produtos_frame, text="📦 Produtos")
        
        # Frame superior com filtros
        filtros_frame = ttk.LabelFrame(produtos_frame, text="Filtros", padding=10)
        filtros_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filtros_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.produto_status_filter = ttk.Combobox(filtros_frame, values=["Todos", "Ativos", "Inativos"], state="readonly", width=10)
        self.produto_status_filter.set("Todos")
        self.produto_status_filter.pack(side=tk.LEFT, padx=5)
        self.produto_status_filter.bind("<<ComboboxSelected>>", lambda e: self.filtrar_produtos())
        
        ttk.Label(filtros_frame, text="Estoque Baixo:").pack(side=tk.LEFT, padx=(20,5))
        self.estoque_baixo_var = tk.BooleanVar()
        ttk.Checkbutton(filtros_frame, variable=self.estoque_baixo_var, command=self.filtrar_produtos).pack(side=tk.LEFT)
        
        ttk.Button(filtros_frame, text="Limpar Filtros", command=self.limpar_filtros_produtos).pack(side=tk.RIGHT, padx=5)
        
        # Tabela de produtos com mais colunas
        self.produtos_tree = ttk.Treeview(produtos_frame, columns=("ID", "Nome", "Preço", "Estoque", "Status", "Categoria"), show="headings", height=15)
        self.produtos_tree.heading("ID", text="ID")
        self.produtos_tree.heading("Nome", text="Nome do Produto")
        self.produtos_tree.heading("Preço", text="Preço (R$)")
        self.produtos_tree.heading("Estoque", text="Estoque")
        self.produtos_tree.heading("Status", text="Status")
        self.produtos_tree.heading("Categoria", text="Categoria")
        
        # Configurando larguras das colunas
        self.produtos_tree.column("ID", width=50, anchor=tk.CENTER)
        self.produtos_tree.column("Nome", width=200, anchor=tk.W)
        self.produtos_tree.column("Preço", width=100, anchor=tk.E)
        self.produtos_tree.column("Estoque", width=80, anchor=tk.CENTER)
        self.produtos_tree.column("Status", width=80, anchor=tk.CENTER)
        self.produtos_tree.column("Categoria", width=120, anchor=tk.W)
        
        # Scrollbars
        produtos_scroll_y = ttk.Scrollbar(produtos_frame, orient=tk.VERTICAL, command=self.produtos_tree.yview)
        produtos_scroll_x = ttk.Scrollbar(produtos_frame, orient=tk.HORIZONTAL, command=self.produtos_tree.xview)
        self.produtos_tree.configure(yscrollcommand=produtos_scroll_y.set, xscrollcommand=produtos_scroll_x.set)
        
        # Pack da tabela e scrollbars
        self.produtos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=5)
        produtos_scroll_y.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        produtos_scroll_x.pack(side=tk.BOTTOM, fill=tk.X, padx=10)
        
        # Frame para botões com melhor organização
        buttons_frame = ttk.LabelFrame(produtos_frame, text="Ações", padding=10)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Primeira linha de botões
        buttons_row1 = ttk.Frame(buttons_frame)
        buttons_row1.pack(fill=tk.X, pady=2)
        
        ttk.Button(buttons_row1, text="➕ Novo Produto", command=self.novo_produto_rapido, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_row1, text="✏️ Editar Produto", command=self.editar_produto_selecionado).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_row1, text="🗑️ Remover Produto", command=self.remover_produto_selecionado).pack(side=tk.LEFT, padx=5)
        
        # Segunda linha de botões
        buttons_row2 = ttk.Frame(buttons_frame)
        buttons_row2.pack(fill=tk.X, pady=2)
        
        ttk.Button(buttons_row2, text="📦 Ajustar Estoque", command=self.ajustar_estoque_produto).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_row2, text="🔄 Ativar/Desativar", command=self.toggle_produto_ativo).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_row2, text="📊 Relatório Estoque", command=self.gerar_relatorio_estoque).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_row2, text="🔄 Atualizar", command=self.carregar_produtos).pack(side=tk.RIGHT, padx=5)

    def create_pedidos_tab(self):
        """Cria aba de pedidos"""
        pedidos_frame = ttk.Frame(self.notebook)
        self.notebook.add(pedidos_frame, text="🚚 Pedidos")
        
        # Adicionar widgets para a aba de pedidos aqui
        self.pedidos_tree = ttk.Treeview(pedidos_frame, columns=("ID", "Cliente", "Total", "Status"), show="headings")
        self.pedidos_tree.heading("ID", text="ID")
        self.pedidos_tree.heading("Cliente", text="Cliente")
        self.pedidos_tree.heading("Total", text="Total")
        self.pedidos_tree.heading("Status", text="Status")
        self.pedidos_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        buttons_frame = ttk.Frame(pedidos_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Novo Pedido", command=self.novo_pedido_rapido).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Ver Detalhes", command=self.ver_detalhes_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Alterar Status", command=self.alterar_status_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancelar Pedido", command=self.cancelar_pedido_selecionado).pack(side=tk.LEFT, padx=5)

    def create_cotacoes_tab(self):
        """Cria aba de cotações"""
        cotacoes_frame = ttk.Frame(self.notebook)
        self.notebook.add(cotacoes_frame, text="💰 Cotações")
        
        # Frame superior com filtros e botões
        top_frame = ttk.Frame(cotacoes_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame de filtros
        filtros_frame = ttk.LabelFrame(top_frame, text="Filtros", padding=10)
        filtros_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Filtro por status
        ttk.Label(filtros_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.filtro_status_cotacao = ttk.Combobox(filtros_frame, values=["Todos", "Pendente", "Aprovada", "Rejeitada", "Expirada"], 
                                                 state="readonly", width=15)
        self.filtro_status_cotacao.set("Todos")
        self.filtro_status_cotacao.pack(side=tk.LEFT, padx=5)
        self.filtro_status_cotacao.bind('<<ComboboxSelected>>', lambda e: self.carregar_cotacoes())
        
        # Frame de botões
        botoes_frame = ttk.Frame(top_frame)
        botoes_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(botoes_frame, text="➕ Nova Cotação", command=self.nova_cotacao).pack(side=tk.LEFT, padx=2)
        ttk.Button(botoes_frame, text="✏️ Editar", command=self.editar_cotacao).pack(side=tk.LEFT, padx=2)
        ttk.Button(botoes_frame, text="👁️ Visualizar", command=self.visualizar_cotacao).pack(side=tk.LEFT, padx=2)
        ttk.Button(botoes_frame, text="🔄 Status", command=self.alterar_status_cotacao).pack(side=tk.LEFT, padx=2)
        ttk.Button(botoes_frame, text="🗑️ Excluir", command=self.excluir_cotacao).pack(side=tk.LEFT, padx=2)
        ttk.Button(botoes_frame, text="🔄 Atualizar", command=self.carregar_cotacoes).pack(side=tk.LEFT, padx=2)
        
        # Frame da tabela
        table_frame = ttk.Frame(cotacoes_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview para cotações
        columns = ("ID", "Cliente", "Data", "Validade", "Status", "Itens", "Total")
        self.cotacoes_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        self.cotacoes_tree.heading("ID", text="ID")
        self.cotacoes_tree.heading("Cliente", text="Cliente")
        self.cotacoes_tree.heading("Data", text="Data")
        self.cotacoes_tree.heading("Validade", text="Validade")
        self.cotacoes_tree.heading("Status", text="Status")
        self.cotacoes_tree.heading("Itens", text="Qtd Itens")
        self.cotacoes_tree.heading("Total", text="Total (R$)")
        
        # Configurar larguras
        self.cotacoes_tree.column("ID", width=50)
        self.cotacoes_tree.column("Cliente", width=200)
        self.cotacoes_tree.column("Data", width=100)
        self.cotacoes_tree.column("Validade", width=100)
        self.cotacoes_tree.column("Status", width=100)
        self.cotacoes_tree.column("Itens", width=80)
        self.cotacoes_tree.column("Total", width=120)
        
        # Scrollbar
        scrollbar_cotacoes = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.cotacoes_tree.yview)
        self.cotacoes_tree.configure(yscrollcommand=scrollbar_cotacoes.set)
        
        # Pack
        self.cotacoes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_cotacoes.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind duplo clique
        self.cotacoes_tree.bind("<Double-1>", lambda e: self.visualizar_cotacao())

    def carregar_cotacoes(self):
        """Carrega cotações na tabela"""
        for item in self.cotacoes_tree.get_children():
            self.cotacoes_tree.delete(item)
        
        # Verificar cotações expiradas
        self.cotacao_manager.verificar_cotacoes_expiradas()
        
        cotacoes = self.cotacao_manager.listar_todas_cotacoes()
        filtro_status = self.filtro_status_cotacao.get()
        
        for cotacao in cotacoes:
            if filtro_status == "Todos" or cotacao.status == filtro_status:
                # Buscar nome do cliente
                cliente = self.cliente_manager.buscar_cliente_por_id(cotacao.id_cliente)
                nome_cliente = cliente.nome if cliente else f"Cliente {cotacao.id_cliente}"
                
                # Calcular data de validade
                data_cotacao = datetime.strptime(cotacao.data_cotacao, "%Y-%m-%d")
                data_validade = data_cotacao + timedelta(days=cotacao.validade_dias)
                
                # Configurar cor baseada no status
                tags = []
                if cotacao.status == "Pendente":
                    tags = ["pendente"]
                elif cotacao.status == "Aprovada":
                    tags = ["aprovada"]
                elif cotacao.status == "Rejeitada":
                    tags = ["rejeitada"]
                elif cotacao.status == "Expirada":
                    tags = ["expirada"]
                
                self.cotacoes_tree.insert("", tk.END, values=(
                    cotacao.id_cotacao,
                    nome_cliente,
                    cotacao.data_cotacao,
                    data_validade.strftime("%Y-%m-%d"),
                    cotacao.status,
                    len(cotacao.itens),
                    f"{cotacao.total:.2f}"
                ), tags=tags)
        
        # Configurar cores das tags
        self.cotacoes_tree.tag_configure("pendente", background="#fff3cd")
        self.cotacoes_tree.tag_configure("aprovada", background="#d4edda")
        self.cotacoes_tree.tag_configure("rejeitada", background="#f8d7da")
        self.cotacoes_tree.tag_configure("expirada", background="#e2e3e5")

    def nova_cotacao(self):
        """Abre diálogo para nova cotação"""
        from gui_dialogs import CotacaoDialog
        dialog = CotacaoDialog(self.root, self.cotacao_manager, self.cliente_manager, self.produto_manager)
        if dialog.result:
            self.carregar_cotacoes()
            self.atualizar_dashboard()

    def editar_cotacao(self):
        """Edita cotação selecionada"""
        selection = self.cotacoes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma cotação para editar.")
            return
        
        item = self.cotacoes_tree.item(selection[0])
        id_cotacao = int(item['values'][0])
        
        from gui_dialogs import CotacaoDialog
        dialog = CotacaoDialog(self.root, self.cotacao_manager, self.cliente_manager, 
                              self.produto_manager, id_cotacao)
        if dialog.result:
            self.carregar_cotacoes()
            self.atualizar_dashboard()

    def visualizar_cotacao(self):
        """Visualiza cotação selecionada"""
        selection = self.cotacoes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma cotação para visualizar.")
            return
        
        item = self.cotacoes_tree.item(selection[0])
        id_cotacao = int(item['values'][0])
        
        from gui_dialogs import VisualizarCotacaoDialog
        VisualizarCotacaoDialog(self.root, self.cotacao_manager, self.cliente_manager, id_cotacao)

    def alterar_status_cotacao(self):
        """Altera status da cotação selecionada"""
        selection = self.cotacoes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma cotação para alterar o status.")
            return
        
        item = self.cotacoes_tree.item(selection[0])
        id_cotacao = int(item['values'][0])
        status_atual = item['values'][4]
        
        # Diálogo para escolher novo status
        dialog = tk.Toplevel(self.root)
        dialog.title("Alterar Status")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        ttk.Label(dialog, text=f"Status atual: {status_atual}").pack(pady=10)
        ttk.Label(dialog, text="Novo status:").pack()
        
        status_var = tk.StringVar(value=status_atual)
        status_combo = ttk.Combobox(dialog, textvariable=status_var, 
                                   values=["Pendente", "Aprovada", "Rejeitada", "Expirada"],
                                   state="readonly")
        status_combo.pack(pady=5)
        
        def confirmar():
            novo_status = status_var.get()
            if self.cotacao_manager.alterar_status_cotacao(id_cotacao, novo_status):
                messagebox.showinfo("Sucesso", "Status alterado com sucesso!")
                self.carregar_cotacoes()
                self.atualizar_dashboard()
                dialog.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao alterar status.")
        
        ttk.Button(dialog, text="Confirmar", command=confirmar).pack(pady=10)

    def excluir_cotacao(self):
        """Exclui cotação selecionada"""
        selection = self.cotacoes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma cotação para excluir.")
            return
        
        item = self.cotacoes_tree.item(selection[0])
        id_cotacao = int(item['values'][0])
        cliente_nome = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir a cotação #{id_cotacao} do cliente {cliente_nome}?"):
            if self.cotacao_manager.excluir_cotacao(id_cotacao):
                messagebox.showinfo("Sucesso", "Cotação excluída com sucesso!")
                self.carregar_cotacoes()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", "Erro ao excluir cotação.")

    def create_graficos_tab(self):
        """Cria aba de gráficos e análises"""
        graficos_frame = ttk.Frame(self.notebook)
        self.notebook.add(graficos_frame, text="📊 Gráficos")
        
        # Frame de controles
        controls_frame = ttk.Frame(graficos_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Vendas por Período", 
                  command=self.grafico_vendas_periodo).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Produtos Mais Vendidos", 
                  command=self.grafico_produtos_vendidos).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Status dos Pedidos", 
                  command=self.grafico_status_pedidos).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Clientes por Mês", 
                  command=self.grafico_clientes_mes).pack(side=tk.LEFT, padx=5)
        
        # Frame para o gráfico
        self.grafico_frame = ttk.Frame(graficos_frame)
        self.grafico_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Mensagem inicial
        ttk.Label(self.grafico_frame, text="Selecione um tipo de gráfico acima", 
                 font=('Arial', 12)).pack(expand=True)

    def grafico_vendas_periodo(self):
        """Gera gráfico de vendas por período"""
        self.limpar_grafico_frame()
        
        # Obter pedidos dos últimos 30 dias
        pedidos = self.pedido_manager.listar_todos_pedidos()
        data_limite = datetime.now() - timedelta(days=30)
        
        vendas_por_dia = defaultdict(float)
        for pedido in pedidos:
            if pedido.data_pedido >= data_limite and pedido.status != StatusPedido.CANCELADO:
                data_str = pedido.data_pedido.strftime('%Y-%m-%d')
                vendas_por_dia[data_str] += pedido.total
        
        if not vendas_por_dia:
            ttk.Label(self.grafico_frame, text="Nenhuma venda encontrada nos últimos 30 dias").pack(expand=True)
            return
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        datas = sorted(vendas_por_dia.keys())
        valores = [vendas_por_dia[data] for data in datas]
        datas_obj = [datetime.strptime(data, '%Y-%m-%d') for data in datas]
        
        ax.plot(datas_obj, valores, marker='o', linewidth=2, markersize=6)
        ax.set_title('Vendas por Período (Últimos 30 dias)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor (R$)')
        ax.grid(True, alpha=0.3)
        
        # Formatar eixo x
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=5))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Adicionar ao tkinter
        canvas = FigureCanvasTkAgg(fig, self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def grafico_produtos_vendidos(self):
        """Gera gráfico de produtos mais vendidos"""
        self.limpar_grafico_frame()
        
        pedidos = self.pedido_manager.listar_todos_pedidos()
        produtos_vendidos = defaultdict(int)
        
        for pedido in pedidos:
            if pedido.status != StatusPedido.CANCELADO:
                for item in pedido.itens:
                    # Corrigindo referência de produto.id_produto ao invés de produto_id
                    produto = self.produto_manager.buscar_produto_por_id(item.produto.id_produto)
                    if produto:
                        produtos_vendidos[produto.nome] += item.quantidade
        
        if not produtos_vendidos:
            ttk.Label(self.grafico_frame, text="Nenhum produto vendido encontrado").pack(expand=True)
            return
        
        # Top 10 produtos
        top_produtos = sorted(produtos_vendidos.items(), key=lambda x: x[1], reverse=True)[:10]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        nomes = [item[0][:20] + '...' if len(item[0]) > 20 else item[0] for item in top_produtos]
        quantidades = [item[1] for item in top_produtos]
        
        bars = ax.bar(range(len(nomes)), quantidades, color='skyblue', edgecolor='navy', alpha=0.7)
        ax.set_title('Top 10 Produtos Mais Vendidos', fontsize=14, fontweight='bold')
        ax.set_xlabel('Produtos')
        ax.set_ylabel('Quantidade Vendida')
        ax.set_xticks(range(len(nomes)))
        ax.set_xticklabels(nomes, rotation=45, ha='right')
        
        # Adicionar valores nas barras
        for bar, quantidade in zip(bars, quantidades):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(quantidade)}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def grafico_status_pedidos(self):
        """Gera gráfico de status dos pedidos"""
        self.limpar_grafico_frame()
        
        pedidos = self.pedido_manager.listar_todos_pedidos()
        status_count = Counter([pedido.status.value for pedido in pedidos])
        
        if not status_count:
            ttk.Label(self.grafico_frame, text="Nenhum pedido encontrado").pack(expand=True)
            return
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        labels = list(status_count.keys())
        sizes = list(status_count.values())
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors[:len(labels)], 
                                         autopct='%1.1f%%', startangle=90)
        
        ax.set_title('Distribuição de Status dos Pedidos', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def grafico_clientes_mes(self):
        """Gera gráfico de novos clientes por mês"""
        self.limpar_grafico_frame()
        
        clientes = self.cliente_manager.listar_todos_clientes()
        clientes_por_mes = defaultdict(int)
        
        for cliente in clientes:
            mes_ano = cliente.data_cadastro.strftime('%Y-%m')
            clientes_por_mes[mes_ano] += 1
        
        if not clientes_por_mes:
            ttk.Label(self.grafico_frame, text="Nenhum cliente encontrado").pack(expand=True)
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        meses = sorted(clientes_por_mes.keys())[-12:]  # Últimos 12 meses
        quantidades = [clientes_por_mes[mes] for mes in meses]
        meses_formatados = [datetime.strptime(mes, '%Y-%m').strftime('%m/%Y') for mes in meses]
        
        bars = ax.bar(meses_formatados, quantidades, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
        ax.set_title('Novos Clientes por Mês', fontsize=14, fontweight='bold')
        ax.set_xlabel('Mês/Ano')
        ax.set_ylabel('Número de Clientes')
        
        # Adicionar valores nas barras
        for bar, quantidade in zip(bars, quantidades):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(quantidade)}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def limpar_grafico_frame(self):
        """Limpa o frame de gráficos"""
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

    def create_relatorios_tab(self):
        """Cria aba de relatórios"""
        relatorios_frame = ttk.Frame(self.notebook)
        self.notebook.add(relatorios_frame, text="📝 Relatórios")
        
        # Frame de controles
        controls_frame = ttk.Frame(relatorios_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Relatório de Vendas (7 dias)", 
                  command=lambda: self.gerar_relatorio_vendas(7)).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Relatório de Vendas (30 dias)", 
                  command=lambda: self.gerar_relatorio_vendas(30)).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Relatório de Estoque", 
                  command=self.gerar_relatorio_estoque).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Estatísticas de Clientes", 
                  command=self.gerar_estatisticas_clientes).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Estatísticas de Produtos", 
                  command=self.gerar_estatisticas_produtos).pack(side=tk.LEFT, padx=5)
        
        # Frame para o relatório
        self.relatorio_frame = ttk.Frame(relatorios_frame)
        self.relatorio_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Text widget para exibir relatórios
        self.relatorio_text = tk.Text(self.relatorio_frame, wrap=tk.WORD)
        self.relatorio_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para o text widget
        scrollbar = ttk.Scrollbar(self.relatorio_frame, orient=tk.VERTICAL, command=self.relatorio_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.relatorio_text.config(yscrollcommand=scrollbar.set)

    def gerar_relatorio_vendas(self, dias):
        """Gera relatório de vendas"""
        try:
            relatorio = self.pedido_manager.gerar_relatorio_vendas(dias)
            self.relatorio_text.delete(1.0, tk.END)
            self.relatorio_text.insert(1.0, relatorio)
            self.update_status(f"Relatório de vendas ({dias} dias) gerado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_relatorio_estoque(self):
        """Gera relatório de estoque"""
        try:
            relatorio = self.produto_manager.gerar_relatorio_estoque()
            self.relatorio_text.delete(1.0, tk.END)
            self.relatorio_text.insert(1.0, relatorio)
            self.update_status("Relatório de estoque gerado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_estatisticas_clientes(self):
        """Gera estatísticas de clientes"""
        try:
            stats = self.cliente_manager.obter_estatisticas_clientes()
            
            relatorio = "=== ESTATÍSTICAS DE CLIENTES ===\n\n"
            relatorio += f"Total de clientes: {stats['total_clientes']}\n"
            relatorio += f"Clientes com pedidos: {stats['clientes_com_pedidos']}\n"
            relatorio += f"Clientes sem pedidos: {stats['clientes_sem_pedidos']}\n\n"
            
            if stats['cliente_mais_pedidos']['cliente']:
                relatorio += f"Cliente com mais pedidos: {stats['cliente_mais_pedidos']['cliente']} "
                relatorio += f"({stats['cliente_mais_pedidos']['quantidade_pedidos']} pedidos)\n"
            
            if stats['cliente_maior_valor']['cliente']:
                relatorio += f"Cliente com maior valor: {stats['cliente_maior_valor']['cliente']} "
                relatorio += f"(R$ {stats['cliente_maior_valor']['valor_total']:.2f})\n"
            
            self.relatorio_text.delete(1.0, tk.END)
            self.relatorio_text.insert(1.0, relatorio)
            self.update_status("Estatísticas de clientes geradas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar estatísticas: {str(e)}")
    
    def gerar_estatisticas_produtos(self):
        """Gera estatísticas de produtos"""
        try:
            stats = self.produto_manager.obter_estatisticas_produtos()
            
            relatorio = "=== ESTATÍSTICAS DE PRODUTOS ===\n\n"
            relatorio += f"Total de produtos: {stats['total_produtos']}\n"
            relatorio += f"Produtos ativos: {stats['produtos_ativos']}\n"
            relatorio += f"Produtos inativos: {stats['produtos_inativos']}\n"
            relatorio += f"Produtos sem estoque: {stats['produtos_sem_estoque']}\n"
            relatorio += f"Produtos com estoque baixo: {stats['produtos_estoque_baixo']}\n"
            relatorio += f"Valor total do estoque: R$ {stats['valor_total_estoque']:.2f}\n\n"
            
            if stats['produto_mais_vendido']['produto']:
                relatorio += f"Produto mais vendido: {stats['produto_mais_vendido']['produto']} "
                relatorio += f"({stats['produto_mais_vendido']['quantidade_vendida']} unidades)\n"
            
            if stats['produto_mais_caro']['produto']:
                relatorio += f"Produto mais caro: {stats['produto_mais_caro']['produto']} "
                relatorio += f"(R$ {stats['produto_mais_caro']['preco']:.2f})\n"
            
            if stats['produto_mais_barato']['produto']:
                relatorio += f"Produto mais barato: {stats['produto_mais_barato']['produto']} "
                relatorio += f"(R$ {stats['produto_mais_barato']['preco']:.2f})\n"
            
            self.relatorio_text.delete(1.0, tk.END)
            self.relatorio_text.insert(1.0, relatorio)
            self.update_status("Estatísticas de produtos geradas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar estatísticas: {str(e)}")

    # Métodos de ação rápida
    def novo_cliente_rapido(self):
        """Abre formulário de novo cliente e muda para aba clientes"""
        self.notebook.select(1)  # Aba clientes
        self.abrir_form_cliente()
    
    def novo_produto_rapido(self):
        """Abre formulário de novo produto e muda para aba produtos"""
        self.notebook.select(2)  # Aba produtos
        self.abrir_form_produto()
    
    def novo_pedido_rapido(self):
        """Abre formulário de novo pedido e muda para aba pedidos"""
        self.notebook.select(3)  # Aba pedidos
        self.abrir_form_pedido()
    
    def atualizar_todos_dados(self):
        """Atualiza todos os dados das abas"""
        self.carregar_dados_iniciais()
        messagebox.showinfo("Sucesso", "Todos os dados foram atualizados!")
    
    # Métodos de formulários (serão implementados nos próximos arquivos)
    def abrir_form_cliente(self, cliente=None):
        """Abre formulário de cliente"""
        from gui_forms import ClienteForm
        form = ClienteForm(self.root, self.cliente_manager, cliente)
        if form.resultado:
            self.carregar_clientes()
            self.atualizar_dashboard()
    
    def abrir_form_produto(self, produto=None):
        """Abre formulário de produto"""
        from gui_forms import ProdutoForm
        form = ProdutoForm(self.root, self.produto_manager, produto)
        if form.resultado:
            self.carregar_produtos()
            self.atualizar_dashboard()
    
    def abrir_form_pedido(self, pedido=None):
        """Abre formulário de pedido"""
        from gui_forms import PedidoForm
        form = PedidoForm(self.root, self.pedido_manager, self.cliente_manager, self.produto_manager, pedido)
        if form.resultado:
            self.carregar_pedidos()
            self.atualizar_dashboard()
    
    # Métodos de edição
    def editar_cliente_selecionado(self):
        """Edita cliente selecionado"""
        selection = self.clientes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar")
            return
        
        item = self.clientes_tree.item(selection[0])
        id_cliente = int(item['values'][0])
        cliente = self.cliente_manager.buscar_cliente_por_id(id_cliente)
        
        if cliente:
            self.abrir_form_cliente(cliente)
    
    def editar_produto_selecionado(self):
        """Edita produto selecionado"""
        selection = self.produtos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para editar")
            return
        
        item = self.produtos_tree.item(selection[0])
        id_produto = int(item['values'][0])
        produto = self.produto_manager.buscar_produto_por_id(id_produto)
        
        if produto:
            self.abrir_form_produto(produto)
    
    # Métodos de remoção
    def remover_cliente_selecionado(self):
        """Remove cliente selecionado"""
        selection = self.clientes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente para remover")
            return
        
        item = self.clientes_tree.item(selection[0])
        id_cliente = int(item['values'][0])
        nome_cliente = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente remover o cliente {nome_cliente}?"):
            sucesso, mensagem = self.cliente_manager.remover_cliente(id_cliente)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.carregar_clientes()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", mensagem)
    
    # Métodos específicos de produtos
    def ajustar_estoque_produto(self):
        """Ajusta estoque do produto selecionado"""
        selection = self.produtos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para ajustar estoque")
            return
        
        item = self.produtos_tree.item(selection[0])
        id_produto = int(item['values'][0])
        nome_produto = item['values'][1]
        
        # Dialog para ajuste de estoque
        from gui_dialogs import EstoqueDialog
        dialog = EstoqueDialog(self.root, nome_produto)
        
        if dialog.resultado:
            operacao, quantidade = dialog.resultado
            sucesso, mensagem = self.produto_manager.ajustar_estoque(id_produto, quantidade, operacao)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.carregar_produtos()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", mensagem)
    
    def toggle_produto_ativo(self):
        """Ativa/desativa produto selecionado"""
        selection = self.produtos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto")
            return
        
        item = self.produtos_tree.item(selection[0])
        id_produto = int(item['values'][0])
        produto = self.produto_manager.buscar_produto_por_id(id_produto)
        
        if produto:
            if produto.ativo:
                sucesso, mensagem = self.produto_manager.desativar_produto(id_produto)
            else:
                sucesso, mensagem = self.produto_manager.ativar_produto(id_produto)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.carregar_produtos()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", mensagem)
    
    # Métodos específicos de pedidos
    def ver_detalhes_pedido(self):
        """Mostra detalhes do pedido selecionado"""
        selection = self.pedidos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um pedido")
            return
        
        item = self.pedidos_tree.item(selection[0])
        id_pedido = int(item['values'][0])
        pedido = self.pedido_manager.buscar_pedido_por_id(id_pedido)
        
        if pedido:
            from gui_dialogs import DetalhesPedidoDialog
            DetalhesPedidoDialog(self.root, pedido)
    
    def alterar_status_pedido(self):
        """Altera status do pedido selecionado"""
        selection = self.pedidos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um pedido")
            return
        
        item = self.pedidos_tree.item(selection[0])
        id_pedido = int(item['values'][0])
        pedido = self.pedido_manager.buscar_pedido_por_id(id_pedido)
        
        if pedido:
            from gui_dialogs import StatusPedidoDialog
            dialog = StatusPedidoDialog(self.root, pedido)
            
            if dialog.resultado:
                novo_status = dialog.resultado
                sucesso, mensagem = self.pedido_manager.alterar_status_pedido(id_pedido, novo_status)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.carregar_pedidos()
                    self.atualizar_dashboard()
                else:
                    messagebox.showerror("Erro", mensagem)
    
    def cancelar_pedido_selecionado(self):
        """Cancela pedido selecionado"""
        selection = self.pedidos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um pedido")
            return
        
        item = self.pedidos_tree.item(selection[0])
        id_pedido = int(item['values'][0])
        
        motivo = simpledialog.askstring("Cancelar Pedido", "Motivo do cancelamento (opcional):")
        if motivo is not None:  # None se cancelou o dialog
            sucesso, mensagem = self.pedido_manager.cancelar_pedido(id_pedido, motivo)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.carregar_pedidos()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", mensagem)

    def carregar_dados_iniciais(self):
        """Carrega dados iniciais nas tabelas"""
        self.carregar_clientes()
        self.carregar_produtos()
        self.carregar_pedidos()
        self.carregar_cotacoes()
        self.atualizar_dashboard()

    def carregar_clientes(self):
        """Carrega clientes na tabela"""
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        # Corrigindo método para listar_todos_clientes
        clientes = self.cliente_manager.listar_todos_clientes()
        for cliente in clientes:
            # Usando id_cliente ao invés de id
            self.clientes_tree.insert("", tk.END, values=(cliente.id_cliente, cliente.nome, cliente.email))
    
    def carregar_produtos(self):
        """Carrega produtos na tabela"""
        for item in self.produtos_tree.get_children():
            self.produtos_tree.delete(item)
        
        # Corrigindo método para listar_todos_produtos
        produtos = self.produto_manager.listar_todos_produtos()
        for produto in produtos:
            status_text = "✅ Ativo" if produto.ativo else "❌ Inativo"
            preco_formatado = f"R$ {produto.preco:.2f}"
            estoque_text = str(produto.estoque)
            if produto.estoque <= 5:
                estoque_text = f"⚠️ {produto.estoque}"
            
            categoria = getattr(produto, 'categoria', 'Geral')
            
            item_id = self.produtos_tree.insert("", tk.END, values=(
                produto.id_produto, 
                produto.nome, 
                preco_formatado, 
                estoque_text, 
                status_text, 
                categoria
            ))
            
            # Colorir linhas baseado no status
            if not produto.ativo:
                self.produtos_tree.item(item_id, tags=("inativo",))
            elif produto.estoque <= 5:
                self.produtos_tree.item(item_id, tags=("estoque_baixo",))
        
        # Configurar tags de cores
        self.produtos_tree.tag_configure("inativo", background="#ffebee", foreground="#666666")
        self.produtos_tree.tag_configure("estoque_baixo", background="#fff3e0", foreground="#e65100")
    
    def carregar_pedidos(self):
        """Carrega pedidos na tabela"""
        for item in self.pedidos_tree.get_children():
            self.pedidos_tree.delete(item)
        
        # Corrigindo método para listar_todos_pedidos
        pedidos = self.pedido_manager.listar_todos_pedidos()
        for pedido in pedidos:
            cliente_nome = pedido.cliente.nome
            # Usando id_pedido ao invés de id
            self.pedidos_tree.insert("", tk.END, values=(pedido.id_pedido, cliente_nome, pedido.total, pedido.status.value))

    def update_status(self, message):
        """Atualiza a barra de status"""
        self.status_bar.config(text=message)

    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()

    def mostrar_sobre(self):
        """Mostra informações sobre o sistema"""
        info = """
Sistema de Gestão de Pedidos - Professional Edition
Versão 2.0

Desenvolvido por: Caio
📱 Telefone: (19) 99713-7010
📧 Email: caioh.mega2018@gmail.com
📷 Instagram: @c41oxz
💻 GitHub: caioomega

Para suporte técnico ou dúvidas, entre em contato através dos canais acima.

© 2024 - Todos os direitos reservados
        """
        messagebox.showinfo("Sobre o Sistema", info)

    def backup_dados(self):
        """Realiza backup dos dados"""
        try:
            # Implementar backup aqui
            messagebox.showinfo("Backup", "Funcionalidade de backup será implementada em breve!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer backup: {str(e)}")

    def filtrar_produtos(self):
        """Filtra produtos baseado nos critérios selecionados"""
        for item in self.produtos_tree.get_children():
            self.produtos_tree.delete(item)
        
        produtos = self.produto_manager.listar_todos_produtos()
        status_filter = self.produto_status_filter.get()
        estoque_baixo_filter = self.estoque_baixo_var.get()
        
        for produto in produtos:
            # Filtro por status
            if status_filter == "Ativos" and not produto.ativo:
                continue
            elif status_filter == "Inativos" and produto.ativo:
                continue
            
            # Filtro por estoque baixo
            if estoque_baixo_filter and produto.estoque > 5:
                continue
            
            # Adicionar produto filtrado
            status_text = "✅ Ativo" if produto.ativo else "❌ Inativo"
            preco_formatado = f"R$ {produto.preco:.2f}"
            estoque_text = str(produto.estoque)
            if produto.estoque <= 5:
                estoque_text = f"⚠️ {produto.estoque}"
            
            categoria = getattr(produto, 'categoria', 'Geral')
            
            item_id = self.produtos_tree.insert("", tk.END, values=(
                produto.id_produto, 
                produto.nome, 
                preco_formatado, 
                estoque_text, 
                status_text, 
                categoria
            ))
            
            if not produto.ativo:
                self.produtos_tree.item(item_id, tags=("inativo",))
            elif produto.estoque <= 5:
                self.produtos_tree.item(item_id, tags=("estoque_baixo",))
        
        # Configurar tags de cores
        self.produtos_tree.tag_configure("inativo", background="#ffebee", foreground="#666666")
        self.produtos_tree.tag_configure("estoque_baixo", background="#fff3e0", foreground="#e65100")
    
    def limpar_filtros_produtos(self):
        """Limpa todos os filtros de produtos"""
        self.produto_status_filter.set("Todos")
        self.estoque_baixo_var.set(False)
        self.carregar_produtos()
    
    def remover_produto_selecionado(self):
        """Remove produto selecionado"""
        selection = self.produtos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um produto para remover")
            return
        
        item = self.produtos_tree.item(selection[0])
        id_produto = int(item['values'][0])
        nome_produto = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente remover o produto {nome_produto}?\n\nEsta ação não pode ser desfeita."):
            try:
                sucesso, mensagem = self.produto_manager.remover_produto(id_produto)
                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.carregar_produtos()
                    self.atualizar_dashboard()
                else:
                    messagebox.showerror("Erro", mensagem)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover produto: {str(e)}")

if __name__ == "__main__":
    app = SistemaGestorPedidosGUI()
    app.run()
