import requests
from lxml import html

USERNAME = "140119121"
PASSWORD = "55006"

LOGIN_URL = "http://lancamento.unig.br/unigonline/cadastrados.jsp"
NOTA_URL = "http://lancamento.unig.br/unigonline/NotaServlet.do"
URL = "http://lancamento.unig.br/unigonline/OnLineServlet.do"

def savefile(obj):
		print 'Save(true)'
		f = open('login_unig.html', 'w')
		f.write(obj)
		f.close

def main():
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
	#print(result.status_code, result.text, result.json)
	#print(OnLineServlet.text)
	print(NotaServlet.text)

	save = 0;
	if save == 1:
		savefile(NotaServlet.text)

if __name__ == '__main__':
	main()
