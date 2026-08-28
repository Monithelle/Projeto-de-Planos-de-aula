import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from app.models.lesson_plan import LessonPlan

def generate_lesson_plan_pdf(plan: LessonPlan) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor('#006b57')
    secondary_color = colors.HexColor('#164235')
    text_color = colors.HexColor('#1c2521')
    light_bg = colors.HexColor('#f6f7f4')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=1,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#61706a'),
        alignment=1,
        spaceAfter=15
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4
    )

    label_style = ParagraphStyle(
        'Label',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#333333')
    )

    value_style = ParagraphStyle(
        'Value',
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=text_color
    )

    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color
    )

    # 1. Cabeçalho
    elements.append(Paragraph("PLANO DE AULA", title_style))
    elements.append(Paragraph("Alinhado ao Guia do Currículo Priorizado", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=0, spaceAfter=12))

    # 2. Informações Gerais em Tabela
    prof_name = plan.user.name if plan.user else 'Não informado'
    subj_name = plan.subject.name if plan.subject else 'Não informado'
    ensino_txt = 'Ensino Médio' if plan.education_level == 'medio' else 'Ensino Fundamental'
    turmas_txt = plan.classes_formatted or 'Não informada'
    periodo_txt = plan.period_formatted or 'Não informado'

    data_grid = [
        [
            Paragraph("<b>Professor(a):</b>", label_style), Paragraph(prof_name, value_style),
            Paragraph("<b>Período:</b>", label_style), Paragraph(periodo_txt, value_style)
        ],
        [
            Paragraph("<b>Componente:</b>", label_style), Paragraph(subj_name, value_style),
            Paragraph("<b>Bimestre:</b>", label_style), Paragraph(f"{plan.bimester}º Bimestre", value_style)
        ],
        [
            Paragraph("<b>Ensino / Série:</b>", label_style), Paragraph(f"{ensino_txt} - {plan.grade}", value_style),
            Paragraph("<b>Turma(s):</b>", label_style), Paragraph(turmas_txt, value_style)
        ],
        [
            Paragraph("<b>Nº de Aulas:</b>", label_style), Paragraph(f"{plan.number_of_lessons} aulas", value_style),
            Paragraph("<b>Data de Registro:</b>", label_style), Paragraph(plan.created_at.strftime('%d/%m/%Y'), value_style)
        ]
    ]

    t = Table(data_grid, colWidths=[90, 170, 85, 175])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#d9e1dd')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5eae7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 14))

    # 3. Blocos de Conteúdo do Plano
    def format_block(title, content):
        if not content:
            return
        elements.append(Paragraph(title, section_header_style))
        formatted_content = content.replace('\n', '<br/>')
        
        block_table = Table([[Paragraph(formatted_content, body_style)]], colWidths=[520])
        block_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafbfa')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#d9e1dd')),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 9),
            ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ]))
        elements.append(block_table)
        elements.append(Spacer(1, 10))

    format_block("1. TÍTULO DAS AULAS", plan.selected_lesson_titles)
    format_block("2. OBJETIVOS DE APRENDIZAGEM", plan.objectives)
    format_block("3. CONTEÚDOS", plan.contents)
    format_block("4. HABILIDADES", plan.skills)
    format_block("5. APRENDIZAGENS ESSENCIAIS (AEs)", plan.essential_learnings)
    format_block("6. RECURSOS DIDÁTICOS", plan.resources)
    format_block("7. METODOLOGIA / DESENVOLVIMENTO DAS AULAS", plan.methodology)
    format_block("8. INSTRUMENTOS DE AVALIAÇÃO", plan.evaluation)

    # 4. Assinatura do Professor no rodapé
    elements.append(Spacer(1, 20))
    signature_data = [
        [
            Paragraph("____________________________________________________<br/>Assinatura do(a) Professor(a)", ParagraphStyle('Sig', parent=styles['Normal'], alignment=1, fontSize=9, leading=14)),
            Paragraph("____________________________________________________<br/>Coordenação Pedagógica", ParagraphStyle('SigCoord', parent=styles['Normal'], alignment=1, fontSize=9, leading=14))
        ]
    ]
    sig_table = Table(signature_data, colWidths=[260, 260])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elements.append(KeepTogether([sig_table]))

    doc.build(elements)
    buffer.seek(0)
    return buffer

