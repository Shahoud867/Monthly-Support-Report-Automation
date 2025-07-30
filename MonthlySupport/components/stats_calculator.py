import pandas as pd
from langflow.custom import Component
from langflow.io import Output, Input, BoolInput
from langflow.schema import Data

class StatsCalculator(Component):
    display_name = "Advanced Stats Calculator"
    description = "Calculate comprehensive statistics with conditional metrics"
    
    inputs = [
        Input(display_name="Sentiment Data", name="sentiment_data"),
        BoolInput(name="include_advanced", display_name="Include Advanced Metrics", value=True)
    ]
    
    outputs = [
        Output(display_name="Statistics", name="statistics", method="calculate_stats")
    ]
    
    def calculate_stats(self) -> Data:
        df = self.sentiment_data.value
        sentiment_counts = df['sentiment'].value_counts()
        
        stats = {
            'total_count': len(df),
            'avg_response': round(df['resolution_days'].mean(), 1),
            'count_positive': sentiment_counts.get('positive', 0),
            'count_neutral': sentiment_counts.get('neutral', 0),
            'count_negative': sentiment_counts.get('negative', 0),
            'month_year': df['open_date'].iloc[0].strftime('%Y-%m') if len(df) > 0 else '2025-05'
        }
        
        if self.include_advanced:
            stats.update({
                'escalated_tickets': df.get('escalated', pd.Series(False)).sum(),
                'high_priority': (df.get('priority', 'normal') == 'high').sum(),
                'satisfaction_rate': round((stats['count_positive'] / stats['total_count']) * 100, 1)
            })
        
        return Data(value=stats)