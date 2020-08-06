import urllib
from bs4 import BeautifulSoup
import csv
import re

class Anime:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
    def __repr__(self):
        return 'Name: %s Rating: %d' % (self.name, self.rating)

def make_animes(anime_list):
    animes = []
    RANK_URL = "http://www.nihonreview.com/images/rank"
    def is_url_rating(src):
        return RANK_URL in src
    for child in anime_list:
        try:
            url = child.a["href"]
            body = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(body, 'html.parser')
            title = soup.find("div", {"class" : "post"}).h2.text
            print(title)
            rating = int(re.findall('\d+', soup.find("img", src=is_url_rating)["src"])[0])
        except Exception as e:
            print('Anime: %s not included Error: %s' % (title, str(e)))
            continue
        animes.append(Anime(title, rating))
    return animes

if __name__ == "__main__":
    home = "http://www.nihonreview.com/anime/"
    response = urllib.request.urlopen(home)
    body = response.read()
    soup = BeautifulSoup(body, 'html.parser')
    anime = soup.find("li", {"class" : "page_item page-item-47 page_item_has_children current_page_item"})
    anime_list = anime.findChildren("li", recursive=True)
    animes = make_animes(anime_list)
    animes.sort(key=lambda a: a.rating)
    print(animes)
    with open('animes.csv', 'w') as f:
        writer = csv.writer(f)
        for anime in animes:
            writer.writerow(str(anime))