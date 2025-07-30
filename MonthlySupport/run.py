#!/usr/bin/env python3
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
import os

def send_email(report, subject, sender_email=None, sender_password=None):
    """Send email with report"""
    if not sender_email or not sender_password:
        print("EMAIL SENDING SKIPPED: No credentials provided")
        print("To send actual email, provide sender_email and sender_password")
        return {"status": "skipped", "message": "No credentials"}
    
    try:
        msg = MIMEText(report)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = "contact@langflow.org"
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return {"status": "sent", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "failed", "message": f"Failed: {str(e)}"}

def run_report(target_month="2025-05", sender_email=None, sender_password=None):
    # Load & filter data
    df = pd.read_csv("tickets.csv")
    df['open_date'] = pd.to_datetime(df['open_date'])
    df['close_date'] = pd.to_datetime(df['close_date'])
    df['resolution_days'] = (df['close_date'] - df['open_date']).dt.days
    df = df.dropna(subset=['ticket_description', 'open_date', 'close_date'])
    
    target_date = pd.to_datetime(target_month)
    df = df[(df['open_date'].dt.year == target_date.year) & 
            (df['open_date'].dt.month == target_date.month)].copy()
    
    # Transform data
    df['email_domain'] = df['email'].str.split('@').str[1].fillna('unknown')
    df['api_reputation'] = 'verified'
    
    # Control flow
    median_time = df['resolution_days'].median()
    df['priority'] = 'high' if (df['resolution_days'] > median_time).sum() >= 10 else 'normal'
    
    # Loop processing
    for idx, row in df.iterrows():
        if row['priority'] == 'high':
            df.at[idx, 'reviewed'] = True
    
    # Parallel sentiment analysis
    pos_kw = {'thank', 'great', 'excellent', 'satisfied'}
    neg_kw = {'issue', 'problem', 'dissatisfied', 'delay'}
    
    def analyze_batch(texts):
        return ['positive' if len(set(t.lower().split()) & pos_kw) > len(set(t.lower().split()) & neg_kw)
                else 'negative' if len(set(t.lower().split()) & neg_kw) > 0 else 'neutral' for t in texts]
    
    if len(df) > 100:
        batches = [df['ticket_description'].iloc[i:i+100].tolist() for i in range(0, len(df), 100)]
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(analyze_batch, batches))
        df['sentiment'] = [item for sublist in results for item in sublist]
    else:
        df['sentiment'] = analyze_batch(df['ticket_description'].tolist())
    
    # Generate report
    sentiment_counts = df['sentiment'].value_counts()
    report = f"""# Support Ticket Summary for {target_month}

**Total Tickets:** {len(df)}
**Average Response Time:** {round(df['resolution_days'].mean(), 1)} days

## Sentiment Breakdown
- Positive: {sentiment_counts.get('positive', 0)}
- Neutral: {sentiment_counts.get('neutral', 0)}
- Negative: {sentiment_counts.get('negative', 0)}"""
    
    # Send email
    subject = f"Monthly Support Ticket Report – {target_month} – SupportAnalyst"
    email_result = send_email(report, subject, sender_email, sender_password)
    
    print(f"EMAIL TO: contact@langflow.org")
    print(f"SUBJECT: {subject}")
    print(f"STATUS: {email_result['status']}")
    print(f"MESSAGE: {email_result['message']}")
    print(f"BODY:\n{report}")
    
    return {"to": "contact@langflow.org", "subject": subject, "body": report, "email_result": email_result}

if __name__ == "__main__":
    # Get credentials from environment variables or prompt
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    run_report(sender_email=sender_email, sender_password=sender_password)