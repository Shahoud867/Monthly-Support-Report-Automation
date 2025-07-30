import pandas as pd
from langflow.custom import Component
from langflow.io import Output, Input, StrInput
from langflow.schema import Data

class DateFilter(Component):
    display_name = "Date Filter"
    description = "Filter tickets by target month"
    
    inputs = [
        Input(display_name="Data", name="data_input"),
        StrInput(
            name="target_month",
            display_name="Target Month (YYYY-MM)",
            value="2025-05"
        )
    ]
    
    outputs = [
        Output(display_name="Filtered Data", name="filtered_data", method="filter_by_month")
    ]
    
    def filter_by_month(self) -> Data:
        df = self.data_input.value
        
        # Filter by target month
        target_date = pd.to_datetime(self.target_month)
        filtered_df = df[
            (df['open_date'].dt.year == target_date.year) & 
            (df['open_date'].dt.month == target_date.month)
        ].copy()
        
        return Data(value=filtered_df)