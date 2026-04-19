from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from timetables.models import Timetable, TimetableSlot, DAYS
from faculty.models import Faculty, FacultyLeave
from resources.models import Subject, Grade
from collections import defaultdict

@login_required
def reports_home(request):
    user = request.user
    timetables = Timetable.objects.filter(owner=user)
    tt_id = request.GET.get('timetable')
    tt = None
    faculty_workload = []
    subject_dist = []
    day_dist = []

    if tt_id:
        tt = get_object_or_404(Timetable, pk=tt_id, owner=user)
        slots = tt.slots.select_related('lesson__faculty', 'lesson__subject').all()

        # Faculty workload
        fac_count = defaultdict(int)
        for slot in slots:
            if slot.lesson.faculty:
                fac_count[slot.lesson.faculty.name] += 1
        faculty_workload = sorted(fac_count.items(), key=lambda x: -x[1])

        # Subject distribution
        sub_count = defaultdict(int)
        for slot in slots:
            sub_count[slot.lesson.subject.name] += 1
        subject_dist = sorted(sub_count.items(), key=lambda x: -x[1])

        # Day distribution
        day_count = defaultdict(int)
        for slot in slots:
            day_count[slot.day] += 1
        day_dist = [(d, day_count.get(d, 0)) for d in DAYS]

    ctx = {
        'timetables': timetables,
        'selected_tt': tt,
        'faculty_workload': faculty_workload,
        'subject_dist': subject_dist,
        'day_dist': day_dist,
        'is_pro': user.is_pro(),
        'total_faculty': Faculty.objects.filter(owner=user).count(),
        'total_subjects': Subject.objects.filter(owner=user).count(),
        'total_grades': Grade.objects.filter(owner=user).count(),
        'leave_history': FacultyLeave.objects.filter(faculty__owner=user).order_by('-created_at')[:20],
    }
    return render(request, 'reports/home.html', ctx)
