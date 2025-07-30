import pandas as pd
from langflow.custom import Component
from langflow.io import Output, Input, BoolInput
from langflow.schema import Data
from concurrent.futures import ThreadPoolExecutor

class SentimentAnalyzer(Component):
    display_name = "Sentiment Analyzer"
    description = "Parallel sentiment analysis with performance optimization"
    
    inputs = [
        Input(display_name="Tickets", name="tickets_input"),
        BoolInput(name="enable_parallel", display_name="Enable Parallel Processing", value=True)
    ]
    
    outputs = [
        Output(display_name="Analyzed Data", name="analyzed_data", method="analyze_sentiment")
    ]
    
    def analyze_sentiment(self) -> Data:
        df = self.tickets_input.value.copy()
        
        # Optimized keyword sets for minimal token usage
        pos_kw = {'thank', 'great', 'excellent', 'perfect', 'satisfied', 'quick'}
        neg_kw = {'issue', 'problem', 'confusing', 'dissatisfied', 'delay', 'persists'}
        
        def classify_batch(texts):
            results = []
            for text in texts:
                text_set = set(text.lower().split())
                pos_score = len(text_set & pos_kw)
                neg_score = len(text_set & neg_kw)
                
                if pos_score > neg_score:
                    results.append('positive')
                elif neg_score > pos_score:
                    results.append('negative')
                else:
                    results.append('neutral')
            return results
        
        # Parallel processing for performance
        if self.enable_parallel and len(df) > 100:
            batch_size = len(df) // 4
            batches = [df['ticket_description'].iloc[i:i+batch_size].tolist() 
                      for i in range(0, len(df), batch_size)]
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(classify_batch, batches))
            
            df['sentiment'] = [item for sublist in results for item in sublist]
        else:
            df['sentiment'] = classify_batch(df['ticket_description'].tolist())
        
        return Data(value=df)