import pandas as pd
import requests
from bs4 import BeautifulSoup

main_url = 'https://www.imdb.com/list/ls072049366/'

def get_Doc(main_url):
    response = requests.get(main_url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {main_url}")
    page_Content = response.text
    Doc = BeautifulSoup(page_Content, 'html.parser')
    return Doc
Doc = get_Doc(main_url)

# getting info with strip()
# parent_title_tag[i], 'span', 'metascore favorable'
get_metascore = lambda parent_tag, tag_name, class_ : parent_tag.find(tag_name, class_).text.strip()

# getting info without strip()
get_info = lambda Doc, tag_name, class_ : Doc.find(tag_name, class_).text

# another big function, first we find the title of real films, then and deppend on the result
# we find other things relate to each film like rate, link, parent's guide, and other things ....
# this function contains lot of helper funtions
def scraping_titles(Doc):
    title_list, our_numbers, films_links, certificate, metascore, imdb_rate, runtime = [], [], [], [], [], [], []
    parent_title_tag = Doc.find_all('div', class_='lister-item-content')
    title_tag = Doc.find_all('h3', class_='lister-item-header')
    for i in range(13):
        title = title_tag[i].find_all('a')
        the_title = title[0].text
        if the_title[:20] == 'Harry Potter and the':
            runtime.append(get_info(parent_title_tag[i], 'span', 'runtime'))
            certificate.append(get_info(parent_title_tag[i], 'span', 'certificate'))
            imdb_rate.append(get_info(parent_title_tag[i], 'span', 'ipl-rating-star__rating'))
            metascore.append(get_metascore(parent_title_tag[i], 'span', 'metascore favorable'))
            title_list.append(the_title)
            films_links.append('https://www.imdb' + title[0]['href'])
            our_numbers.append(i)
    return title_list, our_numbers, films_links, certificate, metascore, imdb_rate, runtime

# finding all info in specific class without stripping() it
scrapping_without_strip = lambda Doc, numbers, class_ : [Doc.find_all('span', {'class' : class_})[i].text for i in numbers]

# finding all info in specific class with stripping() it
scrapping_with_strip = lambda Doc, numbers, class_ : [Doc.find_all('span', {'class' : class_})[i].text.strip() for i in numbers]

# main functions wich conatains the result from all other function
def web_Scraping(Doc):
    films_title, numbers, films_links, certifications, metascores, imdb_rates, runtime = scraping_titles(Doc)
    movie_number = [i for i in range(1, len(numbers)+1)]
    release_year = scrapping_without_strip(Doc, numbers, 'lister-item-year text-muted unbold')
    genre = scrapping_with_strip(Doc, numbers, 'genre')
    Movies_Series_DF = pd.DataFrame({'Index':movie_number, 'Title':films_title, 'Genre':genre, 'Year':release_year, 'runtime':runtime, "Certifications":certifications, 'IMDB Rate':imdb_rates, 'Metascores Rate':metascores, "Film Link":films_links})
    Movies_Series_DF.to_csv('Harry_Potter_Series.txt', index=None)
print(web_Scraping(Doc))
