from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options
import sys
sys.stdout.reconfigure(encoding='utf-8')

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
        self.sel.wait_until_element_is_visible('//*[@id="main"]/section/div/div/div[2]')
        count = self.sel.get_element_count('//*[@id="main"]/section/div/div/div[2]/section/div[1]/div/div')
        print(f"\nThe number of elements in {movie} page is {count-1}")
        #count counts extra nav-page div element

        #Now comes the comparision part
        for i in range(1, count):
            movie_name = self.sel.get_text(f'//*[@id="main"]/section/div/div/div[2]/section/div[1]/div/div[{i}]/div/div[2]/div[1]/div/div/a/h2')
            print(movie_name)



    def close_browser(self) -> None:
        self.sel.close_browser()
        # self.sel.driver.quit()

# if __name__=='__main__':
#     browser = Browser([r"https://www.themoviedb.org/", False, True])
#     browser.navigate()
#     browser.close_browser()