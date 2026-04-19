from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Faculty, FacultyLeave
from resources.models import Subject

@login_required
def faculty_list(request):
    faculty = Faculty.objects.filter(owner=request.user).prefetch_related('subjects')
    subjects = Subject.objects.filter(owner=request.user)
    return render(request, 'faculty/list.html', {'faculty': faculty, 'subjects': subjects})

@login_required
def add_faculty(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            f = Faculty.objects.create(
                owner=request.user,
                name=name,
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                employee_id=request.POST.get('employee_id', ''),
                department=request.POST.get('department', ''),
                designation=request.POST.get('designation', ''),
                max_periods_per_day=request.POST.get('max_periods_per_day', 6),
                max_periods_per_week=request.POST.get('max_periods_per_week', 30),
            )
            subject_ids = request.POST.getlist('subjects')
            if subject_ids:
                f.subjects.set(subject_ids)
            messages.success(request, f'Faculty "{name}" added successfully.')
        else:
            messages.error(request, 'Name is required.')
    return redirect('faculty_list')

@login_required
def edit_faculty(request, pk):
    f = get_object_or_404(Faculty, pk=pk, owner=request.user)
    if request.method == 'POST':
        f.name = request.POST.get('name', f.name)
        f.email = request.POST.get('email', f.email)
        f.phone = request.POST.get('phone', f.phone)
        f.employee_id = request.POST.get('employee_id', f.employee_id)
        f.department = request.POST.get('department', f.department)
        f.designation = request.POST.get('designation', f.designation)
        f.max_periods_per_day = request.POST.get('max_periods_per_day', f.max_periods_per_day)
        f.max_periods_per_week = request.POST.get('max_periods_per_week', f.max_periods_per_week)
        f.status = request.POST.get('status', f.status)
        f.save()
        subject_ids = request.POST.getlist('subjects')
        f.subjects.set(subject_ids)
        messages.success(request, f'Faculty "{f.name}" updated.')
    return redirect('faculty_list')

@login_required
def delete_faculty(request, pk):
    f = get_object_or_404(Faculty, pk=pk, owner=request.user)
    name = f.name
    f.delete()
    messages.success(request, f'Faculty "{name}" deleted.')
    return redirect('faculty_list')

@login_required
def add_leave(request, pk):
    f = get_object_or_404(Faculty, pk=pk, owner=request.user)
    if request.method == 'POST':
        FacultyLeave.objects.create(
            faculty=f,
            leave_type=request.POST.get('leave_type', 'casual'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            reason=request.POST.get('reason', ''),
            status='approved',
        )
        messages.success(request, 'Leave recorded.')
    return redirect('faculty_list')
