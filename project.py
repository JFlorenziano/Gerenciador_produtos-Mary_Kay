import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.ttk as ttk
import json
import os
from datetime import datetime

class Produto:
    def __init__(self, nome, preco, quantidade, custo, vendidos=0):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.custo = custo
        self.vendidos = vendidos

    def vender_produto(self, quantidade_vendida):
        if self.quantidade >= quantidade_vendida:
            self.quantidade -= quantidade_vendida
            self.vendidos += quantidade_vendida
            return True
        else:
            return False

    def alterar_dados(self, nome, preco, quantidade, custo):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.custo = custo

    def valor_bruto(self):
        return self.vendidos * self.preco

    def valor_liquido(self):
        return self.valor_bruto() - (self.vendidos * self.custo)

    def dizimo(self):
        return self.valor_liquido() * 0.10

    def to_dict(self):
        return {
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "custo": self.custo,
            "vendidos": self.vendidos
        }

class GerenciadorProdutos(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciamento de Produtos")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")

        self.produtos = self.carregar_produtos()

        # Menu lateral
        self.side_menu = tk.Frame(self, width=200, bg="#3b5998")
        self.side_menu.pack(side="left", fill="y")

        # Botões do menu
        self.btn_cadastrar = tk.Button(self.side_menu, text="Cadastrar Produto", command=self.form_cadastrar_produto, bg="#8b9dc3", fg="white", font=("Arial", 12), pady=10)
        self.btn_cadastrar.pack(fill="x")

        self.btn_listar = tk.Button(self.side_menu, text="Listar Produtos", command=self.listar_produtos, bg="#8b9dc3", fg="white", font=("Arial", 12), pady=10)
        self.btn_listar.pack(fill="x")

        self.btn_relatorio = tk.Button(self.side_menu, text="Relatório Financeiro", command=self.gerar_relatorio_financeiro, bg="#8b9dc3", fg="white", font=("Arial", 12), pady=10)
        self.btn_relatorio.pack(fill="x")

        # Área de conteúdo
        self.content_area = tk.Frame(self, bg="#f0f0f0")
        self.content_area.pack(side="right", fill="both", expand=True)

    def salvar_produtos(self):
        produtos_dict = {nome: produto.to_dict() for nome, produto in self.produtos.items()}
        with open("produtos.json", "w") as f:
            json.dump(produtos_dict, f)

    def carregar_produtos(self):
        if os.path.exists("produtos.json"):
            with open("produtos.json", "r") as f:
                produtos_dict = json.load(f)
                return {nome: Produto(**dados) for nome, dados in produtos_dict.items()}
        return {}

    def form_cadastrar_produto(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Cadastrar Produto", font=("Arial", 16)).pack(pady=10)

        # Nome
        tk.Label(self.content_area, text="Nome:").pack(anchor="w")
        entry_nome = tk.Entry(self.content_area)
        entry_nome.pack(fill="x")

        # Preço
        tk.Label(self.content_area, text="Preço:").pack(anchor="w")
        entry_preco = tk.Entry(self.content_area)
        entry_preco.pack(fill="x")

        # Quantidade
        tk.Label(self.content_area, text="Quantidade:").pack(anchor="w")
        entry_quantidade = tk.Entry(self.content_area)
        entry_quantidade.pack(fill="x")

        # Custo
        tk.Label(self.content_area, text="Custo:").pack(anchor="w")
        entry_custo = tk.Entry(self.content_area)
        entry_custo.pack(fill="x")

        # Botão salvar
        btn_salvar = tk.Button(self.content_area, text="Salvar Produto", command=lambda: self.salvar_novo_produto(
            entry_nome.get(), entry_preco.get(), entry_quantidade.get(), entry_custo.get()))
        btn_salvar.pack(pady=10)

    def salvar_novo_produto(self, nome, preco, quantidade, custo):
        try:
            preco = float(preco)
            quantidade = int(quantidade)
            custo = float(custo)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")
            return

        if nome and preco and quantidade is not None and custo:
            self.produtos[nome] = Produto(nome, preco, quantidade, custo)
            self.salvar_produtos()
            messagebox.showinfo("Sucesso", f"Produto {nome} cadastrado com sucesso!")
            self.listar_produtos()

    def listar_produtos(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Lista de Produtos", font=("Arial", 16)).pack(pady=10)

        # Criar o Treeview (tabela)
        colunas = ("Nome", "Preço", "Quantidade", "Custo", "Vendidos")
        tree = ttk.Treeview(self.content_area, columns=colunas, show='headings')
        tree.pack(fill="both", expand=True)

        # Definir as colunas
        tree.heading("Nome", text="Nome")
        tree.heading("Preço", text="Preço (R$)")
        tree.heading("Quantidade", text="Quantidade")
        tree.heading("Custo", text="Custo (R$)")
        tree.heading("Vendidos", text="Vendidos")

        # Definir o tamanho das colunas
        tree.column("Nome", width=150)
        tree.column("Preço", width=100)
        tree.column("Quantidade", width=100)
        tree.column("Custo", width=100)
        tree.column("Vendidos", width=100)

        # Preencher a tabela com os produtos
        for nome, produto in self.produtos.items():
            tree.insert("", "end", values=(nome, f"{produto.preco:.2f}", produto.quantidade, f"{produto.custo:.2f}", produto.vendidos))

        # Adicionar botões abaixo do grid
        btn_editar = tk.Button(self.content_area, text="Editar Produto", command=lambda: self.form_editar_produto(tree.item(tree.selection())['values'][0]))
        btn_editar.pack(side="left", padx=5, pady=10)

        btn_vender = tk.Button(self.content_area, text="Vender Produto", command=lambda: self.form_vender_produto(tree.item(tree.selection())['values'][0]))
        btn_vender.pack(side="left", padx=5, pady=10)

        btn_excluir = tk.Button(self.content_area, text="Excluir Produto", command=lambda: self.excluir_produto(tree.item(tree.selection())['values'][0]))
        btn_excluir.pack(side="left", padx=5, pady=10)

    def form_editar_produto(self, nome):
        produto = self.produtos[nome]
        self.clear_content_area()
        tk.Label(self.content_area, text=f"Editar Produto: {nome}", font=("Arial", 16)).pack(pady=10)

        # Nome
        tk.Label(self.content_area, text="Nome:").pack(anchor="w")
        entry_nome = tk.Entry(self.content_area)
        entry_nome.insert(0, produto.nome)
        entry_nome.pack(fill="x")

        # Preço
        tk.Label(self.content_area, text="Preço:").pack(anchor="w")
        entry_preco = tk.Entry(self.content_area)
        entry_preco.insert(0, produto.preco)
        entry_preco.pack(fill="x")

        # Quantidade
        tk.Label(self.content_area, text="Quantidade:").pack(anchor="w")
        entry_quantidade = tk.Entry(self.content_area)
        entry_quantidade.insert(0, produto.quantidade)
        entry_quantidade.pack(fill="x")

        # Custo
        tk.Label(self.content_area, text="Custo:").pack(anchor="w")
        entry_custo = tk.Entry(self.content_area)
        entry_custo.insert(0, produto.custo)
        entry_custo.pack(fill="x")

        # Botão salvar
        btn_salvar = tk.Button(self.content_area, text="Salvar Alterações", command=lambda: self.salvar_edicao_produto(
            nome, entry_nome.get(), entry_preco.get(), entry_quantidade.get(), entry_custo.get()))
        btn_salvar.pack(pady=10)

    def salvar_edicao_produto(self, nome_antigo, novo_nome, novo_preco, nova_quantidade, novo_custo):
        try:
            novo_preco = float(novo_preco)
            nova_quantidade = int(nova_quantidade)
            novo_custo = float(novo_custo)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")
            return

        produto = self.produtos.pop(nome_antigo)
        produto.alterar_dados(novo_nome, novo_preco, nova_quantidade, novo_custo)
        self.produtos[novo_nome] = produto
        self.salvar_produtos()
        messagebox.showinfo("Sucesso", f"Produto {nome_antigo} editado com sucesso!")
        self.listar_produtos()

    def form_vender_produto(self, nome):
        produto = self.produtos[nome]
        quantidade_vender = simpledialog.askinteger("Vender Produto", f"Quantidade a vender de {nome}:", minvalue=1)

        if quantidade_vender is not None and produto.vender_produto(quantidade_vender):
            self.salvar_produtos()
            messagebox.showinfo("Sucesso", f"Vendidos {quantidade_vender} unidades de {nome}!")
            self.listar_produtos()
        else:
            messagebox.showerror("Erro", "Quantidade insuficiente em estoque!")

    def excluir_produto(self, nome):
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o produto {nome}?"):
            self.produtos.pop(nome)
            self.salvar_produtos()
            messagebox.showinfo("Sucesso", f"Produto {nome} excluído com sucesso!")
            self.listar_produtos()

    def gerar_relatorio_financeiro(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Relatório Financeiro", font=("Arial", 16)).pack(pady=10)

        valor_bruto_total = 0
        valor_liquido_total = 0
        dizimo_total = 0

        for produto in self.produtos.values():
            valor_bruto_total += produto.valor_bruto()
            valor_liquido_total += produto.valor_liquido()
            dizimo_total += produto.dizimo()

        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tk.Label(self.content_area, text=f"Relatório gerado em: {data_hora}", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.content_area, text=f"Valor Bruto Total: R$ {valor_bruto_total:.2f}").pack(anchor="w", padx=10)
        tk.Label(self.content_area, text=f"Valor Líquido Total: R$ {valor_liquido_total:.2f}").pack(anchor="w", padx=10)
        tk.Label(self.content_area, text=f"Dízimo Total (10% do valor líquido): R$ {dizimo_total:.2f}").pack(anchor="w",
                                                                                                             padx=10)

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = GerenciadorProdutos()
    app.mainloop()
