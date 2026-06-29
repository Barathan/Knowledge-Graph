from bs4 import BeautifulSoup

with open("data/tn_schemes.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

print(soup.prettify()[:5000])