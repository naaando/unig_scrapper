import requests
from bs4 import BeautifulSoup

def unig_scraper(USERNAME, PASSWORD, INFO):
	#Unig's URLs
	LOGIN_URL = "http://lancamento.unig.br/unigonline/cadastrados.jsp"
	NOTA_URL = "http://lancamento.unig.br/unigonline/NotaServlet.do"
	URL = "http://lancamento.unig.br/unigonline/OnLineServlet.do"

	session_requests = requests.session()

	# Create payload
	payload = {
		"matricula": USERNAME,
		"senha": PASSWORD,
		"submit": "++Entrar++"
	}

	# Perform login
	result = session_requests.post(URL, data = payload)
	OnLineServlet = session_requests.get(URL)
	NotaServlet = session_requests.get(NOTA_URL)

	# Scrape url
	#print( result.status_code, result.text, result.json, OnLineServlet.text, NotaServlet.text)

	if INFO == 'nota' and NotaServlet.status_code == 200:
		return NotaServlet.text

def parser(Data,argument):
	soup = BeautifulSoup(Data, 'html.parser')
	tag = soup.get_text()

	#Procurando os valores nas tabelas
	values = []

	rows = soup.find_all('tr')
	for i in rows:
		rowsp = i.find_all('td')
		for i in rowsp:
			values.append(i.text)

	#Procurando o nome no arquivo
	rows = soup.find_all('font', 'texto')
	nome = rows[0].text

	switcher = {
	0: soup.title.text,
	1: values,
	2: nome
	}

	return switcher.get(argument)

def PrintNota(ParsedD):
	class AnoLetivo:
		def __init__(self):
			self.AnoLetivo = []
			self.cod = []
			self.mat = []
			self.matnum = 0
			self.n1 = []
			self.r1 = []
			self.n2 = []
			self.r2 = []
			self.r2 = []
			self.pf = []
			self.pa = []
			self.pr = []
			self.sc = []
			self.falta = []
			self.situacao = []
		def showNota(self):
			ALFix = self.AnoLetivo.splitlines()
			for i in range(len(ALFix)):
				ALFix[i] = ALFix[i].strip()

			self.AnoLetivo = " ".join(ALFix)
			#Espaço entre as strings
			s = 3
			print(self.AnoLetivo,"Quantidade de materias: ".rjust(56),self.matnum)
			for i in range(self.matnum):
				print(self.cod[i],
				self.mat[i].ljust(35),
				self.n1[i].strip().ljust(s),
				self.r1[i].strip().ljust(s),
				self.n2[i].strip().ljust(s),
				self.r2[i].strip().ljust(s),
				self.pf[i].strip().ljust(s),
				self.pa[i].strip().ljust(s),
				self.pr[i].strip().ljust(s),
				self.sc[i].strip().ljust(s),
				self.falta[i].strip().ljust(s),
				self.situacao[i].strip().ljust(s),
				sep="|")

			print("")

		def duplicated(self, Cod):
			for i in self.cod:
				if i == Cod:
					return True

	AnoLet = []
	x = -1

	for i in range(len(ParsedD)):
		if (ParsedD[i].strip().find("Letivo")) > 0:
			x=x+1
			AnoLet.append(AnoLetivo())
			AnoLet[x].AnoLetivo = ParsedD[i]
		if ParsedD[i].isnumeric() and len(ParsedD[i]) == 4 and not AnoLet[x].duplicated(ParsedD[i]):
			AnoLet[x].matnum = AnoLet[x].matnum+1
			AnoLet[x].cod.append(ParsedD[i])
			AnoLet[x].mat.append(ParsedD[i+1])
			AnoLet[x].n1.append(ParsedD[i+2])
			AnoLet[x].r1.append(ParsedD[i+3])
			AnoLet[x].n2.append(ParsedD[i+4])
			AnoLet[x].r2.append(ParsedD[i+5])
			AnoLet[x].pf.append(ParsedD[i+6])
			AnoLet[x].pa.append(ParsedD[i+7])
			AnoLet[x].pr.append(ParsedD[i+8])
			AnoLet[x].sc.append(ParsedD[i+9])
			AnoLet[x].falta.append(ParsedD[i+10])
			AnoLet[x].situacao.append(ParsedD[i+11])

	for i in AnoLet:
		i.showNota()

def main():
	#Recolhendo credenciais de usuario
	#Conta
	print("Ola, digite sua matricula:")
	matricula = input()

	#Senha
	print("Digite sua senha:")
	senha = input()

	#Baixando html
	Nota = unig_scraper(matricula, senha, "nota")
	Parsed = parser(Nota,1)
	nome = parser(Nota,2)

	#Exibindo credenciais
	print("="*8,"Matricula:",matricula," | ", nome.title(), "="*8)
	print("Codigo |  Materia  | N1 | R1 | N2 | R2 | PF | PA | SC | % de falta | Situação")

	PrintNota(Parsed)

if __name__ == '__main__':
	main()
