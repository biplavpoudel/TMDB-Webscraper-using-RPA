from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options
from app.constants import *
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
            raise e
        else:
            print("Browser successfully opened!")
        self.reviews = []
        self.status = ""

        
    def search(self, movie) -> None:
        self.sel.go_to(self.url+ f"search/movie?query={movie}")
        # time.sleep(5)

        #Xpath changes if the number of tv shows is greater than the movie, hence the bug😑 //*[@id="main"]/section/div/div/div[2]/section/div[1]
        # I think @class = 'search_results movie' dosnt exist for skhgfkjs, hence the error?
        #//*[@id="main"]/section/div/div/div[2]/section/div[1]/div/p:There are no movies that matched your query.
        count = self.sel.get_element_count(movie_card_path + 'div')
        if count == 0:
            count = 0
            # rating = None
            # genre = None
            # audience_score = None
            # storyline = None
            # reviews = None
            # print(f"\nThe number of elements in {movie} page is {count}")
            result = self.init_scraping(movie, count)
        else:
            count = count - 1
            # print(f"\nThe number of elements in {movie} page is {count}")
        #count counts extra nav-page div element

        #Now comes the comparision part
        movie_dict = {}
        if count > 0:
            for i in range(1, count+1):
                try:
                    movie_name = self.sel.get_text(movie_card_path + f'div[{i}]/' +second_part_path+ 'h2')
                    release_date = self.sel.get_text(movie_card_path + f'div[{i}]//span[@class="release_date"]')
                    formatted_release_date = datetime.strptime(release_date, "%B %d, %Y").date()
                    # print(movie_name, formatted_release_date)
                    movie_dict[i] = (movie_name, formatted_release_date)
                    # if movie_name == movie and release_date is not None:
                except:
                    # print("Locator error!")
                    movie_name = movie
                    formatted_release_date = None
                    movie_dict[i] = (movie, formatted_release_date)
                else:
                    # print("Locators found match!")
                    pass

            # print("Movie and their release dates are:", movie_dict)
            first_key = next(iter(movie_dict))
            latest_movie, latest_date = movie_dict[first_key]
            latest_index = first_key
            if count == 1:
                self.sel.click_link(single_movie_link)
                result = self.init_scraping(movie, count)
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
                self.sel.click_link(movie_card_path + f'div[{latest_index}]/' + full_remaining_movie_link)
                result = self.init_scraping(movie, count)
        print("RESULTS: ", result)
        return result
    
    def init_scraping(self, movie_name, count):
        if self.sel.does_page_contain_element('//*[@id="consensus_pill"]'):
            score = self.sel.get_element_attribute('//*[@id="consensus_pill"]//span', "class")
            audience_score = score[-2:]
        else:
            audience_score = "N/A"
        # print("The user score is:", audience_score)
        if self.sel.does_page_contain_element(certification_link):
            rating = self.sel.get_text(certification_link)
        else:
            rating = "N/A"
        # print("The rating for the movie is: ", rating)
        if self.sel.does_page_contain_element(genre_link):
            genre = self.sel.get_text(genre_link)
        else:
            genre = "N/A"
        # print("The genre of the movie is: ", genre)
        if self.sel.does_page_contain_element(storyline_link):
            storyline = self.sel.get_text(storyline_link + '//div/p')
        else:
            storyline = "N/A"
        # print("The storyline of the movie is: ", storyline)
        self.reviews, self.status = self.get_reviews(count)
        print("The name of the movie is: ", movie_name)
        print("\nThe reviews for the movie are: ", self.reviews)

        return [movie_name, audience_score, storyline, rating, genre, self.reviews[0], self.reviews[1], self.reviews[2], self.reviews[3], self.reviews[4], self.status]


    def get_reviews(self, count)->list:
        self.reviews=[]
        limit = 5
        self.status = ""
        if count == 0:
            self.reviews = [None]*5
            self.status = "No match found"
            return (self.reviews, self.status)
        else:
            self.sel.scroll_element_into_view(review_into_view_link)
            if self.sel.does_page_contain_element(actual_review_link):
                # time.sleep(5)
                self.sel.click_element_when_clickable(actual_review_link)
                number_of_reviews = self.sel.get_element_count(count_of_reviews + '/div[1]/div')
                print("\nThe number of reviews is:", number_of_reviews)
                for i in range (0, limit):
                    if self.sel.does_page_contain_element(count_of_reviews+ f'//div[{i+1}]'):
                        self.reviews.append(self.sel.get_text(count_of_reviews+ f'//div[{i+1}]//div[@class="teaser"]'))
                    else:
                        self.reviews.append(None)
            else:
                self.reviews = [None]*5
            # while(len(self.reviews)) < 5 :
            #     self.reviews.append(None)
            self.status = "Match found"
            return (self.reviews, self.status)

    def close_browser(self) -> None:
        self.sel.close_browser()
        # self.sel.driver.quit()

# if __name__=='__main__':
#     browser = Browser([r"https://www.themoviedb.org/", False, True])
#     browser.navigate()
#     browser.close_browser()