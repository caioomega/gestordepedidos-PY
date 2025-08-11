import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from models import Cliente, Produto, Pedido, StatusPedido

class ClienteForm:
    def __init__(self, parent, cliente_manager, cliente=None):
        self.cliente_manager = cliente_manager
        self.cliente = cliente
        self.resultado = False
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Cliente" if cliente is None else f"Editar Cliente - {cliente.nome}")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")
        
        self.setup_ui()
        
        if cliente:
            self.carregar_dados_cliente()
        
        # Aguardar fechamento
        self.window.wait_window()
    
    def setup_ui(self):
        """Configura interface do formulário"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = "Novo Cliente" if self.cliente is None else "Editar Cliente"
        ttk.Label(main_frame, text=title, font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Campos do formulário
        # Nome
        ttk.Label(main_frame, text="Nome *:").pack(anchor=tk.W)
        self.nome_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nome_var, width=50).pack(fill=tk.X, pady=(0, 10))
        
        # Email
        ttk.Label(main_frame, text="Email *:").pack(anchor=tk.W)
        self.email_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.email_var, width=50).pack(fill=tk.X, pady=(0, 10))
        
        # Telefone
        ttk.Label(main_frame, text="Telefone *:").pack(anchor=tk.W)
        self.telefone_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.telefone_var, width=50).pack(fill=tk.X, pady=(0, 10))
        
        # Endereço
        ttk.Label(main_frame, text="Endereço *:").pack(anchor=tk.W)
        self.endereco_text = tk.Text(main_frame, height=4, width=50)
        self.endereco_text.pack(fill=tk.X, pady=(0, 10))
        
        # Nota sobre campos obrigatórios
        ttk.Label(main_frame, text="* Campos obrigatórios", 
                 font=('Arial', 8), foreground='gray').pack(anchor=tk.W, pady=(0, 20))
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=self.cancelar).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(buttons_frame, text="Salvar", 
                  command=self.salvar).pack(side=tk.RIGHT)
        
        # Bind Enter para salvar
        self.window.bind('<Return>', lambda e: self.salvar())
        self.window.bind('<Escape>', lambda e: self.cancelar())
    
    def carregar_dados_cliente(self):
        """Carrega dados do cliente para edição"""
        self.nome_var.set(self.cliente.nome)
        self.email_var.set(self.cliente.email)
        self.telefone_var.set(self.cliente.telefone)
        self.endereco_text.insert(1.0, self.cliente.endereco)
    
    def salvar(self):
        """Salva cliente"""
        try:
            # Obter dados
            nome = self.nome_var.get().strip()
            email = self.email_var.get().strip()
            telefone = self.telefone_var.get().strip()
            endereco = self.endereco_text.get(1.0, tk.END).strip()
            
            # Validar campos obrigatórios
            if not all([nome, email, telefone, endereco]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            # Salvar ou atualizar
            if self.cliente is None:
                # Novo cliente
                sucesso, mensagem, cliente_criado = self.cliente_manager.criar_cliente(nome, email, telefone, endereco)
            else:
                # Atualizar cliente
                sucesso, mensagem = self.cliente_manager.atualizar_cliente(
                    self.cliente.id_cliente, nome, email, telefone, endereco)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.resultado = True
                self.window.destroy()
            else:
                messagebox.showerror("Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def cancelar(self):
        """Cancela operação"""
        self.window.destroy()

class ProdutoForm:
    def __init__(self, parent, produto_manager, produto=None):
        self.produto_manager = produto_manager
        self.produto = produto
        self.resultado = False
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Novo Produto" if produto is None else f"Editar Produto - {produto.nome}")
        self.window.geometry("500x450")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (450 // 2)
        self.window.geometry(f"500x450+{x}+{y}")
        
        self.setup_ui()
        
        if produto:
            self.carregar_dados_produto()
        
        # Aguardar fechamento
        self.window.wait_window()
    
    def setup_ui(self):
        """Configura interface do formulário"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = "Novo Produto" if self.produto is None else "Editar Produto"
        ttk.Label(main_frame, text=title, font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Campos do formulário
        # Nome
        ttk.Label(main_frame, text="Nome *:").pack(anchor=tk.W)
        self.nome_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nome_var, width=50).pack(fill=tk.X, pady=(0, 10))
        
        # Descrição
        ttk.Label(main_frame, text="Descrição *:").pack(anchor=tk.W)
        self.descricao_text = tk.Text(main_frame, height=4, width=50)
        self.descricao_text.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para preço e estoque
        price_stock_frame = ttk.Frame(main_frame)
        price_stock_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Preço
        price_frame = ttk.Frame(price_stock_frame)
        price_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(price_frame, text="Preço (R$) *:").pack(anchor=tk.W)
        self.preco_var = tk.StringVar()
        ttk.Entry(price_frame, textvariable=self.preco_var, width=20).pack(anchor=tk.W)
        
        # Estoque
        stock_frame = ttk.Frame(price_stock_frame)
        stock_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        ttk.Label(stock_frame, text="Estoque *:").pack(anchor=tk.W)
        self.estoque_var = tk.StringVar()
        ttk.Entry(stock_frame, textvariable=self.estoque_var, width=20).pack(anchor=tk.W)
        
        # Status (apenas para edição)
        if self.produto is not None:
            ttk.Label(main_frame, text="Status:").pack(anchor=tk.W, pady=(10, 0))
            self.ativo_var = tk.BooleanVar()
            ttk.Checkbutton(main_frame, text="Produto ativo", 
                           variable=self.ativo_var).pack(anchor=tk.W, pady=(0, 10))
        
        # Nota sobre campos obrigatórios
        ttk.Label(main_frame, text="* Campos obrigatórios", 
                 font=('Arial', 8), foreground='gray').pack(anchor=tk.W, pady=(10, 20))
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=self.cancelar).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(buttons_frame, text="Salvar", 
                  command=self.salvar).pack(side=tk.RIGHT)
        
        # Bind Enter para salvar
        self.window.bind('<Return>', lambda e: self.salvar())
        self.window.bind('<Escape>', lambda e: self.cancelar())
    
    def carregar_dados_produto(self):
        """Carrega dados do produto para edição"""
        self.nome_var.set(self.produto.nome)
        self.descricao_text.insert(1.0, self.produto.descricao)
        self.preco_var.set(str(self.produto.preco))
        self.estoque_var.set(str(self.produto.estoque))
        if hasattr(self, 'ativo_var'):
            self.ativo_var.set(self.produto.ativo)
    
    def salvar(self):
        """Salva produto"""
        try:
            # Obter dados
            nome = self.nome_var.get().strip()
            descricao = self.descricao_text.get(1.0, tk.END).strip()
            preco_str = self.preco_var.get().strip()
            estoque_str = self.estoque_var.get().strip()
            
            # Validar campos obrigatórios
            if not all([nome, descricao, preco_str, estoque_str]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            # Validar e converter números
            try:
                preco = float(preco_str.replace(',', '.'))
                estoque = int(estoque_str)
            except ValueError:
                messagebox.showerror("Erro", "Preço deve ser um número válido e estoque deve ser um número inteiro!")
                return
            
            # Salvar ou atualizar
            if self.produto is None:
                # Novo produto
                sucesso, mensagem, produto_criado = self.produto_manager.criar_produto(nome, descricao, preco, estoque)
            else:
                # Atualizar produto
                sucesso, mensagem = self.produto_manager.atualizar_produto(
                    self.produto.id_produto, nome, descricao, preco, estoque)
                
                # Atualizar status se necessário
                if hasattr(self, 'ativo_var') and sucesso:
                    ativo_desejado = self.ativo_var.get()
                    if ativo_desejado != self.produto.ativo:
                        if ativo_desejado:
                            self.produto_manager.ativar_produto(self.produto.id_produto)
                        else:
                            self.produto_manager.desativar_produto(self.produto.id_produto)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.resultado = True
                self.window.destroy()
            else:
                messagebox.showerror("Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def cancelar(self):
        """Cancela operação"""
        self.window.destroy()

class PedidoForm:
    def __init__(self, parent, pedido_manager, cliente_manager, produto_manager, pedido=None):
        self.pedido_manager = pedido_manager
        self.cliente_manager = cliente_manager
        self.produto_manager = produto_manager
        self.pedido = pedido
        self.resultado = False
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Novo Pedido" if pedido is None else f"Editar Pedido #{pedido.id_pedido}")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"800x600+{x}+{y}")
        
        self.setup_ui()
        
        if pedido:
            self.carregar_dados_pedido()
        
        self.carregar_clientes()
        self.carregar_produtos()
        
        # Aguardar fechamento
        self.window.wait_window()
    
    def setup_ui(self):
        """Configura interface do formulário"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = "Novo Pedido" if self.pedido is None else f"Editar Pedido #{self.pedido.id_pedido}"
        ttk.Label(main_frame, text=title, font=('Arial', 14, 'bold')).pack(pady=(0, 10))
        
        # Frame superior - dados do pedido
        top_frame = ttk.LabelFrame(main_frame, text="Dados do Pedido", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Cliente
        client_frame = ttk.Frame(top_frame)
        client_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(client_frame, text="Cliente *:").pack(side=tk.LEFT)
        self.cliente_var = tk.StringVar()
        self.cliente_combo = ttk.Combobox(client_frame, textvariable=self.cliente_var, 
                                         state="readonly", width=40)
        self.cliente_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Observações
        ttk.Label(top_frame, text="Observações:").pack(anchor=tk.W)
        self.observacoes_text = tk.Text(top_frame, height=3)
        self.observacoes_text.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para itens do pedido
        items_frame = ttk.LabelFrame(main_frame, text="Itens do Pedido", padding=10)
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame para adicionar item
        add_item_frame = ttk.Frame(items_frame)
        add_item_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(add_item_frame, text="Produto:").pack(side=tk.LEFT)
        self.produto_var = tk.StringVar()
        self.produto_combo = ttk.Combobox(add_item_frame, textvariable=self.produto_var, 
                                         state="readonly", width=30)
        self.produto_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(add_item_frame, text="Qtd:").pack(side=tk.LEFT)
        self.quantidade_var = tk.StringVar(value="1")
        ttk.Entry(add_item_frame, textvariable=self.quantidade_var, width=5).pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(add_item_frame, text="Adicionar Item", 
                  command=self.adicionar_item).pack(side=tk.LEFT, padx=(10, 0))
        
        # Treeview para itens
        columns = ("Produto", "Quantidade", "Preço Unit.", "Subtotal")
        self.itens_tree = ttk.Treeview(items_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.itens_tree.heading(col, text=col)
            if col == "Produto":
                self.itens_tree.column(col, width=300)
            else:
                self.itens_tree.column(col, width=100)
        
        # Scrollbar para itens
        items_scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.itens_tree.yview)
        self.itens_tree.configure(yscrollcommand=items_scrollbar.set)
        
        self.itens_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão para remover item
        ttk.Button(items_frame, text="Remover Item Selecionado", 
                  command=self.remover_item).pack(pady=(10, 0))
        
        # Frame inferior - total e botões
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X)
        
        # Total
        total_frame = ttk.Frame(bottom_frame)
        total_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(total_frame, text="TOTAL:", font=('Arial', 12, 'bold')).pack(side=tk.RIGHT, padx=(10, 0))
        self.total_label = ttk.Label(total_frame, text="R$ 0,00", font=('Arial', 12, 'bold'))
        self.total_label.pack(side=tk.RIGHT)
        
        # Botões
        buttons_frame = ttk.Frame(bottom_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=self.cancelar).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(buttons_frame, text="Salvar Pedido", 
                  command=self.salvar).pack(side=tk.RIGHT)
    
    def carregar_clientes(self):
        """Carrega lista de clientes no combobox"""
        clientes = self.cliente_manager.listar_todos_clientes()
        valores = [f"{c.id_cliente} - {c.nome}" for c in clientes]
        self.cliente_combo['values'] = valores
    
    def carregar_produtos(self):
        """Carrega lista de produtos no combobox"""
        produtos = self.produto_manager.listar_todos_produtos(apenas_ativos=True)
        valores = [f"{p.id_produto} - {p.nome} (R$ {p.preco:.2f}) - Estoque: {p.estoque}" for p in produtos]
        self.produto_combo['values'] = valores
    
    def carregar_dados_pedido(self):
        """Carrega dados do pedido para edição"""
        # Selecionar cliente
        cliente_texto = f"{self.pedido.cliente.id_cliente} - {self.pedido.cliente.nome}"
        self.cliente_var.set(cliente_texto)
        
        # Observações
        self.observacoes_text.insert(1.0, self.pedido.observacoes)
        
        # Carregar itens
        for item in self.pedido.itens:
            self.itens_tree.insert("", tk.END, values=(
                item.produto.nome,
                item.quantidade,
                f"R$ {item.preco_unitario:.2f}",
                f"R$ {item.subtotal:.2f}"
            ))
        
        self.atualizar_total()
    
    def adicionar_item(self):
        """Adiciona item ao pedido"""
        try:
            # Validar seleções
            if not self.produto_var.get():
                messagebox.showwarning("Aviso", "Selecione um produto")
                return
            
            quantidade_str = self.quantidade_var.get().strip()
            if not quantidade_str:
                messagebox.showwarning("Aviso", "Informe a quantidade")
                return
            
            try:
                quantidade = int(quantidade_str)
                if quantidade <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo")
                return
            
            # Obter ID do produto
            produto_texto = self.produto_var.get()
            id_produto = int(produto_texto.split(" - ")[0])
            
            # Buscar produto
            produto = self.produto_manager.buscar_produto_por_id(id_produto)
            if not produto:
                messagebox.showerror("Erro", "Produto não encontrado")
                return
            
            # Verificar estoque
            quantidade_atual = 0
            for child in self.itens_tree.get_children():
                item_values = self.itens_tree.item(child)['values']
                if item_values[0] == produto.nome:
                    quantidade_atual = int(item_values[1])
                    break
            
            quantidade_total = quantidade_atual + quantidade
            if produto.estoque < quantidade_total:
                messagebox.showerror("Erro", f"Estoque insuficiente. Disponível: {produto.estoque}")
                return
            
            # Verificar se produto já existe na lista
            item_existente = None
            for child in self.itens_tree.get_children():
                item_values = self.itens_tree.item(child)['values']
                if item_values[0] == produto.nome:
                    item_existente = child
                    break
            
            if item_existente:
                # Atualizar quantidade
                nova_quantidade = quantidade_atual + quantidade
                novo_subtotal = produto.preco * nova_quantidade
                
                self.itens_tree.item(item_existente, values=(
                    produto.nome,
                    nova_quantidade,
                    f"R$ {produto.preco:.2f}",
                    f"R$ {novo_subtotal:.2f}"
                ))
            else:
                # Adicionar novo item
                subtotal = produto.preco * quantidade
                self.itens_tree.insert("", tk.END, values=(
                    produto.nome,
                    quantidade,
                    f"R$ {produto.preco:.2f}",
                    f"R$ {subtotal:.2f}"
                ))
            
            # Limpar campos
            self.produto_var.set("")
            self.quantidade_var.set("1")
            
            self.atualizar_total()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar item: {str(e)}")
    
    def remover_item(self):
        """Remove item selecionado"""
        selection = self.itens_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para remover")
            return
        
        self.itens_tree.delete(selection[0])
        self.atualizar_total()
    
    def atualizar_total(self):
        """Atualiza total do pedido"""
        total = 0
        for child in self.itens_tree.get_children():
            item_values = self.itens_tree.item(child)['values']
            subtotal_str = item_values[3].replace("R$ ", "").replace(",", ".")
            total += float(subtotal_str)
        
        self.total_label.config(text=f"R$ {total:.2f}")
    
    def salvar(self):
        """Salva pedido"""
        try:
            # Validar cliente
            if not self.cliente_var.get():
                messagebox.showerror("Erro", "Selecione um cliente")
                return
            
            # Validar itens
            if not self.itens_tree.get_children():
                messagebox.showerror("Erro", "Adicione pelo menos um item ao pedido")
                return
            
            # Obter ID do cliente
            cliente_texto = self.cliente_var.get()
            id_cliente = int(cliente_texto.split(" - ")[0])
            
            # Obter observações
            observacoes = self.observacoes_text.get(1.0, tk.END).strip()
            
            if self.pedido is None:
                # Novo pedido
                sucesso, mensagem, pedido_criado = self.pedido_manager.criar_pedido(id_cliente, observacoes)
                if not sucesso:
                    messagebox.showerror("Erro", mensagem)
                    return
                
                pedido_id = pedido_criado.id_pedido
            else:
                # Editar pedido existente
                pedido_id = self.pedido.id_pedido
                
                # Atualizar observações
                self.pedido.observacoes = observacoes
                self.pedido_manager.db.salvar_pedido(self.pedido)
                
                # Remover todos os itens atuais
                for item in self.pedido.itens[:]:
                    self.pedido_manager.remover_item_pedido(pedido_id, item.produto.id_produto)
            
            # Adicionar itens
            for child in self.itens_tree.get_children():
                item_values = self.itens_tree.item(child)['values']
                nome_produto = item_values[0]
                quantidade = int(item_values[1])
                
                # Encontrar produto por nome
                produtos = self.produto_manager.listar_todos_produtos(apenas_ativos=True)
                produto = next((p for p in produtos if p.nome == nome_produto), None)
                
                if produto:
                    sucesso, mensagem = self.pedido_manager.adicionar_item_pedido(
                        pedido_id, produto.id_produto, quantidade)
                    if not sucesso:
                        messagebox.showerror("Erro", f"Erro ao adicionar {nome_produto}: {mensagem}")
                        return
            
            messagebox.showinfo("Sucesso", "Pedido salvo com sucesso!")
            self.resultado = True
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def cancelar(self):
        """Cancela operação"""
        self.window.destroy()
