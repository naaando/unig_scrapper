import requests
from bs4 import BeautifulSoup

class UnigScrapper:
	def login(USERNAME, PASSWORD, REQUEST):
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

		if REQUEST == 'nota' and NotaServlet.status_code == 200:
			return NotaServlet.text

	def parser(Data,argument):
		soup = BeautifulSoup(Data, 'html.parser')
		tag = soup.get_text()

		#Procurando os valores nas tabelas
		notas = []

		rows = soup.find_all('tr')
		for i in rows:
			rowsp = i.find_all('td')
			for i in rowsp:
				notas.append(i.text.strip())

		#Procurando o nome no arquivo
		rows = soup.find_all('font', 'texto')
		nome = rows[0].text

		#0:Titulo , 1: Lista de notas, 2: Nome do aluno
		switcher = {
		0: soup.title.text,
		1: notas,
		2: nome,
		}

		return switcher.get(argument)

	def data_arrange(ParsedData):
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
				self.pf = []
				self.pa = []
				self.pr = []
				self.sc = []
				self.falta = []
				self.situacao = []

			def duplicated(self, Cod):
				for i in self.cod:
					if i == Cod:
						return True
		AnoLet = []
		x = -1
		for i in range(len(ParsedData)):
			if (ParsedData[i].strip().find("Letivo")) > 0:
				x=x+1
				ALFix = ParsedData[i].splitlines()
				for i in range(len(ALFix)):
					ALFix[i] = ALFix[i].strip()

				AnoLet.append(AnoLetivo())
				AnoLet[x].AnoLetivo = " ".join(ALFix)
			if ParsedData[i].isnumeric() and len(ParsedData[i]) == 4 and not AnoLet[x].duplicated(ParsedData[i]):
				AnoLet[x].matnum = AnoLet[x].matnum+1
				AnoLet[x].cod.append(ParsedData[i])
				AnoLet[x].mat.append(ParsedData[i+1])
				AnoLet[x].n1.append(ParsedData[i+2])
				AnoLet[x].r1.append(ParsedData[i+3])
				AnoLet[x].n2.append(ParsedData[i+4])
				AnoLet[x].r2.append(ParsedData[i+5])
				AnoLet[x].pf.append(ParsedData[i+6])
				AnoLet[x].pa.append(ParsedData[i+7])
				AnoLet[x].pr.append(ParsedData[i+8])
				AnoLet[x].sc.append(ParsedData[i+9])
				AnoLet[x].falta.append(ParsedData[i+10])
				AnoLet[x].situacao.append(ParsedData[i+11])

		return AnoLet
