from app.connect_database import DatabaseOperation
from app.ExcelReader import ExcelReader
from app.browser import Browser
import app.constants as constants


class Process:
    def __init__(self, browser_lib, path) -> None:
        self.browser = Browser(browser_lib)
        self.excel = ExcelReader(path)
        self.movie_list = []

    def before_run_process(self):
        self.movie_list = self.excel.read_excel()

    def run_process(self):
        for movie in self.movie_list:
            self.browser.search(movie)
            # self.browser.close_browser()
    
    def after_run_process(self):
        self.browser.close_browser()
    