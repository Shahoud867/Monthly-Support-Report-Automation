from langflow.custom import Component
from langflow.io import Output, Input, IntInput
from langflow.schema import Data

class LoopProcessor(Component):
    display_name = "Loop Processor"
    description = "Iterative processing with loop logic"
    
    inputs = [
        Input(display_name="Data", name="data_input"),
        IntInput(name="max_iterations", display_name="Max Iterations", value=3)
    ]
    
    outputs = [
        Output(display_name="Loop Result", name="loop_result", method="process_loop")
    ]
    
    def process_loop(self) -> Data:
        df = self.data_input.value.copy()
        
        # Loop processing for iterative improvements
        for iteration in range(self.max_iterations):
            # Process each ticket in loop
            for idx, row in df.iterrows():
                if row.get('priority') == 'high' and not row.get('reviewed', False):
                    df.at[idx, 'reviewed'] = True
                    df.at[idx, 'review_iteration'] = iteration + 1
        
        return Data(value=df)