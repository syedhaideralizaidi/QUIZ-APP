from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView

from base.models import Classroom, ClassroomStudentEnrolled


class ClassroomCreate(CreateView):
    '''This class creates a classroom for a group of students'''

    model = Classroom
    fields = ['name', 'students']
    success_url = "/dashboard_teacher"
    template_name = 'templates/base/teachers/classroom/classroom_form.html'

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        form.save()
        return super().form_valid(form)

class ClassroomUpdate(UpdateView):
    '''This class can update a classroom for a teacher'''

    model = Classroom
    fields = ['name', 'students']
    success_url = "/dashboard_teacher"
    template_name = 'templates/base/teachers/classroom/classroom_form.html'

class ClassroomTemplate(TemplateView):
    '''Teacher can view all the classes created by him/her through this class'''

    model = Classroom
    template_name = 'templates/base/teachers/classroom/classroom_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classrooms = Classroom.objects.filter(teacher = self.request.user)
        class_students = ClassroomStudentEnrolled.objects.all()
        context["classrooms"] = classrooms
        context['class_students'] = class_students
        return context


class ClassroomDelete(DeleteView):
    '''This class deletes a classroom'''

    model = Classroom
    template_name = 'templates/base/teachers/classroom/classroom_confirm_delete.html'
    success_url = "/classrooms"

class ClassroomStudentTemplate(TemplateView):
    '''Student can view all the classes created by their teachers through this class'''

    model = Classroom
    template_name = 'templates/base/students/classroom_student_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classrooms = Classroom.objects.filter(students = self.request.user)
        class_students = ClassroomStudentEnrolled.objects.all()
        context["classrooms"] = classrooms
        context['class_students'] = class_students
        return context