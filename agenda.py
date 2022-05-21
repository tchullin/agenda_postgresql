from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import banco

###################################################################
# tkinter object
app = Tk()
app.title("Minha Agenda")
app.geometry("800x500")
app.configure(background="#dde")
###################################################################


# Carregar a Treeview com dados da tabela
def popular():
    # Create Striped Treeview Rows
    trv.tag_configure('oddrow', background="white")
    trv.tag_configure('evenrow', background="lightblue")
    trv.delete(*trv.get_children())
    vquery = "SELECT * FROM contatos order by Id"
    linhas = banco.dql(vquery)
    count = 0
    for i in linhas:
        if count % 2 == 0:
            trv.insert("", "end", values=i, tags=('evenrow',))
        else:
            trv.insert("", "end", values=i, tags=('oddrow',))
        # increment counter
        count += 1


def inserir():
    if vnome.get() == "" or vfone.get() == "" or vemail.get() == "" or vobs.get() == "":
        messagebox.showinfo(title="Erro", message="Digite todos os campos")
        return
    try:
        vquery = "INSERT INTO contatos (Nome,Telefone,Email,Obs) " \
                 "VALUES ('" + vnome.get() + "','" + vfone.get() + "','" + vemail.get() + "','" + vobs.get() + "')"
        banco.dml(vquery)
    except Exception as e:
        print(e)
        messagebox.showinfo(title="Erro", message="Erro ao Inserir o Registro")
    popular()
    vnome.delete(0, END)
    vfone.delete(0, END)
    vemail.delete(0, END)
    vobs.delete(0, END)
    vnome.focus()


def alterar():
    print(vid, vnome.get(), vfone.get(), vemail.get(), vobs.get())
    if vnome.get() == "" or vfone.get() == "" or vemail.get() == "" or vobs.get() == "":
        messagebox.showinfo(title="Erro", message="Digite todos os campos")
        return
    try:
        vquery = "UPDATE contatos SET Nome='" + vnome.get() + "', Telefone='" + vfone.get() + "'," \
                        "Email='" + vemail.get() + "',Obs='" + vobs.get() + "' " \
                        "WHERE Id='" + vid + "'"
        banco.dml(vquery)
    except Exception as e:
        print(e)
        messagebox.showinfo(title="Erro", message="Erro ao Alterar o Registro")
    popular()
    vnome.delete(0, END)
    vfone.delete(0, END)
    vemail.delete(0, END)
    vobs.delete(0, END)
    vnome.focus()


def apagar():
    print(vid, vnome.get(), vfone.get(), vemail.get(), vobs.get())
    try:
        vquery = "DELETE FROM contatos WHERE Id='" + vid + "'"
        banco.dml(vquery)
    except Exception as e:
        print(e)
        messagebox.showinfo(title="Erro", message="Erro ao Excluir o Registro")
    popular()
    vnome.delete(0, END)
    vfone.delete(0, END)
    vemail.delete(0, END)
    vobs.delete(0, END)
    vnome.focus()


def obter(event):
    limpar()
    global vid
    try:
        itemselecionado = trv.selection()[0]
        valores = trv.item(itemselecionado, "values")
        # print(valores)
        print("ID      : " + valores[0])
        print("Nome    : " + valores[1])
        print("Telefone: " + valores[2])
        print("E-mail  : " + valores[3])
        print("Obs.    : " + valores[4])
        # carrega valoress nos campos de entrada
        # vid.insert('0', valores[0])
        vid = valores[0]
        vnome.insert('0', valores[1])
        vfone.insert('0', valores[2])
        vemail.insert('0', valores[3])
        vobs.insert('0', valores[4])
    except Exception as e:
        print(e)
        messagebox.showinfo(title="Erro", message="Selecione um elemento a ser mostrado")


