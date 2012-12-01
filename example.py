# encoding: utf8
import cetd
import urllib.request
from bs4 import BeautifulSoup

f = urllib.request.urlopen("http://itpro.nikkeibp.co.jp/article/NEWS/20120116/378602/")

#ff = open("web.html")
#f = ff.read()
#ff.close()

soup = BeautifulSoup(f)

ce = cetd.ContentExtraction()
ce.extract_content(soup.find("body"))

print(ce.get_content_text())

