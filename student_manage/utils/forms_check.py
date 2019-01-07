from django import forms
from student_manage.models import Student, ClassStudyRecord, StudentStudyRecord


class StudentModelForm(forms.ModelForm):
    """
    学生成员modelform
    """

    class Meta:
        model = Student
        fields = '__all__'


class ClassStudyRecordModelForm(forms.ModelForm):
    """
    班级进度
    """

    class Meta:
        model = ClassStudyRecord
        fields = '__all__'


class StudentStudyRecordMF(forms.ModelForm):
    class Meta:
        model = StudentStudyRecord
        fields = '__all__'


class CreateGradeMF(forms.ModelForm):
    class Meta:
        model = StudentStudyRecord
        fields = ['score', 'homework_note']
