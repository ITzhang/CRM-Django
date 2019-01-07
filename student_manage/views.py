from django.shortcuts import render, redirect, reverse, HttpResponse
from student_manage.models import Student, ClassStudyRecord, StudentStudyRecord
from app01.utils.pages import Pagination
from django.views import View
from student_manage.utils.forms_check import StudentModelForm, ClassStudyRecordModelForm, StudentStudyRecordMF, \
    CreateGradeMF
import copy


# Create your views here.


def show_student(request):
    all_student = Student.objects.all()
    current_page_num = request.GET.get('page', 1)
    pagination = Pagination(request, current_page_num, all_student)
    page_html, all_student, counter = pagination.page_html()
    return render(request, 'student.html',
                  {'page_html': page_html,
                   'all_student': all_student,
                   'counter': counter,
                   })


class AddEditStudentView(View):
    """学生编辑，添加"""

    def get(self, request, sid=None):
        student_obj = Student.objects.filter(pk=sid).first()
        forms = StudentModelForm(instance=student_obj)
        return render(request, 'add_edit_consult_record.html', {'forms': forms, 'student_obj': student_obj})

    def post(self, request, sid=None):
        student_obj = Student.objects.filter(pk=sid).first()
        forms = StudentModelForm(instance=student_obj, data=request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(request.GET.get('next', 'student'))
        else:
            return render(request, 'add_edit_consult_record.html', {'forms': forms, 'student_obj': student_obj})


def del_student(request, sid):
    """
    删除学生
    :param request:
    :param sid:
    :return:
    """
    Student.objects.filter(pk=sid).delete()
    return redirect('student')


class ClassStudyRecordView(View):
    def get(self, request):
        all_csr = ClassStudyRecord.objects.all()
        current_page_num = request.GET.get('page', 1)
        pagination = Pagination(request, current_page_num, all_csr)
        page_html, all_csr, counter = pagination.page_html()
        return render(request, 'class_study_record.html',
                      {'page_html': page_html,
                       'all_csr': all_csr,
                       'counter': counter,
                       })

    def post(self, request):
        select_method = request.POST.get('select_method')
        if hasattr(self, select_method):
            func = getattr(self, select_method)
            func(request)
            return redirect('class_study_record')

        else:
            return HttpResponse('非法的操作')

    def batch_create(self, request):
        csr_list = request.POST.getlist('checked_csr')
        for csr in csr_list:
            kclass = ClassStudyRecord.objects.filter(pk=csr).values('class_obj__student')
            for item in kclass:
                try:
                    StudentStudyRecord.objects.create(student_id=item['class_obj__student'],
                                                      classstudyrecord_id=csr)
                except Exception:
                    pass


class AddEditCsrView(View):
    """班级学习进度编辑，添加"""

    def get(self, request, cid=None):
        csr_obj = ClassStudyRecord.objects.filter(pk=cid).first()
        forms = ClassStudyRecordModelForm(instance=csr_obj)
        return render(request, 'add_edit_consult_record.html', {'forms': forms, 'csr_obj': csr_obj})

    def post(self, request, cid=None):
        csr_obj = ClassStudyRecord.objects.filter(pk=cid).first()
        forms = ClassStudyRecordModelForm(instance=csr_obj, data=request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(request.GET.get('next', 'class_study_record'))
        else:
            return render(request, 'add_edit_consult_record.html', {'forms': forms, 'csr_obj': csr_obj})


def del_csr(request, sid):
    ClassStudyRecord.objects.filter(pk=sid).delete()
    return redirect('class_study_record')


class StudentStudyRecordView(View):
    """查看学生学习进度"""

    def get(self, request):
        all_ssr = StudentStudyRecord.objects.all()
        current_page_num = request.GET.get('page', 1)
        pagination = Pagination(request, current_page_num, all_ssr)
        page_html, all_ssr, counter = pagination.page_html()
        return render(request, 'student_study_record.html',
                      {'page_html': page_html,
                       'all_ssr': all_ssr,
                       'counter': counter,
                       })


class AddEditSsrView(View):
    """学生学习进度编辑，添加"""

    def get(self, request, cid=None):
        ssr_obj = StudentStudyRecord.objects.filter(pk=cid).first()
        forms = StudentStudyRecordMF(instance=ssr_obj)
        return render(request, 'add_edit_consult_record.html', {'forms': forms, 'ssr_obj': ssr_obj})

    def post(self, request, cid=None):
        ssr_obj = StudentStudyRecord.objects.filter(pk=cid).first()
        forms = StudentStudyRecordMF(instance=ssr_obj, data=request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(request.GET.get('next', 'student_study_record'))
        else:
            return render(request, 'add_edit_consult_record.html', {'forms': forms, 'ssr_obj': ssr_obj})


def del_ssr(request, sid):
    """
    删除学生学习记录
    :param request:
    :param sid:
    :return:
    """
    StudentStudyRecord.objects.filter(pk=sid).delete()
    return redirect('student_study_record')


class CreateGradeView(View):
    def get(self, request, cid):
        ssr_obj = StudentStudyRecord.objects.filter(classstudyrecord_id=cid)
        ssr_obj = copy.deepcopy(ssr_obj)
        title = ClassStudyRecord.objects.filter(pk=cid).first()
        for item in ssr_obj:
            item.forms = CreateGradeMF(instance=item)
        current_page_num = request.GET.get('page', 1)
        pagination = Pagination(request, current_page_num, ssr_obj)
        page_html, ssr_obj, counter = pagination.page_html()

        return render(request, 'create_grade.html',
                      {'page_html': page_html,
                       'ssr_obj': ssr_obj,
                       'counter': counter,
                       'title': title,
                       })

    def post(self, request, cid):
        data_list = zip(request.POST.getlist('checked_csr'), request.POST.getlist('score'),
                        request.POST.getlist('homework_note'))
        for data in data_list:
            obj = StudentStudyRecord.objects.filter(pk=data[0]).first()
            finally_data = {'score': data[1],
                            'homework_note': data[2]}
            forms = CreateGradeMF(instance=obj, data=finally_data)
            if forms.is_valid():
                forms.save()
            else:
                return HttpResponse('数据不合法')
        return redirect(request.GET.get('next', 'class_study_record'))
