"""
scheduling/engine.py  — Timetable Generation Engine
"""
import random
from collections import defaultdict


class TimetableGenerator:
    def __init__(self, timetable):
        self.timetable = timetable
        self.log_lines = []
        self.bell = timetable.bell_schedule
        self.lessons = list(
            timetable.lessons.select_related('division__grade', 'subject', 'faculty').all()
        )

    def log(self, msg):
        self.log_lines.append(msg)

    def get_log(self):
        return '\n'.join(self.log_lines)

    def generate(self):
        from timetables.models import TimetableSlot, Period

        if not self.bell:
            raise ValueError('No bell schedule assigned to this timetable.')

        working_days = self.bell.working_days  # e.g. ['Monday','Tuesday',...]
        periods = list(
            Period.objects.filter(bell_schedule=self.bell, period_type='class')
            .order_by('period_number')
        )

        if not working_days:
            raise ValueError('Bell schedule has no working days.')
        if not periods:
            raise ValueError('Bell schedule has no class periods.')
        if not self.lessons:
            raise ValueError('No lessons configured for this timetable.')

        self.log(f'Days: {working_days}')
        self.log(f'Periods per day: {len(periods)}')
        self.log(f'Lessons to schedule: {len(self.lessons)}')

        # Build a pool of (lesson, remaining_count) entries
        pool = []
        for lesson in self.lessons:
            for _ in range(lesson.periods_per_week):
                pool.append(lesson)

        random.shuffle(pool)

        slots = []
        # Track what's already placed: faculty_day_period, division_day_period
        faculty_busy   = defaultdict(set)  # faculty_id -> set of (day, period_id)
        division_busy  = defaultdict(set)  # division_id -> set of (day, period_id)

        unscheduled = []

        for lesson in pool:
            placed = False
            # Try every day/period combination in random order
            options = [
                (day, period)
                for day in working_days
                for period in periods
            ]
            random.shuffle(options)

            for day, period in options:
                fkey = (day, period.pk)
                dkey = (day, period.pk)

                if fkey in faculty_busy[lesson.faculty_id]:
                    continue  # faculty already has a class
                if dkey in division_busy[lesson.division_id]:
                    continue  # division already has a class

                # Place it
                faculty_busy[lesson.faculty_id].add(fkey)
                division_busy[lesson.division_id].add(dkey)

                slots.append(TimetableSlot(
                    timetable=self.timetable,
                    lesson=lesson,
                    day=day,
                    period=period,
                ))
                placed = True
                break

            if not placed:
                unscheduled.append(lesson)
                self.log(f'⚠ Could not place: {lesson.subject.name} / {lesson.division}')

        self.log(f'✓ Placed {len(slots)} slots.')
        if unscheduled:
            self.log(f'✗ Unscheduled: {len(unscheduled)} periods (conflicts or full grid).')

        return slots