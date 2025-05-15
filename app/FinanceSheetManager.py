from gspread_formatting import CellFormat, Color, TextFormat, format_cell_range, NumberFormat
from typing import List
from datetime import datetime
from gspread import Cell, Worksheet, Spreadsheet
from config.sheet_client import spreadsheet, worksheet
from tickets.app_config import GOOGLE_SHEETS_CREDENTIALS
from gspread.exceptions import APIError
class FinanceSheetManager:
    TOTAL_COLUMN_NAME = "Total"
    DATE_COLUMN_NAME  = "Date"
    def __init__(self, name: str, spreadsheet: Spreadsheet, worksheet: Worksheet, columns: list):
        self.name = f"{name} Finance's"
        self.set_columns(columns)
        self.spreadsheet = spreadsheet
        self.worksheet = worksheet

    def set_columns(self, columns: list):
        self.columns = [self.get_column_name_formatted(col) for col in columns]
        if self.TOTAL_COLUMN_NAME not in self.columns:
            self.columns.append(self.TOTAL_COLUMN_NAME)
        self.columns_length = len(self.columns)

        
    def sum_or_create(self, value: float, column_name: str):
        try: 
            if self.have_to_create_new():
                 self.create_first_sheet()
            self.sum_value_or_add_row(value, self.get_column_name_formatted(column_name))
            return self.worksheet.url
        except Exception as e:
            print(f"Error in sum_or_create: {e}")
            raise RuntimeError("Error in sum_or_create") from e
        
    def have_to_create_new(self) -> bool:
        try: 
            self.spreadsheet.add_worksheet(title=self.name, rows=100, cols=(self.columns_length + 10))
            return True 
        except APIError as e:
            if e.code == 400:
                return False  
    
    def worksheets(self) -> List[Worksheet]:
        return self.spreadsheet.worksheets()
    
    def get_actual_date(self) -> str:
        return datetime.now().replace(day=1).strftime("%Y-%m-%d")
    
    def create_first_sheet(self):
        self.create_new_profile()
        date = self.get_cell_date()
        cell_names = self.get_cells_names()
        initial_new_row = self.get_initial_new_row()
        self.worksheet.update_cells(date + cell_names + initial_new_row)
        self.sort_by_date_desc()
    
    def sum_value_or_add_row(self, value: float, column_name: str):
        last_date =  self.get_last_date()
        if last_date != self.get_actual_date():
            self.add_new_row()
        self.sum_value_to(value, column_name)
        self.sum_value_to(value, self.TOTAL_COLUMN_NAME)

    
    def get_last_date(self) -> str:
        try: 
            return self.worksheet.col_values(1)[1]
        except IndexError:
            return None
    
    def add_new_row(self):
        new_row = self.get_initial_new_row()
        self.worksheet.update_cells(new_row)
        self.sort_by_date_desc()
        
    def sum_value_to(self, value: float, column_name: str):
        column_index = self.worksheet.find(column_name).col
        cell = self.worksheet.cell(2, column_index)
        cell.value = float(cell.value) + float(value)
        self.worksheet.update_cell(cell.row, cell.col, cell.value)
        
    def range_of_columns(self, first_cell: str, length: int) -> str:
        col_letter = first_cell[0].upper()
        row_number = first_cell[1:]
        start_col = ord(col_letter)
        end_col = start_col + length
        return f"{col_letter}{row_number}:{chr(end_col)}{row_number}"

    def get_format_columns_names(self) -> List[CellFormat]:
        format = CellFormat(
            verticalAlignment="MIDDLE",
            horizontalAlignment="CENTER",
            backgroundColor=Color(19/255, 46/255, 87/255),
            textFormat=TextFormat(
                foregroundColor=Color(1.0, 1.0, 1.0),
                bold=True
            )
        )
        return format
    
  

    def create_new_profile(self):
        try: 
            self.worksheet = self.spreadsheet.add_worksheet(title=self.name, rows=100, cols=(self.columns_length + 10))
            print(self.worksheet.__dict__)
        except APIError as e:
            if e.code == 400:
                print("Worksheet already exists. Updating the title.")
                self.worksheet = self.spreadsheet.worksheet(self.name)
        # self.worksheet.title = self.name
        # pass

    
    def get_cell_date(self) -> List[Cell]:
        cells_date = self.worksheet.range("A1")
        cells_date[0].value = "Date"
       
        format_title = CellFormat(
            horizontalAlignment="CENTER",
            verticalAlignment="MIDDLE",
            backgroundColor=Color(131/255, 160/255, 206/255),
            textFormat=TextFormat(
                foregroundColor=Color(1.0, 1.0, 1.0),
                bold=True
            )
        )

        format_cell_range(self.worksheet, "A1", format_title)

        return cells_date
    
    def get_date_format(self) -> CellFormat:
        return CellFormat(
            horizontalAlignment="CENTER",
            verticalAlignment="MIDDLE",
            backgroundColor=Color(239/255, 239/255, 239/255),
            numberFormat=NumberFormat(
                type="DATE",
                pattern="YYYY-MM-DD"
            )
        )
    
    def sort_by_date_desc(self):
        sort_request = {
            "requests": [
                {
                    "sortRange": {
                        "range": {
                            "sheetId": self.worksheet._properties["sheetId"],
                            "startRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": self.columns_length + 1
                        },
                        "sortSpecs": [
                            {
                                "dimensionIndex": 0,  # Column A (Date)
                                "sortOrder": "DESCENDING"
                            }
                        ]
                    }
                }
            ]
        }
        self.spreadsheet.batch_update(sort_request)    
        
    def get_column_name_formatted(self, column_name: str) -> str:
        return column_name.capitalize()
    
    def get_url(self) -> str:
        return self.spreadsheet.worksheet(self.name).url
    
    def total_category(self, category: str) -> float:
        format_name = self.get_column_name_formatted(category)
        category_column = self.worksheet.col_values(self.worksheet.find(format_name).col)[1:]
        return category_column.sum() if category_column else 0.0
    
    def total(self) -> float:
        return self.worksheet.col_values(self.worksheet.find(self.TOTAL_COLUMN_NAME).col)[2]

    def get_cells_names(self) -> List[Cell]:
        format = self.get_format_columns_names()
        
        range_list = self.range_of_columns("B1", self.columns_length - 1) # rest 1 for the date
        cell_list = self.worksheet.range(range_list)
        format_cell_range(self.worksheet, range_list, format)
        for i, cell in enumerate(cell_list):
            try:  
                if i == self.columns_length: 
                    break
                print(self.columns[i])
                cell.value = self.columns[i]
               
            except Exception as e:
                print(f"Rompio todo en get_cells_names indice {i}: {e}")
        return cell_list

    def get_initial_new_row(self) -> List[Cell]:
        number_format = CellFormat(
            verticalAlignment="MIDDLE",
            horizontalAlignment="CENTER",
        )
        format_title = CellFormat(
            horizontalAlignment="CENTER",
            verticalAlignment="MIDDLE",
            backgroundColor=Color(131/255, 160/255, 206/255),
            textFormat=TextFormat(
                foregroundColor=Color(1.0, 1.0, 1.0),
                bold=True
            )
        )
        number_range = self.range_of_columns("A2", self.columns_length)
        
        format_cell_range(self.worksheet, "A1", format_title)
        format_cell_range(self.worksheet, number_range, number_format)
        
        cell_number_list = self.worksheet.range(number_range)
        for cell in cell_number_list:
            cell.value = 0
            
        cell_number_list[0].value = self.get_actual_date()
            
        return cell_number_list
    
if __name__ == "__main__":
    name = "rey"
    columns = [
        "comida",
        "transporte",
        "entretenimiento",
        "servicios",
        "otros"
    ]
    finance_manager = FinanceSheetManager(name, spreadsheet, worksheet, columns)
    finance_manager.sum_or_create(100, "comida")

    # finance_manager.worksheet.title = "mateos"
    # cell_names = finance_manager.get_cells_names()
    # initial_new_row = finance_manager.get_new_row()
    # # print(cell_names, initial_new_row)
    # worksheet.update_cells(cell_names + initial_new_row)