from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Timetable, BellSchedule, Period, Lesson, TimetableSlot, DAYS
from resources.models import Subject, Grade, Division, Room
from faculty.models import Faculty
from .scheduler import generate_timetable

@login_required
def dashboard(request):
    timetables = Timetable.objects.filter(owner=request.user)
    faculty_count = Faculty.objects.filter(owner=request.user).count()
    subject_count = Subject.objects.filter(owner=request.user).count()
    grade_count = Grade.objects.filter(owner=request.user).count()
    ctx = {
        'timetables': timetables,
        'faculty_count': faculty_count,
        'subject_count': subject_count,
        'grade_count': grade_count,
        'published': timetables.filter(status='published').first(),
    }
    return render(request, 'dashboard/home.html', ctx)

@login_required
def timetable_list(request):
    timetables = Timetable.objects.filter(owner=request.user)
    return render(request, 'timetables/list.html', {'timetables': timetables})

@login_required
def create_timetable(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Timetable name is required.')
            return redirect('timetable_list')
        tt = Timetable.objects.create(
            owner=request.user,
            name=name,
            academic_year=request.POST.get('academic_year', ''),
        )
        messages.success(request, f'Timetable "{name}" created.')
        return redirect('timetable_setup', pk=tt.pk)
    return redirect('timetable_list')

@login_required
def timetable_setup(request, pk):
    tt = get_object_or_404(Timetable, pk=pk, owner=request.user)
    bell_schedules = BellSchedule.objects.filter(owner=request.user)
    grades = Grade.objects.filter(owner=request.user).prefetch_related('divisions')
    faculty_qs = Faculty.objects.filter(owner=request.user, status='active')
    subjects = Subject.objects.filter(owner=request.user)
    rooms = Room.objects.filter(owner=request.user)
    lessons = tt.lessons.select_related('subject', 'faculty', 'division', 'room').all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'assign_bell':
            bell_id = request.POST.get('bell_schedule')
            if bell_id:
                tt.bell_schedule = BellSchedule.objects.get(pk=bell_id, owner=request.user)
                tt.save()
                messages.success(request, 'Bell schedule assigned.')

        elif action == 'add_lesson':
            subject_id = request.POST.get('subject')
            faculty_id = request.POST.get('faculty')
            division_id = request.POST.get('division')
            ppw = request.POST.get('periods_per_week', 4)
            room_id = request.POST.get('room')
            if subject_id and division_id:
                Lesson.objects.create(
                    timetable=tt,
                    subject_id=subject_id,
                    faculty_id=faculty_id if faculty_id else None,
                    division_id=division_id,
                    room_id=room_id if room_id else None,
                    periods_per_week=ppw,
                )
                messages.success(request, 'Lesson added.')
            else:
                messages.error(request, 'Subject and Division are required.')

        elif action == 'delete_lesson':
            lesson_id = request.POST.get('lesson_id')
            Lesson.objects.filter(pk=lesson_id, timetable=tt).delete()
            messages.success(request, 'Lesson removed.')

        elif action == 'generate':
            tt.status = 'generating'
            tt.save()
            success, log = generate_timetable(tt)
            tt.generation_log = log
            tt.ai_generated = True
            tt.status = 'generated' if success else 'draft'
            tt.save()
            if success:
                messages.success(request, 'Timetable generated successfully!')
            else:
                messages.error(request, f'Generation failed: {log[:200]}')
            return redirect('timetable_view', pk=tt.pk)

        elif action == 'publish':
            tt.status = 'published'
            tt.save()
            messages.success(request, 'Timetable published!')

        return redirect('timetable_setup', pk=pk)

    ctx = {
        'tt': tt,
        'bell_schedules': bell_schedules,
        'grades': grades,
        'faculty': faculty_qs,
        'subjects': subjects,
        'rooms': rooms,
        'lessons': lessons,
        'days': DAYS,
        'setup_steps': get_setup_steps(tt),
    }
    return render(request, 'timetables/setup.html', ctx)

def get_setup_steps(tt):
    return {
        'bell': tt.bell_schedule is not None,
        'lessons': tt.lessons.exists(),
        'generated': tt.status in ['generated', 'published'],
    }

@login_required
def timetable_view(request, pk):
    tt = get_object_or_404(Timetable, pk=pk, owner=request.user)
    bell = tt.bell_schedule
    periods = []
    if bell:
        periods = list(bell.periods.order_by('period_number'))
    working_days = bell.working_days if bell else DAYS[:5]

    # Build grid: {division_id: {day: {period_id: slot}}}
    slots = tt.slots.select_related(
        'lesson__subject', 'lesson__division', 'lesson__faculty', 'period', 'room'
    ).all()

    divisions = Division.objects.filter(
        id__in=tt.lessons.values_list('division_id', flat=True)
    ).select_related('grade')

    grid = {}
    for div in divisions:
        grid[div.id] = {day: {} for day in working_days}

    for slot in slots:
        div_id = slot.lesson.division_id
        if div_id in grid and slot.day in grid[div_id]:
            grid[div_id][slot.day][slot.period_id] = slot

    ctx = {
        'tt': tt,
        'periods': periods,
        'working_days': working_days,
        'divisions': divisions,
        'grid': grid,
        'slots': slots,
    }
    return render(request, 'timetables/view.html', ctx)

@login_required
def delete_timetable(request, pk):
    tt = get_object_or_404(Timetable, pk=pk, owner=request.user)
    name = tt.name
    tt.delete()
    messages.success(request, f'Timetable "{name}" deleted.')
    return redirect('timetable_list')

# Bell Schedule Views
@login_required
def bell_list(request):
    bells = BellSchedule.objects.filter(owner=request.user).prefetch_related('periods')
    return render(request, 'timetables/bells.html', {'bells': bells})

@login_required
def create_bell(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        days = request.POST.getlist('working_days')
        if name and days:
            bell = BellSchedule.objects.create(owner=request.user, name=name, working_days=days)
            # Add periods
            period_names = request.POST.getlist('period_name')
            start_times = request.POST.getlist('start_time')
            end_times = request.POST.getlist('end_time')
            period_types = request.POST.getlist('period_type')
            for i, pname in enumerate(period_names):
                if pname.strip() and i < len(start_times) and i < len(end_times):
                    Period.objects.create(
                        bell_schedule=bell,
                        name=pname.strip(),
                        period_number=i + 1,
                        start_time=start_times[i],
                        end_time=end_times[i],
                        period_type=period_types[i] if i < len(period_types) else 'class',
                    )
            messages.success(request, f'Bell schedule "{name}" created.')
        else:
            messages.error(request, 'Name and working days are required.')
    return redirect('bell_list')

@login_required
def delete_bell(request, pk):
    bell = get_object_or_404(BellSchedule, pk=pk, owner=request.user)
    bell.delete()
    messages.success(request, 'Bell schedule deleted.')
    return redirect('bell_list')
