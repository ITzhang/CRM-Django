from django.urls import path, re_path
from student_manage import views

urlpatterns = [

    # 学生成员管理
    path('student/', views.show_student, name='student'),
    path('student/add/', views.AddEditStudentView.as_view(), name='student_add'),
    re_path(r'^student/edit/(\d+)/$', views.AddEditStudentView.as_view(), name='student_edit'),
    re_path(r'^student/del/(\d+)/$', views.del_student, name='student_del'),

    # 班级学习情况管理
    path('class_study_record/', views.ClassStudyRecordView.as_view(), name='class_study_record'),
    path('class_study_record/add/', views.AddEditCsrView.as_view(), name='class_study_record_add'),
    re_path(r'^class_study_record/edit/(\d+)/$', views.AddEditCsrView.as_view(), name='class_study_record_edit'),
    re_path(r'^class_study_record/del/(\d+)/$', views.del_csr, name='class_study_record_del'),

    # 学生学习情况管理
    path('student_study_record/', views.StudentStudyRecordView.as_view(), name='student_study_record'),
    path('student_study_record/add/', views.AddEditSsrView.as_view(), name='student_study_record_add'),
    re_path(r'^student_study_record/edit/(\d+)/$', views.AddEditSsrView.as_view(), name='student_study_record_edit'),
    re_path(r'^student_study_record/del/(\d+)/$', views.del_ssr, name='student_study_record_del'),

    # 录入成绩
    re_path(r'^create_grade/show/(\d+)/$', views.CreateGradeView.as_view(), name='create_grade_show'),
    re_path(r'^create_grade/submit/(\d+)/$', views.CreateGradeView.as_view(), name='create_grade_submit'),

]
