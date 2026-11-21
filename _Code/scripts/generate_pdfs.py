#!/usr/bin/env python3
"""
Generate professional PDF documents from Markdown files using ReportLab.
Produces:
- Storyboard.pdf
- Narration_Script.pdf
- Code_Walkthrough.pdf
- Viva_Prep.pdf
"""
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def md_to_flowables(md_text, styles):
    flowables = []
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_data = []

    while i < len(lines):
        line = lines[i].rstrip()
        
        # Table detection
        if '|' in line and not line.startswith('```'):
            # Table row
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if cols and not all(c.startswith('---') or c.startswith(':--') or c == '' for c in cols):
                table_data.append(cols)
            elif cols and all(c.startswith('---') or c.startswith(':--') for c in cols):
                # Separator line, ignore
                pass
            i += 1
            # Check next line
            if i >= len(lines) or '|' not in lines[i]:
                # End of table
                if table_data:
                    # Render table
                    t_cells = []
                    for row_idx, r in enumerate(table_data):
                        row_cells = []
                        for cell in r:
                            # Parse bold in cell
                            c_text = cell.replace('**', '<b>', 1).replace('**', '</b>', 1)
                            st = styles['Normal'] if row_idx > 0 else styles['TableHead']
                            row_cells.append(Paragraph(c_text, st))
                        t_cells.append(row_cells)
                    col_widths = [160, 320] if len(t_cells[0]) == 2 else None
                    tbl = Table(t_cells, colWidths=col_widths)
                    tbl.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f9f9f9'), colors.white]),
                    ]))
                    flowables.append(tbl)
                    flowables.append(Spacer(1, 10))
                    table_data = []
            continue

        # Headers
        if line.startswith('# '):
            text = line[2:].strip()
            flowables.append(Paragraph(text, styles['DocTitle']))
            flowables.append(Spacer(1, 10))
        elif line.startswith('## '):
            text = line[3:].strip()
            flowables.append(Paragraph(text, styles['SectionHeader']))
            flowables.append(Spacer(1, 8))
        elif line.startswith('### '):
            text = line[4:].strip()
            flowables.append(Paragraph(text, styles['SubSectionHeader']))
            flowables.append(Spacer(1, 6))
        elif line.startswith('> '):
            text = line[2:].strip()
            flowables.append(Paragraph(f"<i>{text}</i>", styles['BlockQuote']))
            flowables.append(Spacer(1, 8))
        elif line.startswith('---'):
            flowables.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc'), spaceBefore=8, spaceAfter=8))
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            # formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
            flowables.append(Paragraph(f"• {text}", styles['BulletItem']))
            flowables.append(Spacer(1, 3))
        elif re.match(r'^\d+\.\s+', line):
            text = re.sub(r'^\d+\.\s+', '', line).strip()
            prefix = line.split('.')[0] + '.'
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
            flowables.append(Paragraph(f"<b>{prefix}</b> {text}", styles['BulletItem']))
            flowables.append(Spacer(1, 4))
        elif line.startswith('```'):
            # Code block
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
                i += 1
            code_text = "<br/>".join(code_lines)
            flowables.append(Paragraph(f"<font face='Courier' size=8>{code_text}</font>", styles['CodeBlock']))
            flowables.append(Spacer(1, 8))
        elif line.strip() == '':
            flowables.append(Spacer(1, 4))
        else:
            text = line.strip()
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
            flowables.append(Paragraph(text, styles['NormalText']))
            flowables.append(Spacer(1, 4))
            
        i += 1

    return flowables

def build_pdf(md_filename, pdf_filename):
    md_path = os.path.join(PROJECT_DIR, md_filename)
    pdf_path = os.path.join(PROJECT_DIR, pdf_filename)
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found")
        return False

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('DocTitle', parent=styles['Normal'], fontSize=20, leading=24, textColor=colors.HexColor('#1a1a2e'), fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle('SectionHeader', parent=styles['Normal'], fontSize=14, leading=18, textColor=colors.HexColor('#0055aa'), fontName='Helvetica-Bold', spaceBefore=10))
    styles.add(ParagraphStyle('SubSectionHeader', parent=styles['Normal'], fontSize=11, leading=15, textColor=colors.HexColor('#222222'), fontName='Helvetica-Bold', spaceBefore=6))
    styles.add(ParagraphStyle('NormalText', parent=styles['Normal'], fontSize=9.5, leading=13.5, textColor=colors.HexColor('#222222'), fontName='Helvetica'))
    styles.add(ParagraphStyle('BulletItem', parent=styles['Normal'], fontSize=9.5, leading=13.5, textColor=colors.HexColor('#222222'), fontName='Helvetica', leftIndent=12))
    styles.add(ParagraphStyle('BlockQuote', parent=styles['Normal'], fontSize=9.5, leading=13.5, textColor=colors.HexColor('#333333'), fontName='Helvetica-Oblique', leftIndent=15, rightIndent=15))
    styles.add(ParagraphStyle('CodeBlock', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.HexColor('#222222'), backColor=colors.HexColor('#f0f0f5'), borderPadding=6))
    styles.add(ParagraphStyle('TableHead', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=colors.white, fontName='Helvetica-Bold'))

    flowables = md_to_flowables(md_text, styles)
    doc.build(flowables)
    print(f"✓ Generated {pdf_filename} ({os.path.getsize(pdf_path)} bytes)")
    return True

if __name__ == '__main__':
    targets = [
        ('Storyboard.md', 'Storyboard.pdf'),
        ('Narration_Script.md', 'Narration_Script.pdf'),
        ('Code_Walkthrough.md', 'Code_Walkthrough.pdf'),
        ('Viva_Prep.md', 'Viva_Prep.pdf'),
    ]
    for md_fn, pdf_fn in targets:
        build_pdf(md_fn, pdf_fn)
