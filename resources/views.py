from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Subject, Room, Grade, Division
from faculty.models import Faculty

@login_required
def resources_home(request):
    tab = request.GET.get('tab', 'classes')
    ctx = {
        'tab': tab,
        'grades': Grade.objects.filter(owner=request.user).prefetch_related('divisions'),
        'rooms': Room.objects.filter(owner=request.user),
        'subjects': Subject.objects.filter(owner=request.user),
    }
    return render(request, 'resources/home.html', ctx)

@login_required
def add_grade(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        level = request.POST.get('level', 1)
        if name:
            grade = Grade.objects.create(owner=request.user, name=name, level=level)
            # Create divisions
            divs = request.POST.get('divisions', '').strip()
            if divs:
                for i, d in enumerate(divs.split(',')):
                    d = d.strip()
                    if d:
                        Division.objects.create(grade=grade, name=d, strength=request.POST.get('strength', 40))
            messages.success(request, f'Grade "{name}" added successfully.')
    return redirect('resources')

@login_required
def add_room(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Room.objects.create(
                owner=request.user,
                name=name,
                room_number=request.POST.get('room_number', ''),
                room_type=request.POST.get('room_type', 'classroom'),
                capacity=request.POST.get('capacity', 40),
                building=request.POST.get('building', ''),
            )
            messages.success(request, f'Room "{name}" added successfully.')
    return redirect('resources')

@login_required
def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Subject.objects.create(
                owner=request.user,
                name=name,
                code=request.POST.get('code', ''),
                subject_type=request.POST.get('subject_type', 'theory'),
                color=request.POST.get('color', '#6366f1'),
            )
            messages.success(request, f'Subject "{name}" added successfully.')
    return redirect('resources')

@login_required
def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk, owner=request.user)
    grade.delete()
    messages.success(request, 'Grade deleted.')
    return redirect('resources')

@login_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk, owner=request.user)
    room.delete()
    messages.success(request, 'Room deleted.')
    return redirect('resources')

@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, owner=request.user)
    subject.delete()
    messages.success(request, 'Subject deleted.')
    return redirect('resources')
