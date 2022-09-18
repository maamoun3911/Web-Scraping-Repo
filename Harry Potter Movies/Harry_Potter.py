import pandas as pd
import requests
from bs4 import BeautifulSoup


class webScrapping():
    main_url = 'https://www.imdb.com/list/ls072049366/'
    def __init__(self, url):
        self.url = url
    def get_Doc(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to load Page {self.url}")
        page_Content = response.text
        Doc = BeautifulSoup(page_Content, 'html.parser')
        return Doc
    def scrapping_info(self, Doc):
        self.Doc, j = Doc, 0
        self.title_list, self.certificate, self.runtime = [""]*8, [""]*8, [""]*8
        self.IMDBRate, self.metaScoreRate, self.Links = [0]*8, [0]*8, [""]*8
        self.releaseYear, self.genres = [0]*8, [0]*8
        title_tag = Doc.find_all('h3', class_='lister-item-header')
        parents_tag = self.Doc.find_all('div', 'lister-item-content')
        for i in range(13):
            title = title_tag[i].find_all('a')[0].text
            link_title = title_tag[i].find_all('a')[0]
            if title[:20] == 'Harry Potter and the':
                self.genres[j] = parents_tag[i].find('span', 'genre').text.strip()
                self.releaseYear[j] = int(parents_tag[i].find('span', class_='lister-item-year text-muted unbold').text[1:5])
                self.Links[j] = 'https://www.imdb' + link_title['href']
                self.metaScoreRate[j] = int(parents_tag[i].find('span', 'metascore favorable').text)
                self.IMDBRate[j] = parents_tag[j].find('span', class_='ipl-rating-star__rating').text + "/10"
                self.runtime[j] = parents_tag[i].find('span', class_='runtime').text
                self.certificate[j] = parents_tag[i].find('span', 'certificate').text
                self.title_list[j] = title
                j += 1
    def main_wScrapping_fun(self):
        test = self.scrapping_info(self.get_Doc())
        HarryPotter_DF = pd.DataFrame({'Title':self.title_list, 'Release Year':self.releaseYear,
        'Genre':self.genres, 'Certificate':self.certificate, 'Runtime':self.runtime,
        "IMDB Rating":self.IMDBRate, 'Metascore Rate':self.metaScoreRate, "Film Page":self.Links})
        return HarryPotter_DF
page = webScrapping(webScrapping.main_url)
print(page.main_wScrapping_fun())
