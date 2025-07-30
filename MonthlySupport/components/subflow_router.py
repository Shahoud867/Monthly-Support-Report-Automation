import pandas as pd
from langflow.custom import Component
from langflow.io import Output, Input, BoolInput
from langflow.schema import Data

class SubflowRouter(Component):
    display_name = "Subflow Router"
    description = "Route data through different processing paths"
    
    inputs = [
        Input(display_name="Data", name="data_input"),
        BoolInput(name="use_advanced_path", display_name="Use Advanced Path", value=True)
    ]
    
    outputs = [
        Output(display_name="Routed Data", name="routed_data", method="route_data"),
        Output(display_name="Path Info", name="path_info", method="get_path_info")
    ]
    
    def route_data(self) -> Data:
        df = self.data_input.value.copy()
        
        # Subflow routing logic
        if self.use_advanced_path:
            # Advanced processing path
            df['processing_path'] = 'advanced'
            df['enhanced_features'] = True
        else:
            # Standard processing path
            df['processing_path'] = 'standard'
            df['enhanced_features'] = False
        
        return Data(value=df)
    
    def get_path_info(self) -> Data:
        path_taken = "advanced" if self.use_advanced_path else "standard"
        return Data(value={"path": path_taken, "timestamp": pd.Timestamp.now()})