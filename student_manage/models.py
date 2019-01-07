from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.


class Student(models.Model):
    """
    学生表（已报名）
    """
    customer = models.OneToOneField(verbose_name='客户信息', to='app01.Customer', on_delete=models.CASCADE, null=True,
                                    blank=True)
    class_list = models.ManyToManyField(verbose_name="已报班级", to='app01.ClassList', blank=True)

    emergency_contract = models.CharField(max_length=32, blank=True, null=True, verbose_name='紧急联系人')
    company = models.CharField(verbose_name='公司', max_length=128, blank=True, null=True)
    location = models.CharField(max_length=64, verbose_name='所在区域', blank=True, null=True)
    position = models.CharField(verbose_name='岗位', max_length=64, blank=True, null=True)
    salary = models.IntegerField(verbose_name='薪资', blank=True, null=True)
    welfare = models.CharField(verbose_name='福利', max_length=256, blank=True, null=True)
    date = models.DateField(verbose_name='入职时间', help_text='格式yyyy-mm-dd', blank=True, null=True)
    memo = models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.customer.name

    def get_class(self):
        class_list = []
        for item in self.class_list.all():
            class_list.append(str(item))
        return mark_safe('</br>'.join(class_list))


class ClassStudyRecord(models.Model):
    """
    上课记录表 （班级记录）
    """
    class_obj = models.ForeignKey(verbose_name="班级", to="app01.ClassList", on_delete=models.CASCADE)
    day_num = models.IntegerField(verbose_name="节次", help_text=u"此处填写第几节课或第几天课程...,必须为数字")

    teacher = models.ForeignKey(verbose_name="讲师", to='app01.UserInfo', limit_choices_to={"positions__in": [5, 6]},
                                on_delete=models.CASCADE)
    date = models.DateField(verbose_name="上课日期", auto_now_add=True)
    course_title = models.CharField(verbose_name='本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField(verbose_name='本节课程内容概要', blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField(verbose_name='本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField(verbose_name='作业描述', max_length=500, blank=True, null=True)
    exam = models.TextField(verbose_name='踩分点', max_length=300, blank=True, null=True)

    def __str__(self):
        return "{0} day{1}".format(self.class_obj, self.day_num)

    class Meta:
        unique_together = ['class_obj', 'day_num']


class StudentStudyRecord(models.Model):
    '''
    学生学习记录
    '''
    student = models.ForeignKey(verbose_name="学员", to='Student', on_delete=models.CASCADE)
    classstudyrecord = models.ForeignKey(verbose_name="第几天课程", to="ClassStudyRecord", on_delete=models.CASCADE)
    record_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('noshow', "缺勤"),
                      ('leave_early', "早退"),
                      )
    record = models.CharField("上课纪录", choices=record_choices, default="checked", max_length=64)
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'B-'),
                     (60, 'C+'),
                     (50, 'C'),
                     (40, 'C-'),
                     (0, ' D'),
                     (-1, 'N/A'),
                     (-100, 'COPY'),
                     (-1000, 'FAIL'),
                     )
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(verbose_name='作业评语', max_length=255, blank=True, null=True)
    note = models.CharField(verbose_name="备注", max_length=255, blank=True, null=True)

    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    stu_memo = models.TextField(verbose_name='学员备注', blank=True, null=True)
    date = models.DateTimeField(verbose_name='提交作业日期', auto_now_add=True)

    def __str__(self):
        return "{0}-{1}".format(self.classstudyrecord, self.student)

    class Meta:
        unique_together = ['student', 'classstudyrecord']
