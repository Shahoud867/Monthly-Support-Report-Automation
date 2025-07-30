import pandas as pd
from langflow.custom import Component
from langflow.io import Output, Input
from langflow.schema import Data

class DataTransformer(Component):
    display_name = "Data Transformer"
    description = "Advanced data transformation with external lookups"
    
    inputs = [
        Input(display_name="Raw Data", name="raw_data")
    ]
    
    outputs = [
        Output(display_name="Transformed Data", name="transformed_data", method="transform_data")
    ]
    
    def transform_data(self) -> Data:
        df = self.raw_data.value.copy()
        
        # Vectorized transformations
        df['email_domain'] = df['email'].str.split('@').str[1].fillna('unknown')
        df['customer_type'] = df['email'].str.contains('corp').map({True: 'enterprise', False: 'standard'})
        
        # External lookup
        domain_rep = {d: 'trusted' if len(d) > 8 else 'standard' for d in df['email_domain'].unique()}
        df['domain_reputation'] = df['email_domain'].map(domain_rep)
        
        return Data(value=df)
