_version = "2.0"
_plugindir = "/usr/lib/enigma2/python/Plugins/Extensions/GeradorPicons"
_title = "Gerador de Picons"
_developer = "gravatasufoca"
_outdir = '/etc/enigma2'
_cacheFile=_plugindir+"/cache.txt"

_urlModelo="https://dl.dropboxusercontent.com/u/12772101/geradorPicons/modelos.conf"
_urlVersao="https://dl.dropboxusercontent.com/u/12772101/geradorPicons/enigma2-plugin-extensions-gerador-picons.ipk"

screens=[]

def addScreen(screen):
	screens.append(screen)


def corrigiNome(nome):
	# return Utils.removeAcentos(nome.toLowerCase().trim()).replace(".png","").replaceAll("\\s+(?=\\d+)","");
	import re
	nome = nome.lower().replace(".png", "")
	return removerAcentos(re.sub('\s+(?=\d+)', '', nome))


def removerAcentos(input_str):
	from unicodedata import normalize
	return normalize('NFKD', input_str.decode("UTF-8")).encode('ASCII', 'ignore')

def addToCache(path):
	arquivo =open(_cacheFile,"w")
	arquivo.write(path+"\n")
	arquivo.close()

def getConfiguracoes():
	import urllib,ConfigParser

	testfile = urllib.URLopener()
	testfile.retrieve(_urlModelo, "/tmp/modelos.conf")

	config = ConfigParser.RawConfigParser()
	config.read('/tmp/modelos.conf')
	items=[]
	for item in config.items("modelos"):
		items.append((item[1],item[0]))

	return {"items":items,"versao":config.get("versao","versao")}

def getPiconsZipped(url,callback=[]):
	import requests, zipfile, StringIO
	r = requests.get(url,stream=True)

	total_length = r.headers.get('content-length')

	content=""
	recebido=0
	for chunck in r.iter_content(1024):
		recebido+=len(chunck)
		content+=chunck
		print len(content)
		callback(total_length,recebido)

	zipDocument = zipfile.ZipFile(StringIO.StringIO(content))
	return zipDocument