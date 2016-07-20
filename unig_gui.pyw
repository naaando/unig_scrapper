# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/
#Disclaimer: Esse aplicativo não tem nenhuma ligação com a Unig e seus associados.

import tkinter as tk
from tkinter import ttk
import unig_scrapper

LARGE_FONT= ("Arimo", 24)

Unig = unig_scrapper.UnigScrapper

class UnigClient(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		#self.theme=ttk.Style()
		#self.theme.theme_use('clam')

		#Icon e titulo, resolver depois
		#tk.Tk.iconbitmap(self,default="unig.ico")
		tk.Tk.wm_title(self, "Notas - Unig")

		self.container = tk.Frame(self)

		self.container.pack(side="top", fill="both", expand=True)

		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		# for F in (LoginPage,MainPage):
		# 	print(F)
		# 	frame = F(container, self)
		# 	self.frames[F] = frame
		# 	frame.grid(row=0, column=0, sticky="nsew")

		print(LoginPage)
		frame = LoginPage(self.container,self)
		self.frames[LoginPage] = frame
		frame.grid(row=0,column=0,sticky='nsew')

		self.show_frame(LoginPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()

	def load_page(self,cont):

		print(cont)
		frame = cont(self.container,self)
		self.frames[cont] = frame
		frame.grid(row=0,column=0,sticky='nsew')

	def Exit(self):
		pass
		#self.destroy()

class LoginPage(tk.Frame):
	def __init__(self, parent, controller, data=0):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text="Unig Login", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		self.Html=None

		self.username=ttk.Entry(self)
		self.username.pack(pady=2)

		self.password=ttk.Entry(self, show="*")
		self.password.pack(pady=2)

		self.login_form=ttk.Frame(self)
		self.login_form.pack()

		self.controller = controller
		login = ttk.Button(self.login_form, text="Entrar", command=self.login)
		login.pack(pady=10,padx=10)

		exit = ttk.Button(self.login_form, text="Fechar", command=self.controller.Exit())
		exit.pack(pady=10,padx=10)

	def login(self):
		print("Matricula : ",self.username.get())
		print("Senha : ",self.password.get())
		print("Efetuando login")
		self.Html = Unig.login(self.username.get(), self.password.get(), "nota")
		MainPage.parser(MainPage,self.Html)
		self.controller.load_page(MainPage)
		self.controller.show_frame(MainPage)

	def login_response(self):
		print("Requisitando html")
		return Html

class MainPage(tk.Frame):
	def __init__(self, parent, controller,data=0):
		tk.Frame.__init__(self,parent)

		label = ttk.Label(self, text="Consulta de notas", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		na = self.nota_arrange[1]

		header = [self.nome, na.AnoLetivo,"Quantidade de materias: ",na.matnum]
		name = ttk.Label(self, text=header)
		name.pack()

		Notas_Columns = ['Codigo','Materia','Nota1','Nota2','Pr','Sc']
		Notas_width = [80, 300, 60, 60, 60, 60]
		self.Notas = ttk.Treeview(self, columns=Notas_Columns,show="headings")

		for col,wid in zip(Notas_Columns,Notas_width):
			self.Notas.heading(col, text=col,command=lambda c=col: sortby(self.tree, c, 0))
			self.Notas.column(col, width=wid)


		for i in range(na.matnum):
			print(i)
			self.Notas.insert('','end',values=(na.cod[i], na.mat[i], na.n1[i], na.n2[i], na.pr[i], na.sc[i]))

		self.Notas.pack()

		LogoutButton = ttk.Button(self, text="Sair",command=lambda: controller.show_frame(LoginPage))
		LogoutButton.pack(pady=10,padx=10)

		#self.buildtree()

	def parser(self,html):
		print(html)
		print("Fazendo parsing do documento....")
		self.nome = Unig.parser(html,2)
		print(self.nome)

		nota = Unig.parser(html, 1)
		self.nota_arrange = Unig.data_arrange(nota)
		print(self.nota_arrange[0])

		if html != None:
			return True

	# 	#Notas.insert('','end',values=self.nota_arrange[0])
	# 	#for item in self.element_list:
    #     #     self.tree.insert('', 'end', values=item)
    #     #     # adjust column's width if necessary to fit each value
    #     #     for ix, val in enumerate(item):
    #     #     	col_w = tkFont.Font().measure(val)
    #     #         if self.tree.column(self.element_header[ix], width=None) < col_w:
    #     #             self.tree.column(self.element_header[ix], width=col_w)
	#
	# 	namse = ttk.Label(self, text="data")
	# 	namse.pack()


app = UnigClient()
app.mainloop()
