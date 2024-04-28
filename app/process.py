from app.connect_database import DatabaseOperation
from app.ExcelReader import ExcelReader
from app.browser import Browser
from app.connect_database import DatabaseOperation
import app.constants as constants


class Process:
    def __init__(self, browser_lib, path) -> None:
        self.browser = Browser(browser_lib)
        self.excel = ExcelReader(path)
        self.movie_list = []
        self.database = DatabaseOperation()

    def before_run_process(self):
        self.movie_list = self.excel.read_excel()
        self.database.create_table()

    def run_process(self):
        for movie in self.movie_list:
            row = self.browser.search(movie)
            self.database.insert_to_database(row)
        # self.browser.search('Jumanji')
    
    def after_run_process(self):
        self.database.close_connection()
        self.browser.close_browser()
    