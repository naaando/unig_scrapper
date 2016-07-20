# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/
#Disclaimer: Esse aplicativo não tem nenhuma ligação com a Unig e seus associados.

import tkinter as tk
from tkinter import ttk
import os
import json
import unig_scrapper

LARGE_FONT= ("Liberation Sans", 24)
bgcolor = '#F0F0F0'
VERSAO= '0.2 beta'

Unig = unig_scrapper.UnigScrapper

class UnigClient(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		self.geometry('700x400')
		self.theme=ttk.Style()
		if os.name != 'nt':
			self.theme.theme_use('clam')
			self.theme.configure(self, relief='flat', background=bgcolor)
			self.theme.configure("TButton", relief='flat' ,padding=10)
			self.theme.configure("N.TButton", background='#6E0E00')
			self.theme.configure("P.TButton", background='#0C7E00')
			self.theme.map("P.TButton",
				foreground=[('pressed', '#white'), ('active', 'white')],
				background=[('pressed', '#0B6E00'), ('active', '#15D100')]
	    		)
			self.theme.map("N.TButton",
				foreground=[('pressed', '#white'), ('active', 'white')],
				background=[('pressed', '#981400'), ('active', '#D81C00')]
	    		)
		else:
			self.theme.configure("TButton", padding=10)
			self.theme.configure("N.TButton")
			self.theme.configure("P.TButton")

		#Icon e titulo, resolver depois
		#tk.Tk.iconbitmap(self,default="unig.ico")
		tk.Tk.wm_title(self, "Unig - Consulta de notas")

		self.container = tk.Frame(self)

		self.container.pack(fill="both", expand=True)

		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames = {}

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
		self.destroy()

class LoginPage(tk.Frame):
	def __init__(self, parent, controller, data=0):
		tk.Frame.__init__(self, parent, bg=bgcolor)

		#Variaveis
		self.Html=None
		self.controller = controller

		#Containers
		label_cont = ttk.Frame(self)
		label_cont.pack()
		mat_cont = ttk.Frame(self)
		mat_cont.pack(pady=10,padx=10,side='top')
		sen_cont = ttk.Frame(self)
		sen_cont.pack(pady=10,padx=10,side='top')
		self.login_form=ttk.Frame(self)
		self.login_form.pack(pady=10,padx=10,side='bottom')

		#label principal e versao
		versao = ttk.Label(label_cont, text='Versão '+VERSAO).pack()
		label = ttk.Label(label_cont, text="Unig Login", font=LARGE_FONT).pack(pady=50,padx=10,side='top')

		#Label e entry da matricula
		matricula = ttk.Label(mat_cont, text="Matricula : ")
		matricula.pack(side='left')
		self.username=ttk.Entry(mat_cont)
		self.username.pack(side='left')

		#Label e entry da senha
		senha = ttk.Label(sen_cont, text="Senha : ")
		senha.pack(side='left')
		self.password=ttk.Entry(sen_cont, show="*")
		self.password.pack(side='left')

		self.rm = tk.IntVar()
		remember = ttk.Checkbutton(self.login_form, text='Lembrar-Me(Em breve)', variable=self.rm)
		remember.state(["disabled"])
		remember.pack(side='top')

		#Botoes
		login = ttk.Button(self.login_form, text="Entrar", command=self.login, style="P.TButton")
		login.pack(side='left',pady=10,padx=10)

		exit = ttk.Button(self.login_form, text="Fechar", command=self.controller.Exit, style='N.TButton')
		exit.pack(side='left',pady=10,padx=10)

	def login(self):
		print("Matricula : ",self.username.get())
		print("Senha : ",self.password.get())
		print("Efetuando login")
		self.Html = Unig.login(self.username.get(), self.password.get(), "nota")
		MainPage.parser(MainPage,self.Html)
		if self.rm.get() == 1:
			print('Salvando credenciais')
			self.remember_me()
		self.controller.load_page(MainPage)
		self.controller.show_frame(MainPage)

	def login_response(self):
		print("Requisitando html")
		return Html

	def remember_me(self):
		with open('credentials', 'w') as outfile:
			data = {'username': self.username.get(), 'password': self.password.get()}
			print(data)
			json.dump(data, outfile)

class MainPage(tk.Frame):
	def __init__(self, parent, controller,data=0):
		tk.Frame.__init__(self,parent,bg=bgcolor)

		label = ttk.Label(self, text="Consulta de notas", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		na = self.nota_arrange[1]

		header = [self.nome,na.AnoLetivo,"Quantidade de materias:"+str(na.matnum)]
		name = ttk.Label(self, text=' | '.join(header))
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

		LogoutButton = ttk.Button(self, text="Sair", style='N.TButton',command=lambda: controller.show_frame(LoginPage))
		LogoutButton.pack(pady=10,padx=10)

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


app = UnigClient()
app.mainloop()
