# ============================================================
# dashboard/views.py
# ============================================================

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View


class LandingView(View):
    """Public landing page — if logged in, go to dashboard."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, 'dashboard/landing.html')


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        ctx = {
            'timetable_count'     : 0,
            'faculty_count'       : 0,
            'grade_count'         : 0,
            'subject_count'       : 0,
            'pending_leaves'      : 0,
            'recent_timetables'   : [],
        }

        from timetables.models import Timetable
        from faculty.models import Faculty, FacultyLeave
        from resources.models import Grade, Subject

        user = request.user

        ctx['timetable_count']   = Timetable.objects.filter(owner=user).count()
        ctx['faculty_count']     = Faculty.objects.filter(owner=user, status='active').count()
        ctx['grade_count']       = Grade.objects.filter(owner=user).count()
        ctx['subject_count']     = Subject.objects.filter(owner=user).count()
        ctx['pending_leaves']    = FacultyLeave.objects.filter(
                                       faculty__owner=user, status='pending').count()
        ctx['recent_timetables'] = Timetable.objects.filter(
                                       owner=user).order_by('-updated_at')[:5]

        return render(request, 'dashboard/home.html', ctx)