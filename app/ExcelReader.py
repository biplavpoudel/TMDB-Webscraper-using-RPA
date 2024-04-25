from RPA.Excel.Files import Files

class ExcelReader:
    def __init__(self, file_path) -> None:
        self.excel = Files()
        self.path = file_path
        self.list = []
    
    def read_excel(self) -> list:
        self.excel.open_workbook(self.path)
        data = self.excel.read_worksheet(header = True)
        for item in data:
            self.list.append(item['Movie'])
        self.excel.close_workbook()
        print(self.list)
        return self.list
    

if __name__=='__main__':
    excel = ExcelReader(r"files/movies.xlsx")
    excel.read_excel()