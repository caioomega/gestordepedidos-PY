import tkinter as tk
from tkinter import ttk, messagebox
from models import StatusPedido, Pedido, ItemCotacao

class EstoqueDialog:
    def __init__(self, parent, nome_produto):
        self.resultado = None
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title(f"Ajustar Estoque")
        self.window.geometry("450x350")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (350 // 2)
        self.window.geometry(f"450x350+{x}+{y}")
        
        # Configurar estilo
        self.window.configure(bg='#f0f0f0')
        
        self.setup_ui(nome_produto)
        
        # Aguardar fechamento
        self.window.wait_window()
    
    def setup_ui(self, nome_produto):
        """Configura interface do diálogo"""
        # Frame principal com estilo moderno
        main_frame = tk.Frame(self.window, bg='#f0f0f0', padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header com ícone e título
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título principal
        title_label = tk.Label(header_frame, text="📦 Ajustar Estoque", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()
        
        # Nome do produto em destaque
        product_frame = tk.Frame(main_frame, bg='#e3f2fd', relief='solid', bd=1)
        product_frame.pack(fill=tk.X, pady=(0, 25), padx=10)
        
        product_label = tk.Label(product_frame, text=nome_produto, 
                                font=('Segoe UI', 12, 'bold'), 
                                bg='#e3f2fd', fg='#1976d2', pady=10)
        product_label.pack()
        
        # Seção de operação
        operation_frame = tk.LabelFrame(main_frame, text="Tipo de Operação", 
                                       font=('Segoe UI', 10, 'bold'),
                                       bg='#f0f0f0', fg='#34495e', 
                                       padx=15, pady=10)
        operation_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.operacao_var = tk.StringVar(value="adicionar")
        
        # Opções de operação com ícones
        operations = [
            ("adicionar", "➕ Adicionar ao estoque", "#27ae60"),
            ("remover", "➖ Remover do estoque", "#e74c3c"),
            ("definir", "🎯 Definir estoque exato", "#3498db")
        ]
        
        for value, text, color in operations:
            rb = tk.Radiobutton(operation_frame, text=text, 
                               variable=self.operacao_var, value=value,
                               font=('Segoe UI', 10), bg='#f0f0f0', fg=color,
                               selectcolor='#ffffff', activebackground='#f0f0f0',
                               pady=5)
            rb.pack(anchor=tk.W, pady=2)
        
        # Seção de quantidade
        quantity_frame = tk.LabelFrame(main_frame, text="Quantidade", 
                                      font=('Segoe UI', 10, 'bold'),
                                      bg='#f0f0f0', fg='#34495e', 
                                      padx=15, pady=10)
        quantity_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Frame para entrada de quantidade
        entry_frame = tk.Frame(quantity_frame, bg='#f0f0f0')
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.quantidade_var = tk.StringVar()
        quantity_entry = tk.Entry(entry_frame, textvariable=self.quantidade_var, 
                                 font=('Segoe UI', 12), width=15, justify='center',
                                 relief='solid', bd=1)
        quantity_entry.pack(side=tk.LEFT)
        quantity_entry.focus()
        
        # Dica de uso
        hint_label = tk.Label(quantity_frame, text="💡 Digite apenas números inteiros positivos", 
                             font=('Segoe UI', 9), bg='#f0f0f0', fg='#7f8c8d')
        hint_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Botões de ação
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botão Cancelar
        cancel_btn = tk.Button(buttons_frame, text="❌ Cancelar", 
                              command=self.cancelar,
                              font=('Segoe UI', 10, 'bold'),
                              bg='#95a5a6', fg='white', 
                              relief='flat', padx=20, pady=8,
                              cursor='hand2')
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Botão Confirmar
        confirm_btn = tk.Button(buttons_frame, text="✅ Confirmar", 
                               command=self.confirmar,
                               font=('Segoe UI', 10, 'bold'),
                               bg='#27ae60', fg='white', 
                               relief='flat', padx=20, pady=8,
                               cursor='hand2')
        confirm_btn.pack(side=tk.RIGHT)
        
        # Bind Enter para confirmar
        self.window.bind('<Return>', lambda e: self.confirmar())
        self.window.bind('<Escape>', lambda e: self.cancelar())
    
    def confirmar(self):
        """Confirma ajuste de estoque"""
        try:
            quantidade_str = self.quantidade_var.get().strip()
            if not quantidade_str:
                messagebox.showerror("Erro", "⚠️ Por favor, informe a quantidade")
                return
            
            try:
                quantidade = int(quantidade_str)
                if quantidade < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Erro", "⚠️ A quantidade deve ser um número inteiro não negativo")
                return
            
            operacao = self.operacao_var.get()
            
            # Confirmação adicional para operações críticas
            if operacao == "remover" and quantidade > 0:
                if not messagebox.askyesno("Confirmar Remoção", 
                                          f"⚠️ Confirma a remoção de {quantidade} unidades do estoque?"):
                    return
            
            self.resultado = (operacao, quantidade)
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro inesperado: {str(e)}")
    
    def cancelar(self):
        """Cancela operação"""
        self.window.destroy()

class StatusPedidoDialog:
    def __init__(self, parent, pedido):
        self.pedido = pedido
        self.resultado = None
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title(f"Alterar Status - Pedido #{pedido.id_pedido}")
        self.window.geometry("450x350")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (350 // 2)
        self.window.geometry(f"450x350+{x}+{y}")
        
        self.window.configure(bg='#f0f0f0')
        
        self.setup_ui()
        
        # Aguardar fechamento
        self.window.wait_window()
    
    def setup_ui(self):
        """Configura interface do diálogo"""
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#f0f0f0', padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="🔄 Alterar Status do Pedido", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()
        
        # Informações do pedido
        info_frame = tk.Frame(main_frame, bg='#e8f5e8', relief='solid', bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        info_text = f"Pedido #{self.pedido.id_pedido} - {self.pedido.cliente.nome}"
        info_label = tk.Label(info_frame, text=info_text, 
                             font=('Segoe UI', 11, 'bold'), 
                             bg='#e8f5e8', fg='#27ae60', pady=10)
        info_label.pack()
        
        # Status atual
        current_frame = tk.LabelFrame(main_frame, text="Status Atual", 
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='#f0f0f0', fg='#34495e', 
                                     padx=15, pady=10)
        current_frame.pack(fill=tk.X, pady=(0, 20))
        
        current_status = tk.Label(current_frame, text=f"📋 {self.pedido.status.value.upper()}", 
                                 font=('Segoe UI', 12, 'bold'), 
                                 bg='#f0f0f0', fg='#e74c3c')
        current_status.pack(pady=5)
        
        # Novo status
        new_status_frame = tk.LabelFrame(main_frame, text="Novo Status", 
                                        font=('Segoe UI', 10, 'bold'),
                                        bg='#f0f0f0', fg='#34495e', 
                                        padx=15, pady=10)
        new_status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Determinar status possíveis
        status_possiveis = self.get_status_possiveis()
        
        if not status_possiveis:
            no_status_label = tk.Label(new_status_frame, 
                                      text="⚠️ Nenhuma transição de status disponível", 
                                      font=('Segoe UI', 10), bg='#f0f0f0', fg='#e74c3c')
            no_status_label.pack(pady=10)
        else:
            self.status_var = tk.StringVar()
            
            # Mapear status para ícones e cores
            status_icons = {
                'Pendente': ('⏳', '#f39c12'),
                'Processando': ('⚙️', '#3498db'),
                'Enviado': ('🚚', '#9b59b6'),
                'Entregue': ('✅', '#27ae60'),
                'Cancelado': ('❌', '#e74c3c')
            }
            
            for status in status_possiveis:
                icon, color = status_icons.get(status.value, ('📋', '#34495e'))
                text = f"{icon} {status.value.upper()}"
                
                rb = tk.Radiobutton(new_status_frame, text=text, 
                                   variable=self.status_var, value=status.value,
                                   font=('Segoe UI', 11), bg='#f0f0f0', fg=color,
                                   selectcolor='#ffffff', activebackground='#f0f0f0',
                                   pady=5)
                rb.pack(anchor=tk.W, pady=3)
        
        # Botões
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill=tk.X, pady=(15, 0))
        
        cancel_btn = tk.Button(buttons_frame, text="❌ Cancelar", 
                              command=self.cancelar,
                              font=('Segoe UI', 10, 'bold'),
                              bg='#95a5a6', fg='white', 
                              relief='flat', padx=20, pady=8,
                              cursor='hand2')
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        if status_possiveis:
            confirm_btn = tk.Button(buttons_frame, text="✅ Confirmar", 
                                   command=self.confirmar,
                                   font=('Segoe UI', 10, 'bold'),
                                   bg='#27ae60', fg='white', 
                                   relief='flat', padx=20, pady=8,
                                   cursor='hand2')
            confirm_btn.pack(side=tk.RIGHT)
    
    def get_status_possiveis(self):
        """Retorna status possíveis baseado no status atual"""
        transicoes_validas = {
            StatusPedido.PENDENTE: [StatusPedido.PROCESSANDO, StatusPedido.CANCELADO],
            StatusPedido.PROCESSANDO: [StatusPedido.ENVIADO, StatusPedido.CANCELADO],
            StatusPedido.ENVIADO: [StatusPedido.ENTREGUE],
            StatusPedido.ENTREGUE: [],
            StatusPedido.CANCELADO: []
        }
        
        return transicoes_validas.get(self.pedido.status, [])
    
    def confirmar(self):
        """Confirma alteração de status"""
        if not hasattr(self, 'status_var') or not self.status_var.get():
            messagebox.showerror("Erro", "⚠️ Por favor, selecione um status")
            return
        
        novo_status = StatusPedido(self.status_var.get())
        
        # Confirmação adicional para cancelamento
        if novo_status == StatusPedido.CANCELADO:
            if not messagebox.askyesno("Confirmar Cancelamento", 
                                      "⚠️ Confirma o cancelamento deste pedido?\n\nEsta ação não pode ser desfeita."):
                return
        
        self.resultado = novo_status
        self.window.destroy()
    
    def cancelar(self):
        """Cancela operação"""
        self.window.destroy()

class DetalhesPedidoDialog:
    def __init__(self, parent, pedido):
        self.pedido = pedido
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title(f"Detalhes do Pedido #{pedido.id_pedido}")
        self.window.geometry("700x600")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"700x600+{x}+{y}")
        
        self.window.configure(bg='#f0f0f0')
        
        self.setup_ui()
        
        # Aguardar fechamento
        self.window.wait_window()
    
    def setup_ui(self):
        """Configura interface do diálogo"""
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text=f"📋 Pedido #{self.pedido.id_pedido}", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()
        
        # Status badge
        status_colors = {
            'Pendente': '#f39c12',
            'Processando': '#3498db',
            'Enviado': '#9b59b6',
            'Entregue': '#27ae60',
            'Cancelado': '#e74c3c'
        }
        
        status_color = status_colors.get(self.pedido.status.value, '#34495e')
        status_frame = tk.Frame(header_frame, bg=status_color, relief='solid', bd=1)
        status_frame.pack(pady=(5, 0))
        
        status_label = tk.Label(status_frame, text=f"Status: {self.pedido.status.value.upper()}", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg=status_color, fg='white', padx=15, pady=5)
        status_label.pack()
        
        # Informações do pedido
        info_frame = tk.LabelFrame(main_frame, text="📞 Informações do Cliente", 
                                  font=('Segoe UI', 12, 'bold'),
                                  bg='#f0f0f0', fg='#34495e', 
                                  padx=15, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Grid com informações
        info_data = [
            ("👤 Cliente:", self.pedido.cliente.nome),
            ("📧 Email:", self.pedido.cliente.email),
            ("📱 Telefone:", self.pedido.cliente.telefone),
            ("📅 Data do Pedido:", self.pedido.data_pedido.strftime("%d/%m/%Y às %H:%M")),
            ("💰 Total:", f"R$ {self.pedido.total:.2f}")
        ]
        
        for i, (label, value) in enumerate(info_data):
            label_widget = tk.Label(info_frame, text=label, 
                                   font=('Segoe UI', 10, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
            label_widget.grid(row=i, column=0, sticky=tk.W, padx=(0, 15), pady=5)
            
            value_widget = tk.Label(info_frame, text=value, 
                                   font=('Segoe UI', 10), 
                                   bg='#f0f0f0', fg='#34495e')
            value_widget.grid(row=i, column=1, sticky=tk.W, pady=5)
        
        # Observações
        if self.pedido.observacoes:
            obs_frame = tk.LabelFrame(main_frame, text="📝 Observações", 
                                     font=('Segoe UI', 12, 'bold'),
                                     bg='#f0f0f0', fg='#34495e', 
                                     padx=15, pady=10)
            obs_frame.pack(fill=tk.X, pady=(0, 15))
            
            obs_text = tk.Text(obs_frame, height=3, wrap=tk.WORD, 
                              font=('Segoe UI', 10), bg='#ffffff',
                              relief='solid', bd=1)
            obs_text.pack(fill=tk.X, pady=5)
            obs_text.insert(1.0, self.pedido.observacoes)
            obs_text.config(state=tk.DISABLED)
        
        # Itens do pedido
        items_frame = tk.LabelFrame(main_frame, text="🛒 Itens do Pedido", 
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='#f0f0f0', fg='#34495e', 
                                   padx=15, pady=10)
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Treeview para itens com estilo melhorado
        style = ttk.Style()
        style.configure("Details.Treeview", font=('Segoe UI', 10))
        style.configure("Details.Treeview.Heading", font=('Segoe UI', 10, 'bold'))
        
        columns = ("Produto", "Quantidade", "Preço Unit.", "Subtotal")
        items_tree = ttk.Treeview(items_frame, columns=columns, show="headings", 
                                 height=10, style="Details.Treeview")
        
        # Configurar colunas
        column_widths = {"Produto": 300, "Quantidade": 100, "Preço Unit.": 120, "Subtotal": 120}
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=column_widths[col], anchor=tk.CENTER if col != "Produto" else tk.W)
        
        # Scrollbar
        items_scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=items_tree.yview)
        items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        # Carregar itens
        for item in self.pedido.itens:
            items_tree.insert("", tk.END, values=(
                item.produto.nome,
                f"{item.quantidade} un",
                f"R$ {item.preco_unitario:.2f}",
                f"R$ {item.subtotal:.2f}"
            ))
        
        items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Botão fechar
        close_btn = tk.Button(main_frame, text="✅ Fechar", 
                             command=self.window.destroy,
                             font=('Segoe UI', 11, 'bold'),
                             bg='#3498db', fg='white', 
                             relief='flat', padx=30, pady=10,
                             cursor='hand2')
        close_btn.pack(pady=(15, 0))
        
        # Bind Escape para fechar
        self.window.bind('<Escape>', lambda e: self.window.destroy())

class CotacaoDialog:
    def __init__(self, parent, cotacao_manager, cliente_manager, produto_manager, id_cotacao=None):
        self.cotacao_manager = cotacao_manager
        self.cliente_manager = cliente_manager
        self.produto_manager = produto_manager
        self.id_cotacao = id_cotacao
        self.result = None
        self.itens_cotacao = []
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Nova Cotação" if not id_cotacao else "Editar Cotação")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"900x700+{x}+{y}")
        
        self.window.configure(bg='#f0f0f0')
        
        # Carregar dados se editando
        if self.id_cotacao:
            self.cotacao_atual = self.cotacao_manager.buscar_cotacao(self.id_cotacao)
            if self.cotacao_atual:
                self.itens_cotacao = self.cotacao_atual.itens.copy()
        
        self.setup_ui()
        
        # Aguardar fechamento
        self.window.wait_window()
    
    def setup_ui(self):
        """Configura interface do diálogo"""
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = "📋 Nova Cotação" if not self.id_cotacao else "✏️ Editar Cotação"
        title_label = tk.Label(header_frame, text=title, 
                              font=('Segoe UI', 18, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()
        
        # Frame de dados básicos
        dados_frame = tk.LabelFrame(main_frame, text="📞 Dados da Cotação", 
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='#f0f0f0', fg='#34495e', 
                                   padx=15, pady=10)
        dados_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Cliente
        tk.Label(dados_frame, text="Cliente:", font=('Segoe UI', 10, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        
        self.cliente_var = tk.StringVar()
        cliente_combo = ttk.Combobox(dados_frame, textvariable=self.cliente_var, 
                                    font=('Segoe UI', 10), width=40, state="readonly")
        
        # Carregar clientes
        clientes = self.cliente_manager.listar_todos_clientes()
        cliente_values = [f"{c.id_cliente} - {c.nome}" for c in clientes]
        cliente_combo['values'] = cliente_values
        cliente_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Observações
        tk.Label(dados_frame, text="Observações:", font=('Segoe UI', 10, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').grid(row=1, column=0, sticky=tk.NW, padx=(0, 10), pady=5)
        
        self.observacoes_text = tk.Text(dados_frame, height=3, width=50, 
                                       font=('Segoe UI', 10), wrap=tk.WORD)
        self.observacoes_text.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Frame de itens
        itens_frame = tk.LabelFrame(main_frame, text="🛒 Itens da Cotação", 
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='#f0f0f0', fg='#34495e', 
                                   padx=15, pady=10)
        itens_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Botões de item
        botoes_item_frame = tk.Frame(itens_frame, bg='#f0f0f0')
        botoes_item_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(botoes_item_frame, text="➕ Adicionar Item", 
                 command=self.adicionar_item,
                 font=('Segoe UI', 10, 'bold'),
                 bg='#27ae60', fg='white', 
                 relief='flat', padx=15, pady=5,
                 cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(botoes_item_frame, text="🗑️ Remover Item", 
                 command=self.remover_item,
                 font=('Segoe UI', 10, 'bold'),
                 bg='#e74c3c', fg='white', 
                 relief='flat', padx=15, pady=5,
                 cursor='hand2').pack(side=tk.LEFT)
        
        # Treeview para itens
        columns = ("Produto", "Quantidade", "Preço Unit.", "Subtotal")
        self.itens_tree = ttk.Treeview(itens_frame, columns=columns, show="headings", height=8)
        
        # Configurar colunas
        column_widths = {"Produto": 300, "Quantidade": 100, "Preço Unit.": 120, "Subtotal": 120}
        for col in columns:
            self.itens_tree.heading(col, text=col)
            self.itens_tree.column(col, width=column_widths[col], anchor=tk.CENTER if col != "Produto" else tk.W)
        
        # Scrollbar para itens
        itens_scrollbar = ttk.Scrollbar(itens_frame, orient=tk.VERTICAL, command=self.itens_tree.yview)
        self.itens_tree.configure(yscrollcommand=itens_scrollbar.set)
        
        self.itens_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        itens_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Frame de totais
        totais_frame = tk.Frame(main_frame, bg='#f0f0f0')
        totais_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Desconto
        tk.Label(totais_frame, text="Desconto (%):", font=('Segoe UI', 10, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').pack(side=tk.LEFT, padx=(0, 10))
        
        self.desconto_var = tk.StringVar(value="0")
        desconto_entry = tk.Entry(totais_frame, textvariable=self.desconto_var, 
                                 font=('Segoe UI', 10), width=10)
        desconto_entry.pack(side=tk.LEFT, padx=(0, 20))
        desconto_entry.bind('<KeyRelease>', self.atualizar_total)
        
        # Total
        self.total_label = tk.Label(totais_frame, text="Total: R$ 0,00", 
                                   font=('Segoe UI', 14, 'bold'), 
                                   bg='#f0f0f0', fg='#27ae60')
        self.total_label.pack(side=tk.RIGHT)
        
        # Botões finais
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(buttons_frame, text="❌ Cancelar", 
                 command=self.cancelar,
                 font=('Segoe UI', 11, 'bold'),
                 bg='#95a5a6', fg='white', 
                 relief='flat', padx=25, pady=10,
                 cursor='hand2').pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(buttons_frame, text="✅ Salvar Cotação", 
                 command=self.salvar_cotacao,
                 font=('Segoe UI', 11, 'bold'),
                 bg='#3498db', fg='white', 
                 relief='flat', padx=25, pady=10,
                 cursor='hand2').pack(side=tk.RIGHT)
        
        # Carregar dados se editando
        if self.id_cotacao and hasattr(self, 'cotacao_atual'):
            self.carregar_dados_cotacao()
        
        self.atualizar_lista_itens()
    
    def carregar_dados_cotacao(self):
        """Carrega dados da cotação para edição"""
        cotacao = self.cotacao_atual
        
        # Selecionar cliente
        cliente_text = f"{cotacao.cliente.id_cliente} - {cotacao.cliente.nome}"
        self.cliente_var.set(cliente_text)
        
        # Observações
        if cotacao.observacoes:
            self.observacoes_text.insert(1.0, cotacao.observacoes)
        
        # Desconto
        self.desconto_var.set(str(cotacao.desconto))
    
    def adicionar_item(self):
        """Abre diálogo para adicionar item"""
        ItemCotacaoDialog(self.window, self.produto_manager, self.adicionar_item_callback)
    
    def adicionar_item_callback(self, produto_id, quantidade, preco_unitario):
        """Callback para adicionar item à lista"""
        produto = self.produto_manager.buscar_produto(produto_id)
        if produto:
            item = ItemCotacao(produto, quantidade, preco_unitario)
            self.itens_cotacao.append(item)
            self.atualizar_lista_itens()
            self.atualizar_total()
    
    def remover_item(self):
        """Remove item selecionado"""
        selection = self.itens_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return
        
        index = self.itens_tree.index(selection[0])
        del self.itens_cotacao[index]
        self.atualizar_lista_itens()
        self.atualizar_total()
    
    def atualizar_lista_itens(self):
        """Atualiza a lista de itens na treeview"""
        # Limpar itens existentes
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        
        # Adicionar itens
        for item in self.itens_cotacao:
            self.itens_tree.insert("", tk.END, values=(
                item.produto.nome,
                f"{item.quantidade} un",
                f"R$ {item.preco_unitario:.2f}",
                f"R$ {item.subtotal:.2f}"
            ))
    
    def atualizar_total(self, event=None):
        """Atualiza o total da cotação"""
        try:
            desconto = float(self.desconto_var.get() or 0)
            subtotal = sum(item.subtotal for item in self.itens_cotacao)
            total = subtotal * (1 - desconto / 100)
            self.total_label.config(text=f"Total: R$ {total:.2f}")
        except ValueError:
            self.total_label.config(text="Total: R$ 0,00")
    
    def salvar_cotacao(self):
        """Salva a cotação"""
        try:
            # Validações
            if not self.cliente_var.get():
                messagebox.showerror("Erro", "Selecione um cliente.")
                return
            
            if not self.itens_cotacao:
                messagebox.showerror("Erro", "Adicione pelo menos um item à cotação.")
                return
            
            # Extrair ID do cliente
            cliente_id = int(self.cliente_var.get().split(' - ')[0])
            cliente = self.cliente_manager.buscar_cliente(cliente_id)
            
            if not cliente:
                messagebox.showerror("Erro", "Cliente não encontrado.")
                return
            
            # Dados da cotação
            observacoes = self.observacoes_text.get(1.0, tk.END).strip()
            desconto = float(self.desconto_var.get() or 0)
            
            if self.id_cotacao:
                # Editar cotação existente
                success = self.cotacao_manager.editar_cotacao(
                    self.id_cotacao, cliente, self.itens_cotacao, observacoes, desconto
                )
            else:
                # Criar nova cotação
                success = self.cotacao_manager.criar_cotacao(
                    cliente, self.itens_cotacao, observacoes, desconto
                )
            
            if success:
                self.result = True
                messagebox.showinfo("Sucesso", "Cotação salva com sucesso!")
                self.window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao salvar cotação.")
                
        except ValueError as e:
            messagebox.showerror("Erro", f"Dados inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def cancelar(self):
        """Cancela operação"""
        self.window.destroy()

class ItemCotacaoDialog:
    def __init__(self, parent, produto_manager, callback):
        self.produto_manager = produto_manager
        self.callback = callback
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Adicionar Item")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")
        
        self.window.configure(bg='#f0f0f0')
        
        self.setup_ui()
        
        # Aguardar fechamento
        self.window.wait_window()
    
    def setup_ui(self):
        """Configura interface do diálogo"""
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#f0f0f0', padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="➕ Adicionar Item", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()
        
        # Produto
        tk.Label(main_frame, text="Produto:", font=('Segoe UI', 10, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor=tk.W, pady=(0, 5))
        
        self.produto_var = tk.StringVar()
        produto_combo = ttk.Combobox(main_frame, textvariable=self.produto_var, 
                                    font=('Segoe UI', 10), width=50, state="readonly")
        
        # Carregar produtos ativos
        produtos = [p for p in self.produto_manager.listar_todos_produtos() if p.ativo]
        produto_values = [f"{p.id_produto} - {p.nome} (R$ {p.preco:.2f})" for p in produtos]
        produto_combo['values'] = produto_values
        produto_combo.pack(fill=tk.X, pady=(0, 15))
        produto_combo.bind('<<ComboboxSelected>>', self.produto_selecionado)
        
        # Quantidade
        tk.Label(main_frame, text="Quantidade:", font=('Segoe UI', 10, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor=tk.W, pady=(0, 5))
        
        self.quantidade_var = tk.StringVar(value="1")
        quantidade_entry = tk.Entry(main_frame, textvariable=self.quantidade_var, 
                                   font=('Segoe UI', 10))
        quantidade_entry.pack(fill=tk.X, pady=(0, 15))
        quantidade_entry.bind('<KeyRelease>', self.calcular_subtotal)
        
        # Preço unitário
        tk.Label(main_frame, text="Preço Unitário:", font=('Segoe UI', 10, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').pack(anchor=tk.W, pady=(0, 5))
        
        self.preco_var = tk.StringVar()
        preco_entry = tk.Entry(main_frame, textvariable=self.preco_var, 
                              font=('Segoe UI', 10))
        preco_entry.pack(fill=tk.X, pady=(0, 15))
        preco_entry.bind('<KeyRelease>', self.calcular_subtotal)
        
        # Subtotal
        self.subtotal_label = tk.Label(main_frame, text="Subtotal: R$ 0,00", 
                                      font=('Segoe UI', 12, 'bold'), 
                                      bg='#f0f0f0', fg='#27ae60')
        self.subtotal_label.pack(pady=(10, 20))
        
        # Botões
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(buttons_frame, text="❌ Cancelar", 
                 command=self.window.destroy,
                 font=('Segoe UI', 10, 'bold'),
                 bg='#95a5a6', fg='white', 
                 relief='flat', padx=20, pady=8,
                 cursor='hand2').pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(buttons_frame, text="✅ Adicionar", 
                 command=self.adicionar_item,
                 font=('Segoe UI', 10, 'bold'),
                 bg='#27ae60', fg='white', 
                 relief='flat', padx=20, pady=8,
                 cursor='hand2').pack(side=tk.RIGHT)
    
    def produto_selecionado(self, event=None):
        """Preenche preço quando produto é selecionado"""
        if self.produto_var.get():
            produto_id = int(self.produto_var.get().split(' - ')[0])
            produto = self.produto_manager.buscar_produto(produto_id)
            if produto:
                self.preco_var.set(f"{produto.preco:.2f}")
                self.calcular_subtotal()
    
    def calcular_subtotal(self, event=None):
        """Calcula subtotal"""
        try:
            quantidade = float(self.quantidade_var.get() or 0)
            preco = float(self.preco_var.get() or 0)
            subtotal = quantidade * preco
            self.subtotal_label.config(text=f"Subtotal: R$ {subtotal:.2f}")
        except ValueError:
            self.subtotal_label.config(text="Subtotal: R$ 0,00")
    
    def adicionar_item(self):
        """Adiciona item à cotação"""
        try:
            if not self.produto_var.get():
                messagebox.showerror("Erro", "Selecione um produto.")
                return
            
            produto_id = int(self.produto_var.get().split(' - ')[0])
            quantidade = int(self.quantidade_var.get())
            preco_unitario = float(self.preco_var.get())
            
            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero.")
                return
            
            if preco_unitario <= 0:
                messagebox.showerror("Erro", "Preço deve ser maior que zero.")
                return
            
            self.callback(produto_id, quantidade, preco_unitario)
            self.window.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos. Verifique os valores inseridos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
