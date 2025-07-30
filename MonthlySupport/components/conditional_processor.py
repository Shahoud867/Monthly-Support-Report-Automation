from langflow.custom import Component
from langflow.io import Output, Input, BoolInput, IntInput
from langflow.schema import Data

class ConditionalProcessor(Component):
    display_name = "Conditional Processor"
    description = "Control flow with branching logic for data processing"
    
    inputs = [
        Input(display_name="Data", name="data_input"),
        BoolInput(name="enable_priority_filter", display_name="Enable Priority Filter", value=True),
        IntInput(name="min_tickets_threshold", display_name="Min Tickets Threshold", value=10)
    ]
    
    outputs = [
        Output(display_name="Processed Data", name="processed_data", method="process_conditionally"),
        Output(display_name="Branch Info", name="branch_info", method="get_branch_info")
    ]
    
    def process_conditionally(self) -> Data:
        df = self.data_input.value.copy()
        
        # Conditional branching
        if self.enable_priority_filter:
            median_time = df['resolution_days'].median()
            high_count = (df['resolution_days'] > median_time).sum()
            df['priority'] = 'high' if high_count >= self.min_tickets_threshold else 'normal'
        else:
            df['priority'] = 'standard'
        
        # Vectorized escalation
        df['escalated'] = df['resolution_days'] > 7
        return Data(value=df)
    
    def get_branch_info(self) -> Data:
        branch_taken = "priority_enabled" if self.enable_priority_filter else "standard_processing"
        return Data(value={"branch": branch_taken, "threshold": self.min_tickets_threshold})