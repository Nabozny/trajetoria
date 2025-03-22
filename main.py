from datetime import datetime
from dotenv import load_dotenv

import os

from scripts.generate_pdf import generate_pdf_report
from scripts.logs import setup_logger, log_error
from scripts.search_ceps import process_ceps
from scripts.send_mail import send_email


logger = setup_logger()
load_dotenv()

dt_ref = datetime.now().strftime('%d/%m/%Y') 
sender_email = os.getenv('EMAIL_ACCOUNT')
password = os.getenv('EMAIL_PASSWORD')
smtp_port = int(os.getenv('SMTP_PORT'))
smtp_server = os.getenv('SMTP_SERVER')

with open('templates/search_cep_body.html', 'r', encoding='utf-8') as f:
    template_html = f.read()

results, failed_ceps = process_ceps('ceps_lista_30.csv')

failed_ceps_html = """
<div class="failed-list">
    <h3>Alguns CEPs não puderam ser processados:</h3>
    <ul>
        {}
    </ul>
    <p>Por favor, verifique se os CEPs acima estão corretos.</p>
</div>
""".format('\n'.join(f'<li>{cep}</li>' for cep in failed_ceps)) if failed_ceps else ''

recipients = [
    {'name': 'Christopher', 'email': 'christopher.gpereira06@gmail.com', 'sent_time': None},
    {'name': 'Teste Trajetoria', 'email': 'testecepstrajetoria@gmail.com', 'sent_time': None}
]

for recipient in recipients:
    email_body = template_html.format(
        greeting='Bom Dia!' if datetime.now().hour < 12 else 'Boa Tarde!',
        recipient=recipient['name'],
        success_count=len(results),
        failed_count=len(failed_ceps),
        failed_ceps_section=failed_ceps_html
    )

    try:
        success = send_email(
            body=email_body,
            subject='Resultados da Consulta de CEPs',
            results=results,
            recipients=recipient['email'],
            sender_email=sender_email,
            password=password,
            smtp_port=smtp_port,
            smtp_server=smtp_server
        )
        if success:
            recipient['sent_time'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    except Exception as e:
        log_error(f"Recipient: {recipient['name']} - Error: {str(e)}")

pdf_filename = generate_pdf_report(results, failed_ceps, email_recipients = recipients)
logger.info(f"PDF report generated: {pdf_filename}")
