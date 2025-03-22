from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import smtplib

def send_email(body, subject, results, recipients, sender_email, password, smtp_port, smtp_server):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipients
        msg['Subject'] = subject
        
        text_part = MIMEText(body.replace('<br>', '\n').replace('</p>', '\n').replace('<p>', ''), 'plain', 'utf-8')
        html_part = MIMEText(body, 'html', 'utf-8')
        
        msg.attach(text_part)
        msg.attach(html_part)

        if not isinstance(results, pd.DataFrame):
            results = pd.DataFrame(results if isinstance(results, list) else [results])

        if not results.empty:
            csv_data = results.to_csv(index=False)
            attachment = MIMEApplication(csv_data.encode('utf-8'))
            attachment.add_header('Content-Disposition', 'attachment', filename='resultados_ceps.csv')
            msg.attach(attachment)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, recipients, text)
            server.quit()
            
        return True
    except Exception as e:
        return False
