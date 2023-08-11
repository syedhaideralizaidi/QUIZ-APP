from django.shortcuts import redirect
from django.views.generic import CreateView , UpdateView , TemplateView , DeleteView

from .models import Classroom , ClassroomStudentEnrolled


class ClassroomCreate(CreateView):
    model = Classroom
    fields = ['name', 'students']
    success_url = "/dashboard_teacher"

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        obj = form.save()
        return super().form_valid(form)

class ClassroomUpdate(UpdateView):
    model = Classroom
    fields = ['name', 'students']
    success_url = "/dashboard_teacher"

class ClassroomTemplate(TemplateView):
    model = Classroom
    template_name = 'templates/base/classroom_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classrooms = Classroom.objects.filter(teacher = self.request.user)
        class_students = ClassroomStudentEnrolled.objects.all()
        context["classrooms"] = classrooms
        context['class_students'] = class_students
        return context


class ClassroomDelete(DeleteView):
    model = Classroom
    success_url = "/classrooms"


class ClassroomStudentTemplate(TemplateView):
    model = Classroom
    template_name = 'templates/base/classroom_student_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classrooms = Classroom.objects.filter(students = self.request.user)
        class_students = ClassroomStudentEnrolled.objects.all()
        context["classrooms"] = classrooms
        context['class_students'] = class_students
        return context