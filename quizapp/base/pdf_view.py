from django.http import FileResponse
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from base.models import QuizScore, Quiz

def pdf_report_generator(request, pk=None):
    """This is function generates the report when user clicks the generate button in statistics.
    It basically displays the table which contains the data which is displayed on the PieChart summarization."""
    buf = io.BytesIO()

    doc = SimpleDocTemplate(buf, pagesize=letter)
    story = []

    if pk == 1:
        data = []
        labels = []
        queryset = QuizScore.objects.all().order_by('-score')
        for score in queryset:
            labels.append(score.quiz_id.title)
            data.append(str(score.score))

        # Create a table with labels and data
        data.insert(0, "Score")  # Header
        data = [labels] + [data]
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)

    if pk == 2:
        data = []
        labels = []
        teacher_queryset = Quiz.objects.filter(teacher__is_teacher=True)
        for score in teacher_queryset:
            labels.append(score.title)
            data.append(str(score.time_limit))

        # Create a table with labels and data
        data.insert(0, "Score")  # Header
        data = [labels] + [data]
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)

    doc.build(story)
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='report.pdf')
