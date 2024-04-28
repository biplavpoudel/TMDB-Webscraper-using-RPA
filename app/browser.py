from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options
import sys
sys.stdout.reconfigure(encoding='utf-8') #to support encoding of non-latin characters
from datetime import datetime
import time

# sel = Selenium()

class Browser():
    def __init__(self, browser_lib) -> None:
        self.sel= Selenium()
        self.url, self.headless, self.maximize = browser_lib
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            self.sel.open_available_browser(url = self.url, headless=self.headless, maximized = self.maximize, options = options)
        except Exception as e:
            print(f"Error captured as: {str(e)}")
            self.sel.driver.quit()
        else:
            print("Browser successfully opened!")

        
    def search(self, movie) -> None:
        self.sel.go_to(self.url+ f"search/movie?query={movie}")
        # time.sleep(5)

        #Xpath changes if the number of tv shows is greater than the movie, hence the bug😑 //*[@id="main"]/section/div/div/div[2]/section/div[1]
        # I think @class = 'search_results movie' dosnt exist for skhgfkjs, hence the error?
        #//*[@id="main"]/section/div/div/div[2]/section/div[1]/div/p:There are no movies that matched your query.
        count = self.sel.get_element_count('//*[@id="main"]/section/div/div/div[2]/section/div[@class="search_results movie "]/div/div')
        if count == 0:
            count = 0
            # rating = None
            # genre = None
            # audience_score = None
            # storyline = None
            # reviews = None
            print(f"\nThe number of elements in {movie} page is {count}")
            self.init_scraping()
        else:
            count = count - 1
            print(f"\nThe number of elements in {movie} page is {count}")
        #count counts extra nav-page div element

        #Now comes the comparision part
        movie_dict = {}
        if count > 0:
            for i in range(1, count+1):
                try:
                    movie_name = self.sel.get_text(f'//*[@id="main"]/section/div/div/div[2]/section/div[@class="search_results movie "]/div/div[{i}]/div/div[2]/div[1]/div/div/a/h2')
                    release_date = self.sel.get_text(f'//*[@id="main"]/section/div/div/div[2]/section/div[@class="search_results movie "]/div/div[{i}]//span[@class="release_date"]')
                    formatted_release_date = datetime.strptime(release_date, "%B %d, %Y").date()
                    # print(movie_name, formatted_release_date)
                    movie_dict[i] = (movie_name, formatted_release_date)
                    # if movie_name == movie and release_date is not None:
                except:
                    # print("Locator error!")
                    movie_name = movie_name
                    formatted_release_date = None
                    movie_dict[i] = (movie_name, formatted_release_date)
                else:
                    # print("Locators found match!")
                    pass

            # print("Movie and their release dates are:", movie_dict)
            first_key = next(iter(movie_dict))
            latest_movie, latest_date = movie_dict[first_key]
            latest_index = first_key
            if count == 1:
                self.sel.click_link(f'//*[@id="main"]/section/div/div/div[2]/section/div[@class="search_results movie "]/div/div[1]/div/div[2]/div[1]/div/div/a[@data-media-type="movie"]')
                self.init_scraping()
            else:
                for index, (movie_name, release_date) in movie_dict.items():
                    if movie_name == movie:
                        if release_date is None:
                            continue
                        elif release_date > latest_date:
                            latest_date = release_date
                            latest_index = index
                            latest_movie = movie_name
                # print(f"Latest index and date for {latest_movie} is: {latest_index} and {latest_date}")
                self.sel.click_link(f'//*[@id="main"]/section/div/div/div[2]/section/div[@class="search_results movie "]/div/div[{latest_index}]/div/div[2]/div[1]/div/div/a[@data-media-type="movie"]')
                self.init_scraping()
    
    def init_scraping(self):
        if self.sel.does_page_contain_element('//*[@id="consensus_pill"]'):
            score = self.sel.get_element_attribute('//*[@id="consensus_pill"]/div/div[1]/div/div/div/span', "class")
            audience_score = score[-2:]
        else:
            audience_score = None
        print("The user score is:", audience_score)
        if self.sel.does_page_contain_element('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="certification"]'):
            rating = self.sel.get_text('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="certification"]')
        else:
            rating = None
        print("The rating for the movie is: ", rating)
        if self.sel.does_page_contain_element('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="genres"]'):
            genre = self.sel.get_text('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="genres"]')
        else:
            genre = None
        print("The genre of the movie is: ", genre)



    def close_browser(self) -> None:
        self.sel.close_browser()
        # self.sel.driver.quit()

# if __name__=='__main__':
#     browser = Browser([r"https://www.themoviedb.org/", False, True])
#     browser.navigate()
#     browser.close_browser()