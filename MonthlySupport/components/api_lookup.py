from langflow.custom import Component
from langflow.io import Output, Input, StrInput
from langflow.schema import Data

class APILookup(Component):
    display_name = "API Lookup"
    description = "External API data enrichment"
    
    inputs = [
        Input(display_name="Data", name="data_input"),
        StrInput(name="api_endpoint", display_name="API Endpoint", value="https://api.example.com/lookup")
    ]
    
    outputs = [
        Output(display_name="Enriched Data", name="enriched_data", method="lookup_data")
    ]
    
    def lookup_data(self) -> Data:
        df = self.data_input.value.copy()
        
        # Mock external API lookup
        unique_domains = df['email_domain'].unique() if 'email_domain' in df.columns else []
        
        # Simulate API response
        api_data = {domain: {'reputation': 'verified', 'risk_score': 0.1} 
                   for domain in unique_domains}
        
        # Enrich data with API results
        if 'email_domain' in df.columns:
            df['api_reputation'] = df['email_domain'].map(
                lambda x: api_data.get(x, {}).get('reputation', 'unknown')
            )
        
        return Data(value=df)