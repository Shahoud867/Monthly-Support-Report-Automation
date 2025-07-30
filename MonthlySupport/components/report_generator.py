from langflow.custom import Component
from langflow.io import Output, Input
from langflow.schema import Data

class ReportGenerator(Component):
    display_name = "Report Generator"
    description = "Generate formatted report output"
    
    inputs = [
        Input(display_name="Stats", name="stats_input")
    ]
    
    outputs = [
        Output(display_name="Report Content", name="report_content", method="generate_report")
    ]
    
    def generate_report(self) -> Data:
        stats = self.stats_input.value
        
        report = f"""# Support Ticket Summary for {stats['month_year']}

**Total Tickets:** {stats['total_count']}
**Average Response Time:** {stats['avg_response']} days

## Sentiment Breakdown
- Positive: {stats['count_positive']}
- Neutral: {stats['count_neutral']}
- Negative: {stats['count_negative']}"""
        
        return Data(value=report)