import sys

if __name__ == '__main__':
	import urllib.request
	# url = sys.argv[0]
	url = "https://github.com/jkutkut"
	datos = urllib.request.urlopen(url).read().decode()

	from bs4 import BeautifulSoup

	soup =  BeautifulSoup(datos)
	tags = soup("img")
	for tag in tags:
		print(tag.get("src"))
	# print(datos)

