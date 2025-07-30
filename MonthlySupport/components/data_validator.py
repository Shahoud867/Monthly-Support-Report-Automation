from langflow.custom import Component
from langflow.io import Output, Input, IntInput
from langflow.schema import Data

class DataValidator(Component):
    display_name = "Data Validator"
    description = "Validate data quality and completeness"
    
    inputs = [
        Input(display_name="Data", name="data_input"),
        IntInput(name="min_records", display_name="Minimum Records", value=1)
    ]
    
    outputs = [
        Output(display_name="Validated Data", name="validated_data", method="validate_data")
    ]
    
    def validate_data(self) -> Data:
        df = self.data_input.value
        
        # Data validation checks
        if len(df) < self.min_records:
            raise ValueError(f"Insufficient data: {len(df)} records, minimum {self.min_records}")
        
        # Remove invalid records
        df = df.dropna(subset=['ticket_description', 'open_date', 'close_date'])
        
        return Data(value=df)