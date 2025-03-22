from datetime import datetime
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os
import pandas as pd


def generate_pdf_report(results, failed_ceps, email_recipients):
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{output_dir}/relatorio_ceps_{timestamp}.pdf"
    
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    width, height = letter

    can.saveState()
    can.setFillAlpha(0.1)
    can.drawImage(
        "imgs/Logo-Azul-trajetoria.png",
        x=120,
        y=320,
        width=width / 2,
        height=height / 4,
        preserveAspectRatio=True,
        anchor='c',
        mask='auto'
    )
    can.restoreState()

    can.saveState()
    can.setFont('Helvetica', 9)
    can.drawString(50, 30, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    can.drawString(width - 80, 30, f"Página {can.getPageNumber()}")
    can.restoreState()
    
    can.setFont("Helvetica-Bold", 16)
    can.drawCentredString(width/2, height - 50, "Relatório de Consulta de CEPs")
    
    y_position = height - 90
    can.setFont("Helvetica", 12)
    intro_text = "Este relatório apresenta os resultados obtidos através de consultas automatizadas de CEPs. "
    intro_text += "O processo realizou buscas nas bases de dados dos Correios e gerou um relatório detalhado "
    intro_text += "com os endereços encontrados. Os resultados foram enviados por e-mail para os destinatários abaixo."
    
    words = intro_text.split()
    line = []
    for word in words:
        line.append(word)
        if len(' '.join(line)) > 99:
            can.drawString(50, y_position, ' '.join(line[:-1]))
            y_position -= 20
            line = [line[-1]]
    if line:
        can.drawString(50, y_position, ' '.join(line))
    
    y_position -= 20
    can.setFont("Helvetica", 11)
    if email_recipients:
        for rec in email_recipients:
            email_info = f"• {rec['name']} - {rec['email']}"
            if rec.get('sent_time'):
                email_info += f" (Enviado em: {rec['sent_time']})"
            can.drawString(60, y_position, email_info)
            y_position -= 12
            if y_position < 50:
                can.showPage()
                y_position = height - 50
                can.saveState()
                can.setFont('Helvetica', 9)
                can.drawString(50, 30, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                can.drawString(width - 80, 30, f"Página {can.getPageNumber()}")
                can.restoreState()
    else:
        can.drawString(50, y_position, "Nenhum email enviado.")
        y_position -= 15

    y_position -= 15
    can.setFont("Helvetica", 11)
    can.drawString(50, y_position, "Durante as buscas, alguns dados de endereços foram encontrados, sendo eles:")
    
    results_df = pd.DataFrame(results)
    found_count = len(results_df)
    can.setFont("Helvetica-Bold", 12)
    y_position -= 20
    
    if not results_df.empty:
        headers = list(results_df.columns)
        n_cols = len(headers)
        margin = 50
        available_width = width - margin * 2
        step = available_width / n_cols
        x_positions = [margin + i * step for i in range(n_cols)]
        
        can.setFont("Helvetica-Bold", 10)
        for i, header in enumerate(headers):
            can.drawString(x_positions[i], y_position, str(header))
        y_position -= 15
        
        can.setFont("Helvetica", 8)
        for _, row in results_df.iterrows():
            for i, header in enumerate(headers):
                can.drawString(x_positions[i], y_position, str(row[header]))
            y_position -= 10
            if y_position < 50:
                can.showPage()
                y_position = height - 50
                can.saveState()
                can.setFont('Helvetica', 9)
                can.drawString(50, 30, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                can.drawString(width - 80, 30, f"Página {can.getPageNumber()}")
                can.restoreState()
    else:
        can.setFont("Helvetica", 10)
        can.drawString(50, y_position, "Nenhum CEP encontrado.")
        y_position -= 15

    y_position -= 20
    can.setFont("Helvetica", 11)
    failed_intro = "Para os CEPs listados abaixo, será necessária uma análise adicional. "
    failed_intro += "Devido às particularidades de alguns CEPs, "
    failed_intro += "recomenda-se uma verificação manual no site dos Correios."
    
    words = failed_intro.split()
    line = []
    for word in words:
        line.append(word)
        if len(' '.join(line)) > 99:
            can.drawString(50, y_position, ' '.join(line[:-1]))
            y_position -= 20
            line = [line[-1]]
    if line:
        can.drawString(50, y_position, ' '.join(line))
    
    y_position -= 20

    can.setFont("Helvetica-Bold", 12)
    can.setFont("Helvetica", 10)
    if failed_ceps:
        for cep in failed_ceps:
            can.drawString(60, y_position, f"• {cep}")
            y_position -= 12
            if y_position < 50:
                can.showPage()
                y_position = height - 50
                can.saveState()
                can.setFont('Helvetica', 9)
                can.drawString(50, 30, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                can.drawString(width - 80, 30, f"Página {can.getPageNumber()}")
                can.restoreState()
    else:
        can.drawString(50, y_position, "Todos os CEPs foram processados.")
    
    can.save()
    packet.seek(0)
    
    overlay_pdf = PdfReader(packet)
    writer = PdfWriter()
    for page in overlay_pdf.pages:
        writer.add_page(page)
    
    with open(filename, "wb") as f_out:
        writer.write(f_out)
    
    return filename
