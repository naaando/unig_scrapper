from src import unig_scrapper

Unig = unig_scrapper.UnigScrapper

def PrintNota(i):
	print(i.AnoLetivo,"Quantidade de materias: ".rjust(56),i.matnum)
	s=4
	for x in range(i.matnum):
		print(i.cod[x],i.mat[x].ljust(35),
			i.n1[x].strip().ljust(s),
			#i.r1[x].strip().ljust(s),
			i.n2[x].strip().ljust(s),
			#i.r2[x].strip().ljust(s),
			i.pf[x].strip().ljust(s),
			i.pa[x].strip().ljust(s),
			i.pr[x].strip().ljust(s),
			i.sc[x].strip().ljust(s),
			i.falta[x].strip().ljust(s),
			i.situacao[x].strip().ljust(s),
			sep="|")

	print("")

def main():
	#Recolhendo credenciais de usuario
	#Conta
	print("Ola, digite sua matricula:")
	matricula = input()

	#Senha
	print("Digite sua senha:")
	senha = input()

	#Baixando html
	Html = Unig.login(matricula, senha, "nota")
	Parsing = Unig.parser(Html,1)
	nome = Unig.parser(Html,2)
	nota = Unig.data_arrange(Parsing)

	#Exibindo credenciais
	i = 10
	print("="*i,"Matricula:",matricula," | ", nome.title(), "="*i)
	# print("Codigo |  Materia  | N1 | R1 | N2 | R2 | PF | PA | SC | % de falta | Situação")
	print("Codigo |  Materia  | N1 | N2 | PF | PA | SC | % de falta | Situação")
	print("="*8*i)

	for i in nota:
		PrintNota(i)

if __name__ == '__main__':
	main()
