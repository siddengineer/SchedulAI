# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.dashboard, name='dashboard'),
#     path('timetables/', views.timetable_list, name='timetable_list'),
#     path('timetables/create/', views.create_timetable, name='create_timetable'),
#     path('timetables/<int:pk>/setup/', views.timetable_setup, name='timetable_setup'),
#     path('timetables/<int:pk>/view/', views.timetable_view, name='timetable_view'),
#     path('timetables/<int:pk>/delete/', views.delete_timetable, name='delete_timetable'),
#     path('bells/', views.bell_list, name='bell_list'),
#     path('bells/create/', views.create_bell, name='create_bell'),
#     path('bells/<int:pk>/delete/', views.delete_bell, name='delete_bell'),
# ]


# ============================================================
# timetables/urls.py  — COMPLETE FILE (replace entirely)
# ============================================================

# from django.urls import path
# from . import views
# from .views import ListView

# app_name = 'timetables'

# urlpatterns = [
#     path('',                                views.TimetableListView.as_view(),      name='list'),
#     path('new/',                            views.TimetableCreateView.as_view(),    name='create'),
#     path('<int:pk>/setup/',                 views.TimetableSetupView.as_view(),     name='setup'),
#     path('<int:pk>/bells/add/',             views.AddBellPeriodView.as_view(),      name='add-bell'),
#     path('<int:pk>/bells/<int:bell_pk>/delete/', views.DeleteBellPeriodView.as_view(), name='delete-bell'),
#     path('<int:pk>/lessons/add/',           views.AddLessonView.as_view(),          name='add-lesson'),
#     path('<int:pk>/lessons/<int:lesson_pk>/delete/', views.DeleteLessonView.as_view(), name='delete-lesson'),
#     path('<int:pk>/generate/',              views.GenerateTimetableView.as_view(),  name='generate'),
#     path('<int:pk>/status/',                views.TimetableStatusView.as_view(),    name='status'),
#     path('<int:pk>/publish/',               views.PublishTimetableView.as_view(),   name='publish'),
#     path('<int:pk>/view/',                  views.TimetableGridView.as_view(),      name='view'),
#     path('<int:pk>/live/',                  views.TimetableLiveView.as_view(),      name='live'),
#     path('<int:pk>/export/excel/',          views.ExportExcelView.as_view(),        name='export-excel'),
#     path('<int:pk>/export/pdf/',            views.ExportPDFView.as_view(),          name='export-pdf'),
#     path('<int:pk>/send-email/',            views.SendTimetableEmailView.as_view(), name='send-email'),
#     path('', views.list_view, name='timetable_list'),
# ]


# from django.urls import path
# from . import views

# app_name = 'timetables'

# urlpatterns = [
#     path('', views.TimetableListView.as_view(), name='list'),
#     path('new/', views.TimetableCreateView.as_view(), name='create'),

#     path('<int:pk>/setup/', views.TimetableSetupView.as_view(), name='setup'),

#     # ✅ ADD THIS (bell list)
#     # path('<int:pk>/bells/', views.BellListView.as_view(), name='bell_list'),

#     path('<int:pk>/bells/add/', views.AddBellPeriodView.as_view(), name='add-bell'),
#     path('<int:pk>/bells/<int:bell_pk>/delete/', views.DeleteBellPeriodView.as_view(), name='delete-bell'),

#     path('<int:pk>/lessons/add/', views.AddLessonView.as_view(), name='add-lesson'),
#     path('<int:pk>/lessons/<int:lesson_pk>/delete/', views.DeleteLessonView.as_view(), name='delete-lesson'),

#     path('<int:pk>/generate/', views.GenerateTimetableView.as_view(), name='generate'),
#     path('<int:pk>/status/', views.TimetableStatusView.as_view(), name='status'),
#     path('<int:pk>/publish/', views.PublishTimetableView.as_view(), name='publish'),

#     path('<int:pk>/view/', views.TimetableGridView.as_view(), name='view'),
#     path('<int:pk>/live/', views.TimetableLiveView.as_view(), name='live'),

#     path('<int:pk>/export/excel/', views.ExportExcelView.as_view(), name='export-excel'),
#     path('<int:pk>/export/pdf/', views.ExportPDFView.as_view(), name='export-pdf'),

#     path('<int:pk>/send-email/', views.SendTimetableEmailView.as_view(), name='send-email'),
# ]




from django.urls import path
from . import views

app_name = 'timetables'

urlpatterns = [
    path('', views.TimetableListView.as_view(), name='list'),
    path('new/', views.TimetableCreateView.as_view(), name='create'),
    path('<int:pk>/setup/', views.TimetableSetupView.as_view(), name='setup'),

    # Bell Schedules — separate pages
    path('bells/', views.BellScheduleListView.as_view(), name='bells'),
    path('bells/new/', views.BellScheduleCreateView.as_view(), name='bell-create'),
    path('bells/<int:pk>/', views.BellScheduleDetailView.as_view(), name='bell-detail'),
    path('bells/<int:pk>/add-period/', views.AddPeriodView.as_view(), name='add-period'),
    path('bells/<int:pk>/periods/<int:period_pk>/delete/', views.DeletePeriodView.as_view(), name='delete-period'),
    path('bells/<int:pk>/delete/', views.DeleteBellScheduleView.as_view(), name='bell-delete'),

    # Lessons
    path('<int:pk>/lessons/add/', views.AddLessonView.as_view(), name='add-lesson'),
    path('<int:pk>/lessons/<int:lesson_pk>/delete/', views.DeleteLessonView.as_view(), name='delete-lesson'),

    path('<int:pk>/generate/', views.GenerateTimetableView.as_view(), name='generate'),
    path('<int:pk>/status/', views.TimetableStatusView.as_view(), name='status'),
    path('<int:pk>/publish/', views.PublishTimetableView.as_view(), name='publish'),
    path('<int:pk>/view/', views.TimetableGridView.as_view(), name='view'),
    path('<int:pk>/live/', views.TimetableLiveView.as_view(), name='live'),
    path('<int:pk>/export/excel/', views.ExportExcelView.as_view(), name='export-excel'),
    path('<int:pk>/export/pdf/', views.ExportPdfView.as_view(), name='export-pdf'),
    path('<int:pk>/send-email/', views.SendEmailView.as_view(), name='send-email'),
]