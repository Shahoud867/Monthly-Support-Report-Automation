import pandas as pd
import sqlite3
from langflow.custom import Component
from langflow.io import Output, DropdownInput, StrInput
from langflow.schema import Data

class DataLoader(Component):
    display_name = "Data Loader"
    description = "Load ticket data from CSV or SQLite database"
    
    inputs = [
        DropdownInput(
            name="data_source",
            display_name="Data Source",
            options=["csv", "sqlite"],
            value="csv"
        ),
        StrInput(
            name="file_path", 
            display_name="File Path",
            value="c:\\MonthlySupport\\tickets.csv"
        )
    ]
    
    outputs = [
        Output(display_name="Data", name="data_output", method="load_data")
    ]
    
    def load_data(self) -> Data:
        if self.data_source == "csv":
            df = pd.read_csv(self.file_path)
        else:
            conn = sqlite3.connect("c:\\MonthlySupport\\tickets.db")
            df = pd.read_sql_query("SELECT * FROM tickets", conn)
            conn.close()
        
        # Convert dates
        df['open_date'] = pd.to_datetime(df['open_date'])
        df['close_date'] = pd.to_datetime(df['close_date'])
        df['resolution_days'] = (df['close_date'] - df['open_date']).dt.days
        
        return Data(value=df)