"""
SchedualAI - Timetable Generator
Constraint-based scheduler with AI optimization via Groq
"""
import random
import json
from collections import defaultdict
from django.conf import settings


DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def generate_timetable(timetable):
    """
    Main entry point. Generates slots for all lessons in timetable.
    Returns (success: bool, log: str)
    """
    lessons = list(timetable.lessons.select_related('subject', 'faculty', 'division', 'room').all())
    bell = timetable.bell_schedule
    if not bell:
        return False, "No bell schedule assigned. Please configure a bell schedule first."
    
    class_periods = list(bell.periods.filter(period_type='class').order_by('period_number'))
    working_days = bell.working_days or DAYS[:5]
    
    if not class_periods:
        return False, "Bell schedule has no class periods configured."
    if not lessons:
        return False, "No lessons configured. Add lessons before generating."

    # Clear existing auto-generated slots
    from .models import TimetableSlot
    timetable.slots.filter(is_manual=False).delete()

    log_lines = []
    log_lines.append(f"Starting timetable generation for '{timetable.name}'")
    log_lines.append(f"Working days: {', '.join(working_days)}")
    log_lines.append(f"Class periods per day: {len(class_periods)}")
    log_lines.append(f"Total lessons to schedule: {len(lessons)}")

    # Build availability grid
    # slot_used[division_id][day][period_id] = True
    # faculty_used[faculty_id][day][period_id] = True
    # room_used[room_id][day][period_id] = True
    div_used = defaultdict(lambda: defaultdict(set))
    fac_used = defaultdict(lambda: defaultdict(set))
    room_used = defaultdict(lambda: defaultdict(set))

    slots_to_create = []
    unscheduled = []

    # Sort lessons: more periods/week first (harder to fit)
    lessons_sorted = sorted(lessons, key=lambda l: -l.periods_per_week)

    for lesson in lessons_sorted:
        needed = lesson.periods_per_week
        scheduled = 0
        attempts = 0
        max_attempts = needed * 200

        # Build list of all possible (day, period) combos and shuffle
        all_slots = [(d, p) for d in working_days for p in class_periods]

        # Try to spread across days
        day_counts = defaultdict(int)

        while scheduled < needed and attempts < max_attempts:
            attempts += 1
            random.shuffle(all_slots)

            for day, period in all_slots:
                if scheduled >= needed:
                    break

                div_id = lesson.division.id
                fac_id = lesson.faculty.id if lesson.faculty else None
                pid = period.id

                # Check conflicts
                if pid in div_used[div_id][day]:
                    continue
                if fac_id and pid in fac_used[fac_id][day]:
                    continue

                # Max 1 occurrence of same subject per day
                already_today = any(
                    s for s in slots_to_create
                    if s['lesson_id'] == lesson.id and s['day'] == day
                )
                if already_today:
                    continue

                # Faculty workload per day
                if fac_id:
                    fac_day_count = len(fac_used[fac_id][day])
                    if fac_day_count >= lesson.faculty.max_periods_per_day:
                        continue

                # Room
                room = lesson.room
                if room:
                    if pid in room_used[room.id][day]:
                        room = None  # fallback: no room

                # Assign
                div_used[div_id][day].add(pid)
                if fac_id:
                    fac_used[fac_id][day].add(pid)
                if room:
                    room_used[room.id][day].add(pid)

                slots_to_create.append({
                    'timetable_id': timetable.id,
                    'lesson_id': lesson.id,
                    'day': day,
                    'period_id': pid,
                    'room_id': room.id if room else None,
                    'is_manual': False,
                })
                day_counts[day] += 1
                scheduled += 1

            if scheduled >= needed:
                break

        log_lines.append(
            f"  ✓ {lesson.subject.name} ({lesson.division}) — scheduled {scheduled}/{needed} periods"
        )
        if scheduled < needed:
            unscheduled.append(f"{lesson.subject.name} ({lesson.division}): only {scheduled}/{needed}")

    # Bulk create
    TimetableSlot.objects.bulk_create([
        TimetableSlot(
            timetable_id=s['timetable_id'],
            lesson_id=s['lesson_id'],
            day=s['day'],
            period_id=s['period_id'],
            room_id=s['room_id'],
            is_manual=s['is_manual'],
        ) for s in slots_to_create
    ])

    total = len(slots_to_create)
    log_lines.append(f"\nTotal slots created: {total}")
    if unscheduled:
        log_lines.append("\nWarnings (partial scheduling):")
        for u in unscheduled:
            log_lines.append(f"  ⚠ {u}")
    else:
        log_lines.append("All lessons scheduled successfully! ✓")

    log = '\n'.join(log_lines)
    success = total > 0
    return success, log


def get_timetable_context_for_ai(timetable):
    """Build a text summary of the timetable for Groq chatbot context."""
    lessons = timetable.lessons.select_related('subject', 'faculty', 'division').all()
    slots = timetable.slots.select_related('lesson__subject', 'lesson__division', 'lesson__faculty', 'period').order_by('day', 'period__period_number')

    lines = [f"Timetable: {timetable.name}", f"Status: {timetable.status}", ""]
    lines.append("Lessons configured:")
    for l in lessons:
        lines.append(f"  - {l.subject.name} | {l.division} | Teacher: {l.faculty.name if l.faculty else 'Unassigned'} | {l.periods_per_week} periods/week")

    lines.append("\nScheduled slots (sample, up to 30):")
    for s in slots[:30]:
        lines.append(f"  {s.day} P{s.period.period_number} ({s.period.start_time}-{s.period.end_time}): {s.lesson.subject.name} — {s.lesson.division} — {s.lesson.faculty.name if s.lesson.faculty else 'No teacher'}")

    return '\n'.join(lines)
