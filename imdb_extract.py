from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time
import pandas as pd

#shows options that imdb thinks to be the desired typed title
def show_options(driver):
        all_results = driver.find_elements_by_class_name('findSection')
        for result in all_results:
            if result.find_element_by_xpath('h3').text == 'Titles':
                matching_titles = result.find_elements_by_xpath('table/tbody/tr')

        i=1
        for title in matching_titles:
            print(str(i) + ' - ', title.text)
            i+=1
        choice = int(input('Which one? '))

        match = matching_titles[choice - 1].find_element_by_xpath('td[2]/a')
        match.click()

class WebIMDb():
    #initializing it will go from setting up the driver to searching for the desired series name
    def __init__(self, path, series_name):
        PATH = path
        self._driver = webdriver.Chrome(PATH)

        name = series_name

        self._driver.get('https://www.imdb.com/')

        search_box = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.ID, 'suggestion-search'))
        )
        search_box.click()
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)
        show_options(self._driver)

    #find main characteristics shown in page
    def find_charcs(self):
        original_title= self._driver.find_element_by_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div[2]/div').text.split(':')[1]
        overall_rating = float(self._driver.find_element_by_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]').text)
        creators= [name.text for name in  self._driver.find_elements_by_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[1]/div/ul/li')]
        longevity = self._driver.find_element_by_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div[2]/ul/li[2]/a').text
        stars = [name.text for name in self._driver.find_elements_by_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[2]/div/ul/li')]
        genres = [genre.text for genre in self._driver.find_elements_by_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div/a')]

        return original_title, overall_rating, creators, longevity, stars, genres

    #scrape each series episode
    def scrape_episodes(self):
        self._driver.find_element_by_xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div/div[1]/a').click()
        episodes = []

        select_season = Select(self._driver.find_element_by_id('bySeason'))
        seasons = select_season.options

        for index in range(len(seasons)):
            select = Select(self._driver.find_element_by_id('bySeason'))
            select.select_by_index(index)

            time.sleep(3)

            list_episodes = self._driver.find_elements_by_xpath('//*[@id="episodes_content"]/div[2]/div[2]/div')

            aux = 1
            for ep in list_episodes:
                episode = {}

                episode['Episode name'] = ep.find_element_by_xpath('div[2]/strong/a').text
                episode['Season'] =  index + 1
                episode['Number'] = aux
                episode['Release date'] = ep.find_element_by_xpath('div[2]/div[1]').text
                episode['Score'] = float(ep.find_element_by_xpath('div[2]/div[2]/div[1]/span[2]').text)

                aux+=1

                episodes.append(episode)

        series_df = pd.DataFrame(episodes, columns=['Episode name', 'Season', 'Number', 'Release date', 'Score'])        
        return series_df

    

class Series():
    def __init__(self, name):
        self._name_typed = name
    
    def set_new_aspcs(self, name, rating, creatos, years, genres, stars):
        self._name_og = name
        self._rating = rating
        self._creators = creatos
        self._years_in_air = years
        self._genres = genres
        self._main_actors = stars

    def set_episodes(self, dict):
        self._episodes = dict

    def portuguese_name(self):
        return self._name_pt
    
    def __str__(self):
        s = '''
Original title: {}
Overall rating: {}
Creator(s): {}
Years in production: {}
Genres: {}
Main actors: {}
        '''.format(self._name_og, self._rating, self._creators, self._years_in_air, self._genres, self._main_actors)

        return s

def main(): 
    name = input('Series name: ')

    local_driver = WebIMDb('/home/user/Documentos/chromedriver', name)
    serie = Series(name)

    serie.set_new_aspcs(local_driver.find_charcs())
    print(serie)
    
    local_driver.scrape_episodes().to_csv('./series_archive.csv')
    return

if __name__ == "__main__":
    main()