def pesquisar():
    trv.delete(*trv.get_children())
    vquery = "SELECT * FROM contatos WHERE Nome LIKE '%" + vnomepesquisar.get() + "%' order by Id"
    linhas = banco.dql(vquery)
    count = 0
    for i in linhas:
        if count % 2 == 0:
            trv.insert("", "end", values=i, tags=('evenrow',))
        else:
            trv.insert("", "end", values=i, tags=('oddrow',))
        # increment counter
        count += 1
    vnomepesquisar.delete(0, END)


def limpar():
    vnome.delete(0, END)
    vfone.delete(0, END)
    vemail.delete(0, END)
    vobs.delete(0, END)
    vnome.focus()


####################################################################
quadroGrid = LabelFrame(app, text="Contatos")
quadroGrid.pack(fill="both", expand=1, padx=10, pady=10)
# Create a Treeview Scrollbar
tree_scroll = Scrollbar(quadroGrid)
tree_scroll.pack(side=RIGHT, fill=Y)
# Create the Treeview
trv = ttk.Treeview(quadroGrid, columns=('id', 'nome', 'fone', 'email', 'obs'), show='headings',
                   yscrollcommand=tree_scroll.set)
# Configure the ScrollBar
tree_scroll.config(command=trv.yview)

# Format Treeview Columns
trv.column('id', width=50, minwidth=0)
trv.column('nome', width=150, minwidth=0)
trv.column('fone', width=100, minwidth=0)
trv.column('email', width=150, minwidth=0)
trv.column('obs', width=250, minwidth=0)
trv.heading('id', text='ID')
trv.heading('nome', text='Nome')
trv.heading('fone', text='Telefone')
trv.heading('email', text='E-mail')
trv.heading('obs', text='Obs.')
trv.pack(fill="both", expand=1)
# Bind the Treeview
trv.bind("<ButtonRelease-1>", obter)
popular()
####################################################################
quadroPesquisar = LabelFrame(app, text="Pesquisar Contatos")
quadroPesquisar.pack(fill="both", expand=1, padx=10, pady=10)
lnome = Label(quadroPesquisar, text="Nome")
lnome.pack(side="left")
vnomepesquisar = Entry(quadroPesquisar)
vnomepesquisar.pack(side="left", padx=10)
btn_pesquisar = Button(quadroPesquisar, text="Pesquisar", command=pesquisar)
btn_pesquisar.pack(side="left", padx=10)
btn_todos = Button(quadroPesquisar, text="Mostrar Todos", command=popular)
btn_todos.pack(side="left", padx=10)
btn_limpar = Button(quadroPesquisar, text="Limpar Campos", command=limpar)
btn_limpar.pack(side="left", padx=10)
####################################################################
quadroInserir = LabelFrame(app, text="Inserir Novos Contatos")
quadroInserir.pack(fill="both", expand=1, padx=10, pady=10)
lbnome = Label(quadroInserir, text="Nome")
lbnome.grid(row=0, column=0, pady=10)
vnome = Entry(quadroInserir)
vnome.grid(row=0, column=1, padx=10, pady=10)
lbfone = Label(quadroInserir, text="Telefone")
lbfone.grid(row=0, column=2)
vfone = Entry(quadroInserir)
vfone.grid(row=0, column=3, padx=10)
lbemail = Label(quadroInserir, text="E-mail")
lbemail.grid(row=0, column=4, pady=10)
vemail = Entry(quadroInserir)
vemail.grid(row=0, column=5, padx=10, pady=10)
lbobs = Label(quadroInserir, text="Obs.")
lbobs.grid(row=1, column=0)
vobs = Entry(quadroInserir)
vobs.grid(row=1, column=1, padx=10, ipadx=200, columnspan=5)
btn_inserir = Button(quadroInserir, text="Inserir", command=inserir)
btn_inserir.grid(row=0, column=7, padx=10, pady=10)
btn_alterar = Button(quadroInserir, text="Alterar", command=alterar)
btn_alterar.grid(row=0, column=8, padx=5, pady=5)
btn_excluir = Button(quadroInserir, text="Excluir", command=apagar)
btn_excluir.grid(row=0, column=9, padx=5, pady=5)
####################################################################

app.mainloop()
