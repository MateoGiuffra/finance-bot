from gspread_formatting import CellFormat, Color, TextFormat, format_cell_range, NumberFormat
from typing import List
from datetime import datetime
from gspread import Cell, Worksheet, Spreadsheet


class FinanceSheetManager:
    def __init__(self, name: str, spreadsheet: Spreadsheet, worksheet: Worksheet, columns: list):
        self.name = f"{name} Finance's"
        self.columns = columns
        self.columns_length = len(columns)
        self.spreadsheet = spreadsheet
        self.worksheet = worksheet

    def set_columns(self, columns: list):
        self.columns = columns
        self.columns_length = len(columns)
    
        
    def sum_or_create(self, value: float, column_name: str):
        if self.have_to_create_new():
             self.create_first_sheet()
        self.sum_value_or_add_row(value, column_name.capitalize())
        return self.worksheet.url
        
    def have_to_create_new(self) -> bool:
        return any(ws.title != self.name for ws in self.worksheets()) or not self.get_last_date()
    
    def worksheets(self) -> List[Worksheet]:
        return self.spreadsheet.worksheets()
    
    def get_actual_date(self) -> str:
        return datetime.now().replace(day=1).strftime("%Y-%m-%d")
    
    def create_first_sheet(self):
        self.create_new_profile()
        dates = self.get_cells_date()
        cell_names = self.get_cells_names()
        zero_values = self.get_first_cells_values()
        self.worksheet.update_cells(dates + cell_names + zero_values)
        self.sort_by_date_desc()
    
    def sum_value_or_add_row(self, value: float, column_name: str):
        last_date =  self.get_last_date()
        if last_date != self.get_actual_date():
            self.add_new_row()
        self.sum_value_to(value, column_name)
    
    def get_last_date(self) -> str:
        try: 
            return self.worksheet.col_values(1)[1]
        except IndexError:
            return None
    
    def add_new_row(self):
        self.worksheet.append_row([self.get_actual_date(), *[0] * (self.columns_length)])
        last_row_index = len(self.worksheet.col_values(1))

        number_format = CellFormat(
            horizontalAlignment="CENTER",
            verticalAlignment="MIDDLE"
        )

        format_cell_range(self.worksheet, f"A{last_row_index}", self.get_date_format())

        column_end = chr(ord("A") + self.columns_length - 1)
        format_cell_range(self.worksheet, f"B{last_row_index}:{column_end}{last_row_index}", number_format)

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
        end_col = start_col + length - 1
        return f"{col_letter}{row_number}:{chr(end_col)}{row_number}"

    def get_cells_names(self) -> List[Cell]:
        format = CellFormat(
            verticalAlignment="MIDDLE",
            horizontalAlignment="CENTER",
            backgroundColor=Color(19/255, 46/255, 87/255),
            textFormat=TextFormat(
                foregroundColor=Color(1.0, 1.0, 1.0),
                bold=True
            )
        )
        range_list = self.range_of_columns("B1", self.columns_length)
        cell_list = self.worksheet.range(range_list)
        format_cell_range(self.worksheet, range_list, format)

        for cell, column_value in zip(cell_list, self.columns):
            cell.value = column_value
        return cell_list

    def get_first_cells_values(self) -> List[Cell]:
        number_format = CellFormat(
            verticalAlignment="MIDDLE",
            horizontalAlignment="CENTER",
        )
        number_range = self.range_of_columns("B2", self.columns_length)
        format_cell_range(self.worksheet, number_range, number_format)
        cell_number_list = self.worksheet.range(number_range)
        for cell in cell_number_list:
            cell.value = 0
        return cell_number_list

    def create_new_profile(self):
        self.worksheet = self.spreadsheet.add_worksheet(title=self.name, rows=100, cols=self.columns_length + 10)

    def get_cells_date(self) -> List[Cell]:
        cells_date = self.worksheet.range("A1:A2")

        cells_date[0].value = "Date"
        cells_date[1].value = self.get_actual_date()

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
        format_cell_range(self.worksheet, "A2", self.get_date_format())

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
    
    def get_url(self) -> str:
        return self.spreadsheet.url
    
    # TODO: Implement total_category and total methods
    
    

