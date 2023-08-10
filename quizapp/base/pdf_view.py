from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from .models import QuizScore, Quiz


def pdf(request, pk=None):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize = letter, bottomup = 0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # pdflist = ['Quiz 1', 'Quiz 1']
    # for line in pdflist:
    #     textob.textLine(line)
    if pk == 1:
        data = []
        labels = []
        queryset = QuizScore.objects.all().order_by('-score')
        for score in queryset:
            labels.append(score.quiz_id.title)
            data.append(score.score)
        print(labels)
        print(data)
        # for i in enumerate(data):
        #     data[i] = str(data[i])
        data = str(data)
        altered = labels
        altered.extend(data)
        print(altered)
        for line in altered:
            textob.textLine(line)
        # for line in (data):
        #     word = line
        #     textob.textLine(word)

    if pk == 2:
        data = []
        labels = []
        teacher_queryset = Quiz.objects.filter(teacher__is_teacher = True)
        for score in teacher_queryset:
            labels.append(score.quiz_id.title)
            data.append(score.score)
        for line in labels:
            textob.textLine(line)
        for line in data:
            textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment = True, filename = 'report.pdf')