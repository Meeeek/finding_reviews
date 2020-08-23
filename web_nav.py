# Web navigator parent class
# Conrad Fukuzawa
# August 2020

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

# THIS NEEDS TO CHANGE, to make it local
PATH = r"C:\Users\conra\Desktop\Scripts\chromedriver.exe"

class WebNav:
    driver = None
    url = '' # This should always be the search URL, not movie
    movie = {}
    # attrs: name, rating, director, year

    def __init__(self, name, direc):
        self.movie = {}
        self.movie['name'] = name
        self.url += self._parse_name(name) # could change to replace, to allow driver.get(URL) in here
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(PATH, options=options)

    def get_movie(self) -> dict:
        # should return a dict containing attributes
        # attrs: name, ratings, director, year
        self.driver.get(self.url) # This has to go here because in __init__ for IMDB, there is extra added onto the link
        # To move this ^^^ to the init, I should change to the replace function in the link, instead of +=
        self._add_attrs(self._search())
        return self.movie
    
    def close(self) -> None:
        # closes the webdriver
        self.driver.quit()
    
    def _parse_name(self, name) -> str:
        # This is to replace spaces with +, and handle other issues
        name = name.lower()
        name_l = name.split(' ') # split by space
        name_fin = ''
        for word in name_l: # this replaces spaces with +
            name_fin += word
            name_fin += '+'
        return name_fin[0:-1]

    def _search(self) -> str:
        # return url of first movie in search
        raise NotImplementedError

    def _add_attrs(self, url) -> None:
        # return None, add attrs to movie based off of webpage
        # url, is not the SEARCH url, but the movie URL (if it exists)
        raise NotImplementedError

    def _expand_shadow_element(self, element):
        # return shadow root element
        # shadow root has to be at the top
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root


class Rotten(WebNav):
    # subclass for rotten tomatoes

    def __init__(self, name, direc):
        self.url = r'https://www.rottentomatoes.com/search?search='
        super().__init__(name, direc)

    def _search(self) -> str:
        web = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, "main-page-content"))
        ) # This waits till the page loads
        
        # Dives into the first shadow element
        web = web.find_element(By.TAG_NAME, "search-result-container")
        shad1 = self._expand_shadow_element(web)

        # Checking to make sure a search option is found
        web2 = None
        for option in shad1.find_elements_by_tag_name('search-result'):
            if option.get_attribute('type') == 'movie':
                web2 = option
        if not web2:
            print("Error, not found")
            return
        # second shadow element
        shad2 = self._expand_shadow_element(web2)

        # getting the url in the 2nd shadow element then returning url
        return shad2.find_element_by_tag_name('media-row').get_attribute('url')

    def _add_attrs(self, url) -> None:
        src = requests.get(url).text
        soup = BeautifulSoup(src, 'lxml')

        # This gets the rating
        self.movie['rating'] = int(soup.find('a', id="tomato_meter_link")\
            .find('span', class_="mop-ratings-wrap__percentage").text.strip()[0:-1])

        # This finds the director
        self.movie['director'] = soup.find('div', id="mainColumn")\
            .find('section', class_="panel panel-rt panel-box movie_info media")\
                .find('ul', class_="content-meta info").find_all('li')[2]\
                    .find('div', class_="meta-value").a.text
        
        # This gets the synoposis
        self.movie['synopsis'] = soup.find('div', id="movieSynopsis").text.strip()

        print(self.movie)


class Imdb(WebNav):
    # subclass for IMDB
   
    def __init__(self, name, direc):
        self.url = r'https://www.imdb.com/find?q='
        super().__init__(name, direc)
        self.url += '&s=tt&ttype=ft&ref_=fn_ft'

    def _search(self):
        # This part can be done with beautifulsoup4, no shadow
        # This part should really be changed honestly
        self.close()
        src = requests.get(self.url).text
        soup = BeautifulSoup(src, 'lxml')

        # This finds the link
        mov_url = soup.find('div', id="main")\
            .find('table', class_="findList")\
                .find('tr', class_="findResult odd")\
                    .find('td', class_="result_text")\
                        .a['href']
        mov_url = r'https://www.imdb.com/' + mov_url
        return mov_url

    def _add_attrs(self, url) -> None:
        src = requests.get(url).text
        soup = BeautifulSoup(src, 'lxml')

        # This gets the rating it is /10 so we multiply by 10
        rat_float = float(soup.find('div', class_="ratingValue")\
            .find('strong')['title'][0:3])
        self.movie['rating'] = int(rat_float*10)

        # This gets the title (still needs parsing)
        self.movie['title'] = soup.find('div', class_="titleBar")\
            .find('div', class_="title_wrapper").h1.text
        
        # This gets the year
        self.movie['year'] = soup.find("span", id="titleYear").a.text



class Meta(WebNav):
    # subclass for metacritic
   
    def __init__(self, name, direc):
        self.url = r'https://www.metacritic.com/search/movie/' # this search is to filter to movie
        super().__init__(name, direc)
        self.url += r'/results' # this is because the link has to end with this

    def _search(self):
        # can be found using BS4, similar to the IMDB website
        src = requests.get(self.url).text
        soup = BeautifulSoup(src, 'lxml')

        # This finds the link
        print(soup.prettify())
        mov_url = soup.find('div', id="main_content")\
            .find('div', class_="module search_results fxdcol gu6")\
                #.find('ul', class_="search_results module")\
                    #.find('li', class_="result first_result")\
            #             .find('div', class_="main_stats")\
            #                 .h3.a['href']
        print("worked")
        exit()
        
        # This is to add the beginning bits, the href cuts it off normally
        mov_url = r'https://www.metacritic.com/' + mov_url
        return mov_url

    def _add_attrs(self, url) -> None:
        src = requests.get(url).text
        soup = BeautifulSoup(src, 'lxml')

        # Finding the title
        # ' Reviews - Metacritic' is always added onto the end
        self.movie['title'] = soup.head\
            .title.text[0: -1*len(' Reviews - Metacritic')]

        # Finding the rating
        self.movie['rating'] = soup.find('div', id="main_content")\
            .find('table', class_="maskedauto")\
                .find('span', class_="metascore_w larger movie positive")\
                    .text

        # Finding the year
        self.move['year'] = soup.find('div', class_="details_section")\
            .find("div", class_="release_date")\
                .find("span", class_=False).text

        # Finding the director
        # dont do this lol