from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options
import unittest

# sel = Selenium()

class Browser():
    def __init__(self, browser_lib) -> None:
        self.sel= Selenium()
        self.url, self.headless, self.maximize = browser_lib
        try:
            options = Options()
            # options.add_argument("--no-sandbox")
            # options.add_argument("--disable-gpu")
            # self.sel.open_available_browser(url = self.url, headless=self.headless, browser_selection='chrome', maximized = self.maximize, options = options)
            self.sel.open_chrome_browser(url=self.url)
        except Exception as e:
            print(f"Error captured as: {str(e)}")
            self.sel.driver.quit()
        else:
            print("Browser successfully opened!")

        
    def search(self, movie) -> None:
        self.sel.go_to(self.url+ f"search/movie?query={movie}")
        self.sel.wait_until_element_is_visible('//*[@id="main"]/section/div/div/div[2]')
        count = self.sel.get_element_count('//*[@id="main"]/section/div/div/div[2]/section/div[1]/div/div') - 1
        print(f"The number of elements in {movie} page is {count}")
        


    def close_browser(self) -> None:
        self.sel.close_browser()
        # self.sel.driver.quit()

# if __name__=='__main__':
#     browser = Browser([r"https://www.themoviedb.org/", False, True])
#     browser.navigate()
#     browser.close_browser()