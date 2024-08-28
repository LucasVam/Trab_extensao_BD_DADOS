import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname="tipo_pg",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabela():
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                telefone VARCHAR(15) NOT NULL,
                valor_pago NUMERIC(10, 2) NOT NULL,
                pagamento VARCHAR(10) NOT NULL
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()

def salvar_cliente():
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    valor_pago = entry_valor_pago.get().replace(',', '.')
    pagamento = var_pagamento.get()

    try:
        valor_pago = float(valor_pago)
    except ValueError:
        messagebox.showwarning("Atenção", "Valor pago inválido. Use o formato correto (ex: 1100.00).")
        return

    if nome and telefone and valor_pago is not None and pagamento:
        conn = conectar_banco()
        if conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO clientes (nome, telefone, valor_pago, pagamento)
                VALUES (%s, %s, %s, %s)
            ''', (nome, telefone, valor_pago, pagamento))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            limpar_campos()
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_valor_pago.delete(0, tk.END)
    var_pagamento.set("")

def consultar_clientes():
    nome = entry_nome_consulta.get()
    telefone = entry_telefone_consulta.get()
    conn = conectar_banco()
    if conn:
        cur = conn.cursor()
        query = 'SELECT * FROM clientes WHERE TRUE'
        params = []

        if nome:
            query += ' AND nome ILIKE %s'
            params.append(f'%{nome}%')
        if telefone:
            query += ' AND telefone ILIKE %s'
            params.append(f'%{telefone}%')

        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Limpar a árvore de resultados
        for item in tree.get_children():
            tree.delete(item)

        # Inserir os resultados na árvore
        for row in rows:
            tree.insert('', tk.END, values=row)
    else:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")

def criar_botao_personalizado(container, texto, comando):
    """ Cria um botão personalizado com cor azul e bordas arredondadas """
    botao_canvas = tk.Canvas(container, width=200, height=40, bg='blue', highlightthickness=0, borderwidth=0)
    botao_canvas.create_oval(0, 0, 200, 40, fill='blue', outline='blue')
    botao_canvas.create_text(100, 20, text=texto, fill='white', font=('Arial', 12, 'bold'))
    botao_canvas.bind("<Button-1>", lambda e: comando())
    botao_canvas.grid(row=4, column=1, pady=10, padx=10, sticky='se')

# Criação da interface gráfica
root = tk.Tk()
root.title("Cadastro e Consulta de Clientes")

# Configuração da tela cheia
root.attributes('-fullscreen', True)
root.bind("<F11>", lambda event: root.attributes('-fullscreen', not root.attributes('-fullscreen')))  # Alternar fullscreen com F11
root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))  # Sair do fullscreen com Escape

# Configuração das abas
tab_control = ttk.Notebook(root)

# Aba de Cadastro
tab_cadastro = ttk.Frame(tab_control)
tab_control.add(tab_cadastro, text='Cadastro')

# Configuração de estilo
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))
style.configure('Treeview', font=('Arial', 10))

# Adicionando widgets à aba de cadastro
tk.Label(tab_cadastro, text="Nome:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
entry_nome = tk.Entry(tab_cadastro, width=40, font=('Arial', 12))
entry_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(tab_cadastro, text="Telefone:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
entry_telefone = tk.Entry(tab_cadastro, width=40, font=('Arial', 12))
entry_telefone.grid(row=1, column=1, padx=10, pady=10)

tk.Label(tab_cadastro, text="Valor Pago:").grid(row=2, column=0, padx=10, pady=10, sticky='w')
entry_valor_pago = tk.Entry(tab_cadastro, width=40, font=('Arial', 12))
entry_valor_pago.grid(row=2, column=1, padx=10, pady=10)

tk.Label(tab_cadastro, text="Pagamento:").grid(row=3, column=0, padx=10, pady=10, sticky='w')
var_pagamento = tk.StringVar()
tk.Radiobutton(tab_cadastro, text="À Vista", variable=var_pagamento, value="À Vista").grid(row=3, column=1, padx=10, pady=10, sticky='w')
tk.Radiobutton(tab_cadastro, text="A Prazo", variable=var_pagamento, value="A Prazo").grid(row=3, column=1, padx=10, pady=10, sticky='e')

criar_botao_personalizado(tab_cadastro, "Salvar", salvar_cliente)

# Aba de Consulta
tab_consulta = ttk.Frame(tab_control)
tab_control.add(tab_consulta, text='Consulta')

tk.Label(tab_consulta, text="Nome:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
entry_nome_consulta = tk.Entry(tab_consulta, width=40, font=('Arial', 12))
entry_nome_consulta.grid(row=0, column=1, padx=10, pady=10)

tk.Label(tab_consulta, text="Telefone:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
entry_telefone_consulta = tk.Entry(tab_consulta, width=40, font=('Arial', 12))
entry_telefone_consulta.grid(row=1, column=1, padx=10, pady=10)

criar_botao_personalizado(tab_consulta, "Consultar", consultar_clientes)

# Árvore para exibir resultados
columns = ("id", "nome", "telefone", "valor_pago", "pagamento")
tree = ttk.Treeview(tab_consulta, columns=columns, show='headings')
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("telefone", text="Telefone")
tree.heading("valor_pago", text="Valor Pago")
tree.heading("pagamento", text="Pagamento")
tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Ajusta o peso das colunas para preencher a área disponível
tab_consulta.grid_rowconfigure(2, weight=1)
tab_consulta.grid_columnconfigure(0, weight=1)
tab_consulta.grid_columnconfigure(1, weight=1)

tab_control.pack(expand=1, fill='both')

criar_tabela()

root.mainloop()
