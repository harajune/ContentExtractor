import cetd
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<!--
 coommennts!!!!
 -->

<p class="story">...</p>
</body>
</html>
"""

soup = BeautifulSoup(html_doc)

ce = cetd.ContentExtraction()
ce.calc_ctdds(soup.find("body"))

nodes = ce.get_nodes()

for n in nodes:
    print("%f:%s" % (n[1], n[0].name))

